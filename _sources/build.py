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
    tag = "Domaines de mariage" if d["famille"] == "mariage" else "Gîtes"
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

def video_block(d):
    if not d.get("video"):
        return ""
    ids, titre = d["video"]
    ids = [ids] if isinstance(ids, str) else ids
    out = f'<h3>{E(titre)}</h3>'
    for i, vid in enumerate(ids, 1):
        t = titre if len(ids) == 1 else f"{titre} ({i}/{len(ids)})"
        out += (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}?rel=0" '
                f'title="{E(t)}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" '
                f'allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>'
                f'<p class="hint"><a class="lien" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">Voir la vidéo sur YouTube ↗</a></p>')
    return out

def fiche(d):
    chiffres = "".join(f'<li><b>{E(v)}</b><span>{E(l)}</span></li>' for v, l in d["chiffres"])
    texte = "".join(f"<p>{E(p)}</p>" for p in d["texte"])
    atouts = "".join(f"<li>{E(a)}</li>" for a in d["atouts"])
    photos = "".join(
        f'<figure><button type="button" class="ph" data-full="img/{p}.jpg" data-cap="{E(c)}"><img src="img/{p}-s.jpg" alt="{E(c)}" loading="lazy"></button><figcaption>{E(c)}</figcaption></figure>'
        for p, c in d["photos"])
    fam = "Domaines de mariage" if d["famille"] == "mariage" else "Gîtes"
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
      {video_block(d)}
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
      <a class="btn btn--block btn--ghost" href="#contact" data-ask="{d['slug']}" data-mode="appel">Prendre rendez-vous téléphonique</a>
      <a class="btn btn--block" href="#contact" data-ask="{d['slug']}" data-mode="date">Demander une date</a>
    </aside>
  </div>
  <div class="wrap fiche__avis">{avis_fiche(d)}</div>
  <div class="wrap fiche__cons">{conseiller(d['slug'])}</div>
</section>'''

SITE = "https://gitesvienne.fr"

def biz(d):
    """Fiche schema.org d'un domaine (même contenu sur toutes les pages qui la citent)."""
    s, url = SCHEMA[d["slug"]], f"{SITE}{PAGES[d['slug']][0]}"
    imgs = [f"{SITE}/img/{i}" for i in s["images"]]
    adr = {"@type": "PostalAddress"}
    if s.get("rue"): adr["streetAddress"] = s["rue"]
    adr.update({"postalCode": s["cp"], "addressLocality": s["ville"], "addressRegion": "Nouvelle-Aquitaine", "addressCountry": "FR"})
    logement = {"@type": "Accommodation", "name": s["hebergement"]}
    if s.get("chambres"): logement["numberOfRooms"] = s["chambres"]
    if s.get("sdb"): logement["numberOfBathroomsTotal"] = s["sdb"]
    logement["occupancy"] = {"@type": "QuantitativeValue", "maxValue": s["couchages"], "unitText": "couchages"}
    mariage = d["famille"] == "mariage"
    b = {"@type": ["LodgingBusiness", "EventVenue"] if mariage else "LodgingBusiness", "@id": f"{url}#lieu",
         "name": d["nom"], "description": s["description"], "url": url,
         "image": imgs if len(imgs) > 1 else imgs[0],
         "telephone": PHONE_INTL, "email": CONTACT_EMAIL, "address": adr,
         "containedInPlace": {"@type": "AdministrativeArea", "name": s["departement"]},
         "hasMap": avis_url(d["slug"])}
    if s.get("convives"): b["maximumAttendeeCapacity"] = max(s["convives"], s.get("debout", 0))
    if s.get("chambres"): b["numberOfRooms"] = s["chambres"]
    b["containsPlace"] = logement
    b["amenityFeature"] = [{"@type": "LocationFeatureSpecification", "name": e, "value": True} for e in s["equipements"]]
    b["priceRange"] = s["prix"]
    b["makesOffer"] = {"@type": "Offer", "name": s["offre"], "price": min_price(d), "priceCurrency": "EUR", "url": url}
    b["parentOrganization"] = {"@id": f"{SITE}/#org"}
    b["sameAs"] = s["sites"] + [avis_url(d["slug"])]
    return b

def org():
    return {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Gîtes Vienne", "url": f"{SITE}/",
            "description": ORG_DESC, "email": CONTACT_EMAIL, "telephone": PHONE_INTL,
            "logo": {"@type": "ImageObject", "url": f"{SITE}/img/favicon.png"},
            "founder": {"@id": f"{SITE}/#julien-sabatier"},
            "contactPoint": {"@type": "ContactPoint", "contactType": "reservations", "telephone": PHONE_INTL,
                             "email": CONTACT_EMAIL, "availableLanguage": "fr"},
            "areaServed": [{"@type": "AdministrativeArea", "name": "Vienne (86)"}, {"@type": "AdministrativeArea", "name": "Charente (16)"}],
            "knowsAbout": ORG_SAVOIRS}

FAQ_HOME = next(t["faq"] for t in THEMES if t["slug"] == "gite-mariage-vienne")

def jsonld(only=None):
    if only is not None:
        return json.dumps({"@context": "https://schema.org", "@graph": [biz(d) for d in DOMAINES if d["slug"] == only]}, ensure_ascii=False)
    graph = [
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Gîtes Vienne",
         "description": SITE_DESC, "inLanguage": "fr-FR", "publisher": {"@id": f"{SITE}/#org"}},
        {"@type": "WebPage", "@id": f"{SITE}/#webpage", "url": f"{SITE}/",
         "name": "Gîtes Vienne · Domaines de mariage et gîtes de groupe dans la Vienne (86)",
         "description": SITE_PAGE_DESC, "inLanguage": "fr-FR",
         "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#org"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/img/borderie-card.jpg"},
         "mainEntity": {"@id": f"{SITE}/#domaines"},
         "relatedLink": [f"{SITE}/{t['slug']}/" for t in THEMES]},
        {"@type": "FAQPage", "@id": f"{SITE}/#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ_HOME]},
        org(),
        {"@type": "Person", "@id": f"{SITE}/#julien-sabatier", "name": f"{CONSEILLER['prenom']} {CONSEILLER['nom']}",
         "image": f"{SITE}/{CONSEILLER['photo']}", "worksFor": {"@id": f"{SITE}/#org"}},
        {"@type": "ItemList", "@id": f"{SITE}/#domaines", "name": "Domaines de mariage et gîtes de groupe autour de Lusignan",
         "numberOfItems": len(DOMAINES),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@id": f"{SITE}{PAGES[d['slug']][0]}#lieu"}}
                             for i, d in enumerate(DOMAINES)]},
    ] + [biz(d) for d in DOMAINES]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)

def devis_form():
    return r'''
