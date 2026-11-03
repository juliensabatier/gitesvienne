# -*- coding: utf-8 -*-
"""Génère index.html à partir de data.py.
Usage : python3 build.py            -> ../index.html (version OVH)
        python3 build.py --preview  -> ../preview.html (aperçu, titre court)
"""
import json, sys, html, os
sys.path.insert(0, os.path.dirname(__file__))
from data import *

E = html.escape
PREVIEW = "--preview" in sys.argv

def eur(n):
    return f"{n:,}".replace(",", " ") + " €"

def min_price(d):
    return min(d["tarifs"].values())

def card(d):
    tag = "Mariages et réceptions" if d["famille"] == "mariage" else "Week-ends et vacances"
    chiffres = "".join(f'<li><b>{E(v)}</b><span>{E(l)}</span></li>' for v, l in d["chiffres"])
    prefix = "à partir de " if d["famille"] == "mariage" or True else ""
    return f'''
<article class="card card--{d['famille']}" id="carte-{d['slug']}">
  <a class="card__img" href="#{d['slug']}" aria-label="Découvrir {E(d['nom'])}">
    <img src="img/{d['slug']}-card-s.jpg" srcset="img/{d['slug']}-card-s.jpg 720w, img/{d['slug']}-card.jpg 1600w" sizes="(max-width: 700px) 100vw, 50vw" alt="{E(d['nom'])}" loading="lazy" width="720" height="480">
  </a>
  <div class="card__body">
    <p class="card__lieu card__lieu--row"><span>{E(d['lieu'])}</span>{iti_card(d)}</p>
    <h3 class="card__nom"><a href="#{d['slug']}">{E(d['nom'])}</a></h3>
    <p class="card__accroche">{E(d['accroche'])}</p>
    <ul class="chiffres">{chiffres}</ul>
    <div class="card__foot">
      <p class="prix">{prefix}<b>{eur(min_price(d))}</b> {E(d['unite'])}</p>
      <div class="card__actions">
        <a class="btn btn--ghost" href="#{d['slug']}">Découvrir</a>
        <button class="btn" type="button" data-dispo="{d['slug']}">Voir les dates</button>
      </div>{plaq_card(d)}
    </div>
  </div>
</article>'''

from urllib.parse import quote
def maps_url(slug):
    return "https://www.google.com/maps/dir/?api=1&destination=" + quote(MAPS[slug])
def iti_card(d):
    return f'<a class="iti" href="{maps_url(d["slug"])}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>Itinéraire depuis chez moi</a>'

def plaq_card(d):
    p = PLAQUETTES.get(d["slug"])
    if not p: return ""
    return f'<p class="card__plaq"><a class="lien" href="{p}" target="_blank" rel="noopener">Lire la plaquette (PDF) ↗</a><a class="dl" href="{p}" download>Télécharger</a></p>'

def plaq_block(d):
    p = PLAQUETTES.get(d["slug"])
    if not p: return ""
    return f'''<div class="side-block plaq"><h3>La plaquette</h3><p>Espaces, chambres, tarifs détaillés et prestataires, au format PDF.</p>
        <div class="plaq__btns"><a class="btn btn--ghost" href="{p}" target="_blank" rel="noopener">Ouvrir ↗</a><a class="btn btn--ghost" href="{p}" download>Télécharger</a></div></div>'''

def conseiller(slug="", compact=False):
    c = CONSEILLER
    full = f"{c['prenom']} {c['nom']}"
    has = os.path.exists(os.path.join(os.path.dirname(__file__), "..", c["photo"]))
    ini = (c["prenom"][0] + c["nom"][0]).upper()
    pic = (f'<img class="cons__pic" src="{c["photo"]}" alt="{E(full)}" width="120" height="120" loading="lazy">' if has
           else f'<span class="cons__pic cons__ini" aria-hidden="true">{ini}</span>')
    btns = ""
    if slug:
        d = next(x for x in DOMAINES if x["slug"] == slug)
        visite = (f'<a class="btn" href="#contact" data-ask="{slug}" data-mode="visite">Demander une visite</a>' if d["famille"] == "mariage" else "")
        btns = f'<div class="cons__btns">{visite}<a class="btn btn--ghost" href="#contact" data-ask="{slug}" data-mode="date">Demander une date</a></div>'
    return f'''<div class="cons{' cons--compact' if compact else ''}">{pic}<div class="cons__txt"><p class="eyebrow">{E(c['role'])}</p>
      <p class="cons__nom">{E(full)}</p><p class="cons__desc">{E(c['texte'])}</p>
      <p class="cons__coord">{E(CONTACT_EMAIL)} · {E(PHONE)}</p>{btns}</div></div>'''

