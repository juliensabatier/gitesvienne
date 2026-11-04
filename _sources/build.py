# -*- coding: utf-8 -*-
"""Génère index.html à partir de data.py.
Usage : python3 build.py            -> ../index.html (version OVH)
        python3 build.py --preview  -> ../preview.html (aperçu, titre court)
"""
import json, sys, html, os
sys.path.insert(0, os.path.dirname(__file__))
from data import *
from themes import THEMES

E = html.escape
PREVIEW = "--preview" in sys.argv

def eur(n):
    return f"{n:,}".replace(",", " ") + " €"

def min_price(d):
    return min(d["tarifs"].values())

def link(slug):
    return "#" + slug if PREVIEW else PAGES[slug][0]

def card(d):
    tag = "Mariages et réceptions" if d["famille"] == "mariage" else "Week-ends et vacances"
    chiffres = "".join(f'<li><b>{E(v)}</b><span>{E(l)}</span></li>' for v, l in d["chiffres"])
    prefix = "à partir de " if d["famille"] == "mariage" or True else ""
    return f'''
<article class="card card--{d['famille']}" id="carte-{d['slug']}">
  <a class="card__img" href="{link(d['slug'])}" aria-label="Découvrir {E(d['nom'])}">
    <img src="img/{d['slug']}-card-s.jpg" srcset="img/{d['slug']}-card-s.jpg 720w, img/{d['slug']}-card.jpg 1600w" sizes="(max-width: 700px) 100vw, 50vw" alt="{E(d['nom'])}" loading="lazy" width="720" height="480">
  </a>
  <div class="card__body">
    <p class="card__lieu card__lieu--row"><span>{E(d['lieu'])}</span>{iti_card(d)}</p>
    <h3 class="card__nom"><a href="{link(d['slug'])}">{E(d['nom'])}</a></h3>
    <p class="card__accroche">{E(d['accroche'])}</p>
    <ul class="chiffres">{chiffres}</ul>
    <div class="card__foot">
      <p class="prix">{prefix}<b>{eur(min_price(d))}</b> {E(d['unite'])}</p>
      <div class="card__actions">
        <a class="btn btn--ghost" href="{link(d['slug'])}">Découvrir</a>
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

def avis_url(slug):
    return "https://maps.google.com/?cid=" + AVIS[slug]["cid"]
STAR = '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z"/></svg>'
def stars():
    return '<span class="stars" aria-hidden="true">' + STAR*5 + '</span>'
def avis_cards(slug, n=3):
    a = AVIS[slug]
    return "".join(f'''<figure class="avis__item"><blockquote>« {E(t)} »</blockquote>
      <figcaption><b>{E(nom)}</b><span>{E(ctx)}</span></figcaption></figure>''' for nom, ctx, t in a["extraits"][:n])
def avis_fiche(d):
    a = AVIS[d["slug"]]
    return f'''<section class="avis avis--fiche" aria-labelledby="av-{d['slug']}">
      <div class="avis__head"><div><p class="eyebrow">Avis clients</p><h3 id="av-{d['slug']}">Ils nous ont fait confiance</h3></div>
      <a class="avis__score" href="{avis_url(d['slug'])}" target="_blank" rel="noopener">{stars()}<b>{a['note']}/5</b><span>{a['nb']} avis Google ↗</span></a></div>
      <div class="avis__grid">{avis_cards(d['slug'])}</div></section>'''
def avis_home():
    out = []
    for d in DOMAINES:
        a = AVIS[d["slug"]]
        nom, ctx, t = a["extraits"][0]
        out.append(f'''<article class="avis__dom"><a class="avis__score" href="{avis_url(d['slug'])}" target="_blank" rel="noopener">{stars()}<b>{a['note']}/5</b><span>{a['nb']} avis ↗</span></a>
          <h3><a href="{link(d['slug'])}">{E(d['nom'])}</a></h3><blockquote>« {E(t)} »</blockquote><p class="avis__who"><b>{E(nom)}</b> · {E(ctx)}</p></article>''')
    total = sum(AVIS[k]["nb"] for k in AVIS)
    return "".join(out), total

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
  <div class="wrap fiche__avis">{avis_fiche(d)}</div>
  <div class="wrap fiche__cons">{conseiller(d['slug'])}</div>
</section>'''