<section class="section" id="demande-devis" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow mark">Devis sur mesure</p>
    <h2>Demandez un devis <i>pour votre entreprise</i></h2>
    <p>Décrivez votre séminaire : je vous envoie un devis détaillé, adapté à votre nombre de participants, à la restauration et à l'hébergement souhaités.</p>
    <form id="devis-form" novalidate>
      <label>Entreprise<input name="Entreprise" autocomplete="organization" required></label>
      <label>Nom et prénom<input name="Contact" autocomplete="name" required></label>
      <label>E-mail<input name="E-mail" type="email" autocomplete="email" required></label>
      <label>Téléphone<input name="Téléphone" type="tel" autocomplete="tel"></label>
      <label>Date souhaitée<input name="Date souhaitée" type="date"></label>
      <label>Durée<select name="Durée"><option>Une journée</option><option>Une demi-journée</option><option>Deux jours</option><option>Trois jours ou plus</option><option>À définir</option></select></label>
      <label>Nombre de participants<input name="Participants" type="number" min="1" max="200" inputmode="numeric"></label>
      <label>Personnes à loger (nuitées)<input name="Personnes à loger" type="number" min="0" max="66" inputmode="numeric" placeholder="0 si pas d'hébergement"></label>
      <label class="full">Configuration de la salle<select name="Configuration"><option>Réunion en théâtre (rangs de chaises)</option><option>Tables en U</option><option>Salle de classe</option><option>Tables rondes (ateliers)</option><option>Cocktail debout</option><option>À définir ensemble</option></select></label>
      <fieldset class="mode full"><legend>Restauration souhaitée</legend>
        <label><input type="checkbox" name="Restauration" value="Accueil café et viennoiseries"> Accueil café</label>
        <label><input type="checkbox" name="Restauration" value="Pauses café"> Pauses café</label>
        <label><input type="checkbox" name="Restauration" value="Déjeuner"> Déjeuner</label>
        <label><input type="checkbox" name="Restauration" value="Dîner"> Dîner</label>
        <label><input type="checkbox" name="Restauration" value="Cocktail"> Cocktail</label>
        <label><input type="checkbox" name="Restauration" value="Petit-déjeuner (résidentiel)"> Petit-déjeuner</label>
      </fieldset>
      <label class="full">Traiteur<select name="Traiteur"><option>Je souhaite que vous me proposiez un traiteur</option><option>J'ai déjà mon traiteur</option><option>Pas de repas sur place</option></select></label>
      <fieldset class="mode full"><legend>Matériel</legend>
        <label><input type="checkbox" name="Matériel" value="Vidéoprojecteur"> Vidéoprojecteur</label>
        <label><input type="checkbox" name="Matériel" value="Écran TV"> Écran TV</label>
        <label><input type="checkbox" name="Matériel" value="Paperboard"> Paperboard</label>
        <label><input type="checkbox" name="Matériel" value="Wi-Fi"> Wi-Fi</label>
        <label><input type="checkbox" name="Matériel" value="Sonorisation / micro"> Sono, micro</label>
        <label><input type="checkbox" name="Matériel" value="Activité team building"> Team building</label>
      </fieldset>
      <label class="full">Précisions sur votre projet<textarea name="Précisions" rows="4" placeholder="Programme, horaires, régimes alimentaires, budget, autres besoins..."></textarea></label>
      <div class="full"><button class="btn btn--block" type="submit">Envoyer ma demande de devis</button></div>
      <p class="full formule">Le bouton ouvre votre messagerie avec votre demande déjà rédigée, adressée à <a href="mailto:contact@gitesvienne.fr">contact@gitesvienne.fr</a>. Il ne vous reste qu'à l'envoyer. Vous pouvez aussi appeler le 06 18 70 82 19.</p>
    </form>
  </div>
