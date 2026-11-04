# -*- coding: utf-8 -*-
"""Pages thématiques pour le référencement (une page par recherche visée).
Chaque page : titre Google, description, texte, domaines mis en avant, questions fréquentes.
Ne mettre ici que des faits vérifiés (repris de data.py)."""

THEMES = [
  {
    "slug": "gite-mariage-vienne",
    "famille": "mariage",
    "title": "Gîte et domaine de mariage dans la Vienne (86), près de Poitiers et Lusignan",
    "desc": "Domaines de mariage à louer dans la Vienne : Persine à Lusignan, Montbeil à Boivre-la-Vallée, la Borderie aux portes de la Vienne. 42 à 93 couchages, salle de réception, parc. Tarifs et dates libres.",
    "eyebrow": "Mariage dans la Vienne",
    "h1": "Gîte de mariage dans la Vienne : <i>trois domaines</i> pour recevoir tous vos invités",
    "intro": [
      "Vous cherchez un lieu de mariage dans la Vienne où vos invités peuvent aussi dormir sur place ? Nous proposons trois domaines privatisés pour le week-end, autour de Lusignan, au cœur du Pays Mélusin, à quelques minutes de Poitiers.",
      "Chaque domaine dispose d'une salle de réception, d'une cuisine pour votre traiteur et de nombreux couchages : de 42 couchages au Domaine de Persine jusqu'à 93 couchages au Château de la Borderie. Vous gardez le libre choix de vos prestataires, et nous vous transmettons notre liste sur demande.",
    ],
    "points": [
      ("Domaine de Persine, Lusignan", "Salle climatisée de 180 m² pour 150 convives assis, 42 couchages, parc clos d'un hectare, pas de droit de bouchon."),
      ("Château de Montbeil, Boivre-la-Vallée", "49 couchages, chalet de réception de 100 m² climatisé, kiosque pour cérémonie laïque, parc de 5 000 m²."),
      ("Château de la Borderie, Benest", "Aux portes de la Vienne, en Charente : 93 couchages, salle de 140 m², piscine et parc de 19 hectares."),
    ],
    "domaines": ["persine", "montbeil", "borderie"],
    "faq": [
      ("Combien d'invités peuvent dormir sur place ?", "De 42 couchages au Domaine de Persine à 49 au Château de Montbeil et 93 au Château de la Borderie. Pour un grand mariage à Lusignan, le Clos de Mélior (12 personnes) et la Villa d'Elinas (14 personnes), à deux minutes de Persine, complètent l'hébergement."),
      ("Peut-on choisir son traiteur ?", "Oui. Chaque domaine dispose d'une cuisine pour le traiteur de votre choix, et nous vous transmettons notre liste de prestataires sur demande."),
      ("Peut-on faire une cérémonie laïque sur place ?", "Oui : dans le parc arboré et clos de Persine, sous le kiosque de Montbeil ou dans le parc de 19 hectares de la Borderie."),
      ("Comment voir les dates libres et les tarifs ?", "Le calendrier de chaque domaine affiche les dates libres et le tarif de la saison. Vous pouvez aussi demander une visite : vous recevez aussitôt la plaquette du domaine par e-mail."),
    ],
  },
  {
    "slug": "gite-de-groupe-poitiers",
    "famille": "gite",
    "title": "Grand gîte de groupe près de Poitiers et du Futuroscope, avec piscine (Vienne)",
    "desc": "Gîtes de groupe à Lusignan, près de Poitiers et du Futuroscope : Villa d'Elinas (14 personnes) et Clos de Mélior (12 personnes) avec piscine chauffée, et grands domaines jusqu'à 93 couchages.",
    "eyebrow": "Gîte de groupe dans la Vienne",
    "h1": "Grand gîte de groupe <i>près de Poitiers</i> et du Futuroscope",
    "intro": [
      "Pour un week-end entre amis, des vacances en famille ou un séjour au Futuroscope, nos gîtes de groupe vous accueillent à Lusignan, dans le bourg médiéval, à quelques minutes de Poitiers.",
      "La Villa d'Elinas reçoit 14 personnes et le Clos de Mélior 12 personnes, tous deux avec piscine chauffée. Pour un groupe plus grand, les domaines de Persine (42 couchages), Montbeil (49 couchages) et la Borderie (93 couchages) se louent aussi en entier.",
    ],
    "points": [
      ("Villa d'Elinas, Lusignan", "14 personnes, 6 chambres, 4 salles de bain, piscine chauffée, billard, salle de fitness et jardin clos sans vis-à-vis."),
      ("Le Clos de Mélior, Lusignan", "12 personnes, 4 chambres, piscine chauffée, salon avec cheminée monumentale, terrasse et barbecue."),
      ("Pour les grands groupes", "Persine, Montbeil et la Borderie accueillent de 42 à 93 personnes, avec une grande salle pour les repas."),
    ],
    "domaines": ["elinas", "melior", "persine"],
    "faq": [
      ("Les deux gîtes sont-ils proches l'un de l'autre ?", "Oui : le Clos de Mélior et la Villa d'Elinas se trouvent à Lusignan, à deux minutes du Domaine de Persine. Vous pouvez les réserver ensemble pour 26 personnes."),
      ("La piscine est-elle chauffée ?", "Oui, au Clos de Mélior comme à la Villa d'Elinas."),
      ("Peut-on venir en train ?", "Oui : la gare de Lusignan est à quelques minutes des gîtes."),
      ("Comment réserver ?", "Choisissez vos dates dans le calendrier du gîte : vous voyez le tarif de la saison et vous envoyez votre demande en un clic. Je vous recontacte ensuite pour confirmer."),
    ],
  },
  {
    "slug": "seminaire-anniversaire-vienne",
    "famille": "gite",
    "title": "Lieu pour séminaire, anniversaire ou fête de famille dans la Vienne (86)",
    "desc": "Louez un domaine entier près de Poitiers pour un séminaire, un anniversaire ou une fête de famille : salle de réception, hébergement sur place de 12 à 93 personnes, cuisine pour traiteur.",
    "eyebrow": "Séminaires et fêtes de famille",
    "h1": "Séminaire, anniversaire, fête de famille : <i>un domaine rien que pour vous</i>",
    "intro": [
      "Un anniversaire, des retrouvailles de famille, un séminaire d'équipe ou un week-end de cohésion : nos cinq domaines autour de Lusignan se louent en entier, avec l'hébergement sur place pour tout le monde.",
      "Vous disposez d'une grande salle pour les repas et les réunions, d'une cuisine pour votre traiteur et d'espaces extérieurs pour vous détendre. Poitiers est à une vingtaine de minutes.",
    ],
    "points": [
      ("De 12 à 26 personnes", "Le Clos de Mélior et la Villa d'Elinas, avec piscine chauffée, à réserver seuls ou ensemble."),
      ("De 40 à 50 personnes", "Le Domaine de Persine (42 couchages, salle de 180 m²) ou le Château de Montbeil (49 couchages, chalet de 100 m²)."),
      ("Jusqu'à 93 personnes", "Le Château de la Borderie, son parc de 19 hectares, sa piscine et sa salle de réception de 140 m²."),
    ],
    "domaines": ["persine", "montbeil", "elinas"],
    "faq": [
      ("Peut-on louer un domaine en semaine ?", "Envoyez-moi vos dates : le calendrier de chaque domaine montre les jours libres, et je vous indique les conditions pour une location en semaine."),
      ("Y a-t-il une salle pour une réunion ou un repas de groupe ?", "Oui : 180 m² au Domaine de Persine, un chalet de 100 m² au Château de Montbeil et 140 m² au Château de la Borderie."),
      ("Peut-on venir visiter avant de réserver ?", "Oui, demandez une visite depuis le formulaire : vous recevez aussitôt la présentation du domaine par e-mail, puis je vous recontacte pour fixer un rendez-vous."),
    ],
  },
]