def biz(d):
    return {"@type": ["LodgingBusiness", "EventVenue"], "@id": f"https://gitesvienne.fr{PAGES[d['slug']][0]}#lieu",
            "name": d["nom"], "description": d["accroche"],
            "address": {"@type": "PostalAddress", "streetAddress": d["adresse"], "addressRegion": "Nouvelle-Aquitaine", "addressCountry": "FR"},
            "url": f"https://gitesvienne.fr{PAGES[d['slug']][0]}", "image": f"https://gitesvienne.fr/img/{d['slug']}-card.jpg",
            "telephone": PHONE_INTL, "priceRange": f"à partir de {min_price(d)} €",
            "sameAs": [d["site"], avis_url(d["slug"])]}

def jsonld(only=None):
    items = [biz(d) for d in DOMAINES if only is None or d["slug"] == only]
    if only is None:
        items.insert(0, {"@type": "Organization", "@id": "https://gitesvienne.fr/#org", "name": "Gîtes Vienne", "url": "https://gitesvienne.fr/",
                         "email": CONTACT_EMAIL, "telephone": PHONE_INTL, "logo": "https://gitesvienne.fr/img/favicon.png",
                         "founder": {"@type": "Person", "name": "Julien Sabatier"}})
    return json.dumps({"@context": "https://schema.org", "@graph": items}, ensure_ascii=False)

def theme_body(t):
    doms = {d["slug"]: d for d in DOMAINES}
    intro = "".join(f"<p>{E(x)}</p>" for x in t["intro"])
    pts = "".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a, b in t["points"])
    faq = "".join(f'<details class="faq__item"><summary>{E(q)}</summary><p>{E(r)}</p></details>' for q, r in t["faq"])
    others = "".join(f'<a class="btn btn--ghost" href="/{o["slug"]}/">{E(o["eyebrow"])}</a>' for o in THEMES if o["slug"] != t["slug"])
    cards = "".join(card(doms[s]) for s in t["domaines"])
    return f'''
<section class="section section--{t['famille']} theme">
  <div class="wrap">
    <p class="eyebrow mark">{E(t['eyebrow'])}</p>
    <h1 class="theme__h1">{t['h1']}</h1>
    <div class="theme__intro">{intro}</div>
    <ul class="theme__pts">{pts}</ul>
    <div class="actions"><a class="btn" href="/#disponibilites">Voir les dates libres</a><a class="btn btn--ghost" href="#contact" data-ask="" data-mode="visite">Demander une visite</a></div>
  </div>
</section>
<section class="section section--{t['famille']}" style="padding-top:0">
  <div class="wrap">
    <div class="cards cards--3">{cards}</div>
  </div>
</section>
<section class="section faq" style="padding-top:0">
  <div class="wrap faq__wrap">
    <h2>Questions fréquentes</h2>
    {faq}
    <p class="faq__more">Voir aussi : {others} <a class="btn btn--ghost" href="/">Tous les domaines</a></p>
  </div>
</section>'''

def theme_jsonld(t):
    return json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": f"https://gitesvienne.fr/{t['slug']}/", "name": t["title"], "description": t["desc"],
         "isPartOf": {"@id": "https://gitesvienne.fr/#org"}, "inLanguage": "fr-FR"},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in t["faq"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Gîtes Vienne", "item": "https://gitesvienne.fr/"},
            {"@type": "ListItem", "position": 2, "name": t["eyebrow"], "item": f"https://gitesvienne.fr/{t['slug']}/"}]},
    ] + [biz(d) for d in DOMAINES if d["slug"] in t["domaines"]]}, ensure_ascii=False)