</section>
<script>
(function(){
  var f = document.getElementById("devis-form"); if (!f) return;
  f.addEventListener("submit", function(e){
    e.preventDefault();
    var req = f.querySelectorAll("[required]");
    for (var i = 0; i < req.length; i++) { if (!req[i].value.trim()) { req[i].focus(); req[i].reportValidity && req[i].reportValidity(); return; } }
    var d = {}, order = [];
    new FormData(f).forEach(function(v, k){ v = String(v).trim(); if (!v) return; if (!(k in d)) { d[k] = []; order.push(k); } d[k].push(v); });
    if (d["Date souhaitée"]) { var p = d["Date souhaitée"][0].split("-"); if (p.length === 3) d["Date souhaitée"] = [p[2] + "/" + p[1] + "/" + p[0]]; }
    var lignes = order.map(function(k){ return k + " : " + d[k].join(", "); });
    var corps = "Bonjour,\n\nVoici ma demande de devis pour un séminaire au Domaine de Persine.\n\n" + lignes.join("\n") + "\n\nMerci de me faire parvenir votre devis.\n";
    var sujet = "Demande de devis séminaire" + (d["Entreprise"] ? " - " + d["Entreprise"][0] : "");
    window.location.href = "mailto:contact@gitesvienne.fr?subject=" + encodeURIComponent(sujet) + "&body=" + encodeURIComponent(corps);
  });
})();
</script>'''

def theme_body(t):
    doms = {d["slug"]: d for d in DOMAINES}
    intro = "".join(f"<p>{E(x)}</p>" for x in t["intro"])
    pts = "".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a, b in t["points"])
    faq = "".join(f'<details class="faq__item"><summary>{E(q)}</summary><p>{E(r)}</p></details>' for q, r in t["faq"])
    others = "".join(f'<a class="btn btn--ghost" href="/{o["slug"]}/">{E(o["eyebrow"])}</a>' for o in THEMES if o["slug"] != t["slug"])
    cards = "".join(card(doms[s]) for s in t["domaines"])
    photos = "".join(f'<figure><button type="button" class="ph" data-full="/img/{s}.jpg" data-cap="{E(c)}"><img src="/img/{s}-s.jpg" alt="{E(c)}" loading="lazy"></button><figcaption>{E(c)}</figcaption></figure>' for s, c in t.get("photos", []))
    galerie = f'<section class="section" style="padding-top:0"><div class="wrap"><div class="galerie">{photos}</div></div></section>' if photos else ""
    cartes = f'''<section class="section section--{t['famille']}" style="padding-top:0">
  <div class="wrap">
    <div class="cards cards--3">{cards}</div>
  </div>