HERO = [("borderie-card","borderie"),("montbeil-01","montbeil"),("persine-01","persine"),("melior-card","melior"),("borderie-13","borderie"),("elinas-card","elinas"),("montbeil-card","montbeil")]
def slides():
    noms = {d["slug"]: d["nom"] for d in DOMAINES}
    out = []
    for i, (img, slug) in enumerate(HERO):
        attr = f'src="img/{img}.jpg" fetchpriority="high"' if i == 0 else f'data-src="img/{img}.jpg"'
        out.append(f'<li class="slide" data-slug="{slug}" data-nom="{E(noms[slug])}"><img {attr} alt=""></li>')
    return "".join(out)

def tarif_table(d):
    order = [k for k in ["H", "M", "B", "C", "W"] if k in d["tarifs"]]
    rows = "".join(
        f'<tr><th scope="row">{SAISON_NOM[k]}<small>{E(d["periodes"][k])}</small></th><td>{eur(d["tarifs"][k])}</td></tr>'
        for k in order)
    opts = ""
    if d["options"]:
        opts = '<h4>Options</h4><table class="tarifs tarifs--opts">' + "".join(
            f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td></tr>' for a, b in d["options"]) + "</table>"
    note = '<p class="note">Tarif indicatif « à partir de », confirmé selon les dates et le nombre de personnes.</p>' if d["famille"] == "gite" else ""
    return f'''<h3>Tarifs</h3><p class="formule">{E(d['formule'])}</p>
<table class="tarifs">{rows}</table>{note}{opts}'''

def fiche(d):
    chiffres = "".join(f'<li><b>{E(v)}</b><span>{E(l)}</span></li>' for v, l in d["chiffres"])
    texte = "".join(f"<p>{E(p)}</p>" for p in d["texte"])
    atouts = "".join(f"<li>{E(a)}</li>" for a in d["atouts"])
    photos = "".join(
        f'<figure><button type="button" class="ph" data-full="img/{p}.jpg" data-cap="{E(c)}"><img src="img/{p}-s.jpg" alt="{E(c)}" loading="lazy"></button><figcaption>{E(c)}</figcaption></figure>'
        for p, c in d["photos"])
    fam = "Mariages et réceptions" if d["famille"] == "mariage" else "Week-ends et vacances"
    return f'''
<section class="fiche fiche--{d['famille']}" id="fiche-{d['slug']}" data-slug="{d['slug']}" hidden aria-labelledby="t-{d['slug']}">
  <div class="fiche__bar"><a class="back" href="#domaines">← Tous les domaines</a><span class="fiche__fam">{fam}</span>
    <span class="fiche__acts">{('<a class="btn btn--sm btn--ghost" href="#contact" data-ask="'+d['slug']+'" data-mode="visite">Demander une visite</a>') if d['famille']=='mariage' else ''}<a class="btn btn--sm" href="#contact" data-ask="{d['slug']}" data-mode="date">Demander une date</a></span></div>
  <header class="fiche__hero">
    <img src="img/{d['slug']}-card.jpg" alt="{E(d['nom'])}">
    <div class="fiche__title"><p class="card__lieu">{E(d['lieu'])}</p><h2 id="t-{d['slug']}">{E(d['nom'])}</h2><p>{E(d['accroche'])}</p></div>
  </header>
  <div class="wrap fiche__grid">
    <div class="fiche__main">
      <ul class="chiffres chiffres--lg">{chiffres}</ul>
      <div class="prose">{texte}</div>
      <div class="galerie">{photos}</div>
      <h3>Disponibilités</h3>
      <p class="hint">Les jours barrés sont déjà réservés. Touchez une date d'arrivée puis une date de départ.</p>
      <div class="cal" data-cal="{d['slug']}"></div>
    </div>
    <aside class="fiche__side">
      <div class="side-block">{tarif_table(d)}</div>
      {plaq_block(d)}
      <div class="side-block"><h3>Les plus</h3><ul class="atouts">{atouts}</ul></div>
      <div class="side-block"><h3>Accès</h3><p>{E(d['adresse'])}</p><p>{E(d['acces'])}</p>
        <a class="btn btn--ghost btn--block" href="{maps_url(d['slug'])}" target="_blank" rel="noopener">Calculer mon trajet (Google Maps) ↗</a>
        <p><a class="lien" href="{d['site']}" target="_blank" rel="noopener">Voir le site du domaine ↗</a></p></div>
      {('<a class="btn btn--block btn--ghost" href="#contact" data-ask="'+d['slug']+'" data-mode="visite">Demander une visite</a>') if d['famille']=='mariage' else ''}
      <a class="btn btn--block" href="#contact" data-ask="{d['slug']}" data-mode="date">Demander une date</a>
    </aside>
  </div>
  <div class="wrap fiche__cons">{conseiller(d['slug'])}</div>
</section>'''

def jsonld():
    items = []
    for d in DOMAINES:
        items.append({"@type": "LodgingBusiness", "name": d["nom"], "description": d["accroche"],
                      "address": {"@type": "PostalAddress", "streetAddress": d["adresse"], "addressCountry": "FR"},
                      "url": f"https://gitesvienne.fr/#{d['slug']}", "image": f"https://gitesvienne.fr/img/{d['slug']}-card.jpg",
                      "priceRange": f"à partir de {min_price(d)} €"})
    return json.dumps({"@context": "https://schema.org", "@graph": items}, ensure_ascii=False)

js_data = {
    "domaines": [{k: d[k] for k in ["slug", "famille", "nom", "court", "saisons", "default_saison", "tarifs", "unite", "formule"]} for d in DOMAINES],
    "ical": ICAL, "snapshot": SNAPSHOT, "snapshotDate": SNAPSHOT_DATE, "saisonNom": SAISON_NOM,
    "email": CONTACT_EMAIL, "plaquettes": PLAQUETTES,
}

tpl = open(os.path.join(os.path.dirname(__file__), "template.html"), encoding="utf-8").read()
title = "Gîtes Vienne" if PREVIEW else "Gîtes Vienne · Domaines de mariage et gîtes près du Futuroscope"
out = (tpl.replace("%%TITLE%%", title)
          .replace("%%CARDS_MARIAGE%%", "".join(card(d) for d in DOMAINES if d["famille"] == "mariage"))
          .replace("%%CARDS_GITE%%", "".join(card(d) for d in DOMAINES if d["famille"] == "gite"))
          .replace("%%FICHES%%", "".join(fiche(d) for d in DOMAINES))
          .replace("%%OPTIONS%%", "".join(f'<option value="{d["slug"]}">{E(d["nom"])}</option>' for d in DOMAINES))
          .replace("%%CHIPS%%", "".join(f'<button type="button" class="chip chip--{d["famille"]}" data-chip="{d["slug"]}" aria-pressed="false">{E(d["court"])}</button>' for d in DOMAINES))
          .replace("%%LINKS%%", "".join(f'<li><a href="{d["site"]}" target="_blank" rel="noopener">{E(d["nom"])}</a></li>' for d in DOMAINES))
          .replace("%%EMAIL%%", CONTACT_EMAIL).replace("%%PHONE%%", PHONE).replace("%%PHONE_INTL%%", PHONE_INTL)
          .replace("%%JSONLD%%", jsonld()).replace("%%CONSEILLER%%", conseiller(compact=True)).replace("%%SLIDES%%", slides())
          .replace("%%DATA%%", json.dumps(js_data, ensure_ascii=False)))
if PREVIEW:
    out = out.replace('<!--HEAD-->', '<meta name="claude:viewport-fit-sides" content="cover">').replace("<!--BODY-->", "")
else:
    head, body = out.replace("<!--HEAD-->", "").split("<!--BODY-->")
    out = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '<link rel="icon" href="img/favicon.png">\n' + head + '</head>\n<body>\n' + body + '</body>\n</html>\n')
dest = os.path.join(os.path.dirname(__file__), "..", "preview.html" if PREVIEW else "index.html")
open(dest, "w", encoding="utf-8").write(out)
print("écrit", os.path.abspath(dest), len(out), "octets")