js_data = {
    "domaines": [{k: d[k] for k in ["slug", "famille", "nom", "court", "saisons", "default_saison", "tarifs", "unite", "formule"]} for d in DOMAINES],
    "ical": ICAL, "snapshot": SNAPSHOT, "snapshotDate": SNAPSHOT_DATE, "saisonNom": SAISON_NOM,
    "email": CONTACT_EMAIL, "plaquettes": PLAQUETTES, "pages": {k: v[0] for k, v in PAGES.items()},
}

tpl = open(os.path.join(os.path.dirname(__file__), "template.html"), encoding="utf-8").read()
import re
ROOT = os.path.join(os.path.dirname(__file__), "..")

def common(t):
    return (t.replace("%%CARDS_MARIAGE%%", "".join(card(d) for d in DOMAINES if d["famille"] == "mariage"))
          .replace("%%CARDS_GITE%%", "".join(card(d) for d in DOMAINES if d["famille"] == "gite"))
          .replace("%%OPTIONS%%", "".join(f'<option value="{d["slug"]}">{E(d["nom"])}</option>' for d in DOMAINES))
          .replace("%%CHIPS%%", "".join(f'<button type="button" class="chip chip--{d["famille"]}" data-chip="{d["slug"]}" aria-pressed="false">{E(d["court"])}</button>' for d in DOMAINES))
          .replace("%%LINKS%%", "".join(f'<li><a href="{d["site"]}" target="_blank" rel="noopener">{E(d["nom"])}</a></li>' for d in DOMAINES))
          .replace("%%THEMES%%", "".join(f'<li><a href="{"#" if PREVIEW else "/" + t["slug"] + "/"}">{E(t["eyebrow"])}</a></li>' for t in THEMES))
          .replace("%%EMAIL%%", CONTACT_EMAIL).replace("%%PHONE%%", PHONE).replace("%%PHONE_INTL%%", PHONE_INTL)
          .replace("%%CONSEILLER%%", conseiller(compact=True)).replace("%%SLIDES%%", slides())
          .replace("%%AVIS_HOME%%", avis_home()[0]).replace("%%AVIS_TOTAL%%", str(avis_home()[1]))
          .replace("%%DATA%%", json.dumps(js_data, ensure_ascii=False)))

def wrap(out, favicon="img/favicon.png"):
    head, body = out.replace("<!--HEAD-->", "").split("<!--BODY-->")
    return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<link rel="icon" href="{favicon}">\n' + head + '</head>\n<body>\n' + body + '</body>\n</html>\n')

def write(path, txt):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(txt); print("écrit", os.path.relpath(path, ROOT), len(txt), "octets")

if PREVIEW:
    out = common(tpl.replace("%%TITLE%%", "Gîtes Vienne")).replace("%%FICHES%%", "".join(fiche(d) for d in DOMAINES)).replace("%%JSONLD%%", jsonld())
    out = out.replace('<!--HEAD-->', '<meta name="claude:viewport-fit-sides" content="cover">').replace("<!--BODY-->", "").replace("<!--HOME-->", "").replace("<!--/HOME-->", "")
    write(os.path.join(ROOT, "preview.html"), out)