</section>''' if cards else ""
    devis = devis_form() if t.get("devis") else ""
    actions = ('<a class="btn" href="#demande-devis">Demander un devis</a><a class="btn btn--ghost" href="#contact" data-ask="persine" data-mode="visite">Demander une visite</a><a class="btn btn--ghost" href="tel:' + PHONE_INTL + '">Appeler</a><a class="btn btn--ghost" href="/plaquettes/plaquette-seminaire-domaine-de-persine.pdf" target="_blank" rel="noopener">Télécharger la plaquette</a>') if t.get("devis") else \
              '<a class="btn" href="/#disponibilites">Voir les dates libres</a><a class="btn btn--ghost" href="#contact" data-ask="" data-mode="visite">Demander une visite</a><a class="btn btn--ghost" href="#contact" data-ask="" data-mode="appel">Prendre rendez-vous téléphonique</a>'
    return f'''
<section class="section section--{t['famille']} theme">
  <div class="wrap">
    <p class="eyebrow mark">{E(t['eyebrow'])}</p>
    <h1 class="theme__h1">{t['h1']}</h1>
    <div class="theme__intro">{intro}</div>
    <ul class="theme__pts">{pts}</ul>
    <div class="actions">{actions}</div>
  </div>
</section>
{galerie}{cartes}{devis}
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

# ---------- Référencement IA : questions fréquentes par domaine, llms.txt, tarifs.md ----------
import datetime
MAJ = datetime.date.today()
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MAJ_TXT = f"{MAJ.day} {MOIS[MAJ.month - 1]} {MAJ.year}"

def nb(n):
    return f"{n:,}".replace(",", " ")

def faq_domaine(d):
    """Questions fréquentes construites uniquement à partir des données vérifiées (data.py)."""
    s, nom = SCHEMA[d["slug"]], d["nom"]
    order = [k for k in ["C", "B", "M", "H", "W"] if k in d["tarifs"]]
    lo, hi = d["tarifs"][order[0]], max(d["tarifs"].values())
    q = []
    if d["famille"] == "mariage":
        q.append((f"Combien d'invités peut-on recevoir au {nom} ?",
                  f"Le {nom} reçoit jusqu'à {s['convives']} convives assis pour le repas et {s['debout']} en cocktail debout, et dispose de {s['couchages']} couchages sur place{" (24 au château, le reste au gîte et dans les chalets, en option)" if d["slug"] == "borderie" else " : vos invités dorment au domaine tout le week-end"}."))
        q.append((f"Quel est le prix de location du {nom} pour un mariage ?",
                  f"La location démarre à {eur(lo)} {d['unite']} en {SAISON_NOM[order[0]].lower()} et va jusqu'à {eur(hi)} en haute saison ({d['periodes']['H'].lower()}). Formule : {d['formule'].lower()}. Le détail des saisons et des options figure dans le tableau des tarifs de cette page."))
        q.append((f"Peut-on choisir son traiteur au {nom} ?",
                  "Oui. Le domaine dispose d'une cuisine dédiée au traiteur de votre choix, et nous vous transmettons notre liste de prestataires sur demande."))
    else:
        q.append((f"Combien de personnes peut accueillir {nom} ?",
                  f"{nom} accueille {s['couchages']} personnes dans {s['chambres']} chambres, à Lusignan, dans la Vienne."))
        q.append((f"Quel est le prix d'un week-end à {nom} ?",
                  f"À partir de {eur(lo)} {d['unite']}, pour {d['periodes']['W'][len('Week-end, '):].lower()}. Le tarif est confirmé selon les dates et le nombre de personnes."))
        q.append(("La piscine est-elle chauffée ?", f"Oui, {nom} dispose d'une piscine chauffée."))
    q.append((f"Où se trouve {'le ' + nom if d['famille'] == 'mariage' else nom} ?", f"{d['adresse']}. Accès : {d['acces']}"))
    q.append(("Comment voir les dates libres ?",
              "Le calendrier de cette page se met à jour automatiquement depuis notre planning de réservation : les jours barrés sont déjà réservés. "
              f"Choisissez vos dates pour voir le tarif, puis envoyez votre demande ; vous pouvez aussi nous joindre au {PHONE}."))
    return q

def faq_html(d):
    items = "".join(f'<details class="faq__item"><summary>{E(a)}</summary><p>{E(b)}</p></details>' for a, b in faq_domaine(d))
    return f'''<div class="wrap faq__wrap fiche__faq">
    <h2>Questions fréquentes sur {"le " if d["famille"] == "mariage" else ""}{E(d["nom"])}</h2>
    {items}
    <p class="hint">Tarifs et informations mis à jour le {MAJ_TXT}. Disponibilités en temps réel.</p>
  </div>'''

def page_jsonld(d):
    url = f"{SITE}{PAGES[d['slug']][0]}"
    return json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": f"{url}#page", "url": url, "name": PAGES[d["slug"]][1], "description": PAGES[d["slug"]][2],
         "inLanguage": "fr-FR", "dateModified": MAJ.isoformat(), "isPartOf": {"@id": f"{SITE}/#website"},
         "about": {"@id": f"{url}#lieu"}, "author": {"@id": f"{SITE}/#julien-sabatier"}},
        {"@type": "Person", "@id": f"{SITE}/#julien-sabatier", "name": f"{CONSEILLER['prenom']} {CONSEILLER['nom']}",
         "jobTitle": CONSEILLER["role"], "image": f"{SITE}/{CONSEILLER['photo']}", "telephone": PHONE_INTL},
        biz(d),
        {"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faq_domaine(d)]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Gîtes Vienne", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": d["nom"], "item": url}]},
    ]}, ensure_ascii=False)

def tarifs_md():
    L = [f"# Tarifs : Gîtes Vienne (gitesvienne.fr)", "",
         f"Mis à jour le {MAJ_TXT}. Prix en euros TTC, location du lieu entier. Disponibilités en temps réel sur chaque page du site.",
         f"Réservation et visites : {CONSEILLER['prenom']} {CONSEILLER['nom']}, {PHONE}, {CONTACT_EMAIL}.", ""]
    for d in DOMAINES:
        s = SCHEMA[d["slug"]]
        L += [f"## {d['nom']} · {d['lieu']}", "",
              f"- Page : {SITE}{PAGES[d['slug']][0]}",
              f"- Type : {'domaine de mariage et de réception' if d['famille'] == 'mariage' else 'gîte de groupe'}",
              f"- Capacité : {s['couchages']} couchages" + (f", {s['convives']} convives assis, {s['debout']} debout" if s.get("convives") else ""),
              f"- Formule : {d['formule']}", ""]
        order = [k for k in ["H", "M", "B", "C", "W"] if k in d["tarifs"]]
        L += ["| Saison | Période | Prix |", "|---|---|---|"]
        L += [f"| {SAISON_NOM[k]} | {d['periodes'][k]} | {nb(d['tarifs'][k])} € {d['unite']} |" for k in order]
        if d["famille"] == "gite":
            L += ["", "Tarif « à partir de », confirmé selon les dates et le nombre de personnes."]
        if d["options"]:
            L += ["", "Options :"] + [f"- {a} : {b}" for a, b in d["options"]]
        if d["slug"] in PLAQUETTES:
            L += ["", f"Plaquette complète (PDF) : {SITE}/{PLAQUETTES[d['slug']]}"]
        L.append("")
    return "\n".join(L)