else:
    home = common(tpl.replace("%%TITLE%%", "Gîtes Vienne · Domaines de mariage et gîtes de groupe dans la Vienne (86)")).replace("%%FICHES%%", "").replace("%%JSONLD%%", jsonld())
    write(os.path.join(ROOT, "index.html"), wrap(home.replace("<!--HOME-->", "").replace("<!--/HOME-->", "")))
    for d in DOMAINES:
        url, ttl, desc = PAGES[d["slug"]]
        f = fiche(d).replace(' hidden aria-labelledby', ' aria-labelledby').replace(f'class="fiche fiche--{d["famille"]}"', f'class="fiche fiche--{d["famille"]} fiche--page"')
        f = f.replace(f'<h2 id="t-{d["slug"]}">', f'<h1 id="t-{d["slug"]}">').replace(f'{E(d["nom"])}</h2><p>', f'{E(d["nom"])}</h1><p>', 1)
        f = f.replace('href="#domaines"', 'href="/#mariages"')
        f = re.sub(r'href="#contact" data-ask="(\w+)" data-mode="(\w+)"', r'href="/?d=\1&amp;m=\2#contact" data-ask="\1" data-mode="\2"', f)
        f = re.sub(r'href="#contact" data-ask="(\w+)"', r'href="/?d=\1#contact" data-ask="\1"', f)
        page = common(tpl.replace("%%TITLE%%", E(ttl)))
        a, b = page.split("<!--HOME-->"); _, c = b.split("<!--/HOME-->")
        page = a + f + c
        page = page.replace("%%FICHES%%", "").replace("%%JSONLD%%", jsonld(d["slug"]))
        page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', page, count=1)
        page = page.replace('<link rel="canonical" href="https://gitesvienne.fr/">', f'<link rel="canonical" href="https://gitesvienne.fr{url}">')
        page = page.replace('<meta property="og:url" content="https://gitesvienne.fr/">', f'<meta property="og:url" content="https://gitesvienne.fr{url}">')
        page = page.replace('content="https://gitesvienne.fr/img/borderie-card.jpg"', f'content="https://gitesvienne.fr/img/{d["slug"]}-card.jpg"')
        page = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(d["nom"])}">', page, count=1)
        # chemins absolus
        page = re.sub(r'(?<=[\s"(,])(img|plaquettes)/', r'/\1/', page)
        page = page.replace('fetch("ical.php"', 'fetch("/ical.php"').replace('fetch("contact.php"', 'fetch("/contact.php"')
        page = page.replace('href="#accueil"', 'href="/"').replace('href="#mariages"', 'href="/#mariages"').replace('href="#week-ends"', 'href="/#week-ends"').replace('href="#avis"', 'href="/#avis"').replace('href="#disponibilites"', 'href="/#disponibilites"')
        write(os.path.join(ROOT, url.strip("/"), "index.html"), wrap(page, "/img/favicon.png"))
    for t in THEMES:
        url = f"/{t['slug']}/"
        page = common(tpl.replace("%%TITLE%%", E(t["title"])))
        a, b = page.split("<!--HOME-->"); _, c = b.split("<!--/HOME-->")
        page = a + theme_body(t) + c
        page = page.replace("%%FICHES%%", "").replace("%%JSONLD%%", theme_jsonld(t))
        page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(t["desc"])}">', page, count=1)
        page = page.replace('<link rel="canonical" href="https://gitesvienne.fr/">', f'<link rel="canonical" href="https://gitesvienne.fr{url}">')
        page = page.replace('<meta property="og:url" content="https://gitesvienne.fr/">', f'<meta property="og:url" content="https://gitesvienne.fr{url}">')
        page = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(t["title"])}">', page, count=1)
        page = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(t["desc"])}">', page, count=1)
        page = re.sub(r'(?<=[\s"(,])(img|plaquettes)/', r'/\1/', page)
        page = page.replace('fetch("ical.php"', 'fetch("/ical.php"').replace('fetch("contact.php"', 'fetch("/contact.php"')
        page = page.replace('href="#accueil"', 'href="/"').replace('href="#mariages"', 'href="/#mariages"').replace('href="#week-ends"', 'href="/#week-ends"').replace('href="#avis"', 'href="/#avis"').replace('href="#disponibilites"', 'href="/#disponibilites"')
        write(os.path.join(ROOT, t["slug"], "index.html"), wrap(page, "/img/favicon.png"))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
          '  <url><loc>https://gitesvienne.fr/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>']
    sm += [f'  <url><loc>https://gitesvienne.fr{PAGES[d["slug"]][0]}</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>' for d in DOMAINES]
    sm += [f'  <url><loc>https://gitesvienne.fr/{t["slug"]}/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>' for t in THEMES]
    sm += [f'  <url><loc>https://gitesvienne.fr/{p}</loc></url>' for p in PLAQUETTES.values()]
    sm.append('</urlset>')
    write(os.path.join(ROOT, "sitemap.xml"), "\n".join(sm) + "\n")