def llms_txt():
    L = ["# Gîtes Vienne", "",
         f"> Cinq lieux à louer en entier autour de Lusignan, dans la Vienne (86) et en Charente (16) : trois domaines de mariage privatisés (Domaine de Persine, Château de Montbeil, Château de la Borderie) et deux gîtes de groupe avec piscine chauffée (Le Clos de Mélior, La Villa d'Elinas), près de Poitiers et du Futuroscope. Calendriers de disponibilité en temps réel et tarifs publics.", "",
         f"Interlocuteur unique pour les cinq lieux : {CONSEILLER['prenom']} {CONSEILLER['nom']}, {PHONE}, {CONTACT_EMAIL}. Visites sur rendez-vous.",
         f"Informations mises à jour le {MAJ_TXT}.", "",
         "## Les domaines", ""]
    for d in DOMAINES:
        s = SCHEMA[d["slug"]]
        cap = f"{s['couchages']} couchages" + (f", {s['convives']} convives assis, {s['debout']} en cocktail debout" if s.get("convives") else "")
        av = AVIS.get(d["slug"])
        note = f", note Google {av['note']}/5 ({av['nb']} avis)" if av else ""
        L.append(f"- [{d['nom']}]({SITE}{PAGES[d['slug']][0]}): {d['lieu']}. {d['accroche']} {cap}. {s['prix']}{note}.")
    L += ["", "## Par besoin", ""]
    L += [f"- [{t['eyebrow']}]({SITE}/{t['slug']}/): {t['desc']}" for t in THEMES]
    L += ["", "## Informations pratiques", "",
          f"- [Tarifs détaillés de tous les domaines]({SITE}/tarifs.md): saisons, prix et options en texte simple",
          f"- [Calendrier des dates libres]({SITE}/#disponibilites): disponibilités des cinq lieux, mises à jour automatiquement",
          f"- [Avis clients]({SITE}/#avis): extraits des avis Google de chaque domaine",
          f"- [Demander une date ou une visite]({SITE}/#contact): formulaire, réponse avec la plaquette du domaine", "",
          "## Optional", ""]
    L += [f"- [Plaquette {d['nom']}]({SITE}/{PLAQUETTES[d['slug']]})" for d in DOMAINES if d["slug"] in PLAQUETTES]
    L += [f"- [Site historique {d['nom']}]({d['site']})" for d in DOMAINES]
    return "\n".join(L) + "\n"

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
          .replace("%%FAQ_HOME%%", "".join(f'<details class="faq__item"><summary>{E(q)}</summary><p>{E(r)}</p></details>' for q, r in FAQ_HOME))
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
        f = f.replace('<div class="wrap fiche__avis">', faq_html(d) + '\n  <div class="wrap fiche__avis">', 1)
        f = re.sub(r'href="#contact" data-ask="(\w+)" data-mode="(\w+)"', r'href="/?d=\1&amp;m=\2#contact" data-ask="\1" data-mode="\2"', f)
        f = re.sub(r'href="#contact" data-ask="(\w+)"', r'href="/?d=\1#contact" data-ask="\1"', f)
        page = common(tpl.replace("%%TITLE%%", E(ttl)))
        a, b = page.split("<!--HOME-->"); _, c = b.split("<!--/HOME-->")
        page = a + f + c
        page = page.replace("%%FICHES%%", "").replace("%%JSONLD%%", page_jsonld(d))
        page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', page, count=1)
        page = page.replace('<link rel="canonical" href="https://gitesvienne.fr/">', f'<link rel="canonical" href="https://gitesvienne.fr{url}">')
        page = page.replace('<meta property="og:url" content="https://gitesvienne.fr/">', f'<meta property="og:url" content="https://gitesvienne.fr{url}">')
        page = page.replace('content="https://gitesvienne.fr/img/borderie-card.jpg"', f'content="https://gitesvienne.fr/img/{d["slug"]}-card.jpg"')
        page = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(d["nom"])}">', page, count=1)
        # chemins absolus
        page = re.sub(r'(?<=[\s"(,])(img|plaquettes)/', r'/\1/', page)
        page = page.replace('fetch("ical.php"', 'fetch("/ical.php"').replace('fetch("contact.php"', 'fetch("/contact.php"').replace('fetch("rdv.php"', 'fetch("/rdv.php"')
        page = page.replace('href="#accueil"', 'href="/"').replace('href="#mariages"', 'href="/#mariages"').replace('href="#week-ends"', 'href="/#week-ends"').replace('href="#avis"', 'href="/#avis"').replace('href="#disponibilites"', 'href="/#disponibilites"').replace('href="#faq"', 'href="/#faq"')
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
        page = page.replace('fetch("ical.php"', 'fetch("/ical.php"').replace('fetch("contact.php"', 'fetch("/contact.php"').replace('fetch("rdv.php"', 'fetch("/rdv.php"')
        page = page.replace('href="#accueil"', 'href="/"').replace('href="#mariages"', 'href="/#mariages"').replace('href="#week-ends"', 'href="/#week-ends"').replace('href="#avis"', 'href="/#avis"').replace('href="#disponibilites"', 'href="/#disponibilites"').replace('href="#faq"', 'href="/#faq"')
        write(os.path.join(ROOT, t["slug"], "index.html"), wrap(page, "/img/favicon.png"))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
          '  <url><loc>https://gitesvienne.fr/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>']
    sm += [f'  <url><loc>https://gitesvienne.fr{PAGES[d["slug"]][0]}</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>' for d in DOMAINES]
    sm += [f'  <url><loc>https://gitesvienne.fr/{t["slug"]}/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>' for t in THEMES]
    sm += [f'  <url><loc>https://gitesvienne.fr/{p}</loc></url>' for p in PLAQUETTES.values()]
    sm.append('</urlset>')
    write(os.path.join(ROOT, "sitemap.xml"), "\n".join(sm) + "\n")
    write(os.path.join(ROOT, "llms.txt"), llms_txt())
    write(os.path.join(ROOT, "tarifs.md"), tarifs_md())
