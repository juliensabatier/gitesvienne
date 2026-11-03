# -*- coding: utf-8 -*-
"""Contenu du site gitesvienne.fr. Modifiez ce fichier puis relancez build.py."""

CONTACT_EMAIL = "contact@gitesvienne.fr"
PHONE = "06 18 70 82 19"
PHONE_INTL = "+33618708219"
SITE_URL = "https://gitesvienne.fr"

# Interlocuteur affiché en bas de chaque fiche et dans le contact.
# Déposez la photo dans img/julien-sabatier.jpg (format carré conseillé) : elle remplace les initiales automatiquement.
CONSEILLER = {"prenom": "Julien", "nom": "Sabatier", "photo": "img/julien-sabatier.jpg",
              "role": "Votre interlocuteur pour les cinq domaines",
              "texte": "Je vous fais visiter les domaines, je réponds à vos questions et je prépare votre devis."}

# Destination Google Maps pour le bouton « Itinéraire » (adresse ou nom du lieu)
MAPS = {
    "persine":  "Domaine de Persine, 3 rue de la Roche Grolleau, 86600 Lusignan",
    "montbeil": "Château de Montbeil, 9 lieu-dit Montbeil, 86470 Boivre-la-Vallée",
    "borderie": "Château de la Borderie, 16350 Benest",
    "melior":   "Le Clos de Mélior, 86600 Lusignan",
    "elinas":   "Villa Elinas, 86600 Lusignan",
}

# Avis Google (extraits relevés le 03/11/2026 sur les fiches Google de chaque domaine)
AVIS = {
  "persine": {"note": "4,9", "nb": 61, "cid": "15266615184325557735", "extraits": [
    ("Bilitis M.", "Mariage, mai 2026", "Un grand merci à Erwan pour son professionnalisme, sa gentillesse, ses précieux conseils et sa réactivité. Nous avons eu un immense coup de cœur pour ce domaine où nous nous sommes sentis immédiatement bien. Notre mariage y a été tout simplement incroyable et restera un souvenir inoubliable."),
    ("Jérôme G.", "Mariage, juin 2025", "Erwan et son équipe nous ont permis de réaliser le mariage de nos rêves en étant très flexibles et aux petits soins avec nous. Le domaine est sublime. La capacité de couchage est parfaite."),
    ("Ildiko D.", "Anniversaire, décembre 2025", "Nous avons loué le Domaine de Persine pour fêter l’anniversaire de mon conjoint et tout était absolument parfait ! Le lieu est magnifique, très bien entretenu et offre un cadre idyllique pour célébrer un événement spécial."),
  ]},
  "montbeil": {"note": "5,0", "nb": 71, "cid": "10603852060669505702", "extraits": [
    ("Claire P.", "Mariage, avril 2026", "Nous avons célébré notre mariage au château de Montbeil et tout était absolument parfait. Notre contact Erwan a toujours été à l’écoute et de bon conseil."),
    ("Axelle D.", "Mariage, juin 2026", "Nous avons célébré notre mariage dans ce domaine absolument magnifique, et le mot est faible. Dès l'arrivée, le charme opère. Chaque pièce possède sa propre atmosphère, ce qui a totalement subjugué nos invités."),
    ("Laëti B.", "Week-end en famille, avril 2026", "Week-end absolument magique au château de Montbeil ! Un moment inoubliable en famille."),
  ]},
  "borderie": {"note": "4,7", "nb": 106, "cid": "6121021280733075338", "extraits": [
    ("Clément S.", "Mariage, juillet 2026", "Magnifique domaine dans lequel on est assuré de passer un agréable séjour. Nous l'avons loué pour un week-end de mariage et tout s'est très bien passé, sans parler de la gentillesse et du professionnalisme avec lesquels Erwan a pu nous accompagner avant et pendant notre mariage. Je recommande à 100% !"),
    ("Manu M., photographe", "Mariage, septembre 2025", "J'ai eu la chance de photographier un mariage au Château de la Borderie : ce lieu est superbe ! Le château en lui-même et ses dépendances sont magnifiques, et que dire du parc avec la lumière incroyable qui y tombe en fin de journée...!!"),
    ("Françoise", "Fête de famille, décembre 2024", "Nous avons passé un super séjour au château les 21 et 22 décembre 2024 ; les 40 convives ont pu apprécié à sa juste valeur la qualité du site de réception et ses hébergements."),
  ]},
  "melior": {"note": "4,9", "nb": 27, "cid": "17475271891860752454", "extraits": [
    ("Sylvie F.", "Week-end en famille, novembre 2024", "A l'occasion d'un long week-end familial nous avons été totalement séduits par le gîte. Accueil remarquablement attentionné, une grande propreté et un équipement très complet. De plus le gîte est très bien situé dans un village charmant. Merci pour tout."),
    ("François C.", "Mai 2024", "Magnifique demeure très bien équipée. Grandes chambres avec dressing, très bonne literie et les lits sont déjà faits à votre arrivée ! Grandes salles de bain (baignoire et douche) avec serviettes fournies ! Lieu reposant et détente assurée ! Je recommande !"),
    ("Frédéric R.", "Vacances, août 2023", "Nous avons passé une semaine de vacances très reposante dans un gîte très fonctionnel, bien équipé et rénové avec goût. Parfait pour notre groupe de 12 personnes avec un jardin et piscine agréable qui offre une vue sur la vallée."),
  ]},
  "elinas": {"note": "4,9", "nb": 32, "cid": "18314508989955872147", "extraits": [
    ("Nadine B.", "Mai 2026", "Maison magnifique, très spacieuse, très bien décorée et au coeur du village. Erwan est au petit soin avec ses hotes et très reactif. Je recommande les yeux fermés"),
    ("Karine K.", "Week-end en famille, mai 2026", "Nous avons passé un long weekend en famille dans le gîte. Il est magnifique, les chambres sont très grandes, les équipements sont vraiment top! Le propriétaire est très arrangeant et disponible."),
    ("Léa P.", "Anniversaire, octobre 2024", "J'ai fêté mes 25 ans dans ce merveilleux gîte et nous avons passé un super week-end !"),
  ]},
}

PLAQUETTES = {
    "persine":  "plaquettes/plaquette-domaine-de-persine.pdf",
    "montbeil": "plaquettes/plaquette-chateau-de-montbeil.pdf",
    "borderie": "plaquettes/plaquette-chateau-de-la-borderie.pdf",
}

# Correspondance domaine -> identifiant du lien iCal Amenitiz.
# Attribution validée par Julien le 03/11/2026.
ICAL = {
    "persine":  "9c1706b6-09d9-4bfd-b23c-378d1f47b67d",
    "montbeil": "6c78fb44-5e4d-4f7f-8407-cd3e5474e7b4",
    "borderie": "283979e1-c327-4fa9-8138-e80e26b155df",
    "melior":   "2ea51c1a-5ac9-44fc-a307-28838fd3a6d9",
    "elinas":   "b491cb0c-c3e6-4185-98a6-0a85ec198341",
}

# Saisons : liste de (mois, jour_debut, jour_fin, code). Le premier qui correspond gagne.
# Codes : H haute, M moyenne, B basse, C creuse.
DOMAINES = [
  {
    "slug": "persine", "famille": "mariage",
    "nom": "Domaine de Persine", "court": "Persine",
    "lieu": "Lusignan (86)", "adresse": "3 rue de la Roche Grolleau, 86600 Lusignan",
    "site": "https://www.domainedepersine.fr",
    "accroche": "L'ancien bistrot du village, restauré dans un esprit chic et champêtre, avec son parc clos d'un hectare.",
    "chiffres": [("130", "convives assis"), ("40", "couchages"), ("180 m²", "salle climatisée"), ("1 ha", "parc clos")],
    "texte": [
      "Autrefois connu comme le bistrot du village de Lusignan, Persine renaît en 2010 avec une rénovation complète et l'extension de sa grande salle de réception.",
      "La salle de 180 m², climatisée et lumineuse, s'ouvre sur une terrasse ensoleillée de même surface. Elle reçoit jusqu'à 130 convives assis et 200 debout. Ses tons neutres, son parquet et ses poutres laissent toute la place à votre décoration.",
      "Le bar d'origine a été conservé : un coin bistrot pour le café du lendemain ou l'apéritif entre amis. Dans le parc arboré et entièrement clos, la pelouse plane et ombragée accueille les cérémonies laïques en plein air.",
    ],
    "atouts": ["Salle de 180 m² climatisée ouverte sur terrasse", "10 chambres, 40 couchages", "Chambre PMR et salle de bain adaptée au rez-de-chaussée",
               "Cuisine traiteur : chambre froide, piano de cuisson, lave-vaisselle", "Tables rondes, rectangulaires et chaises fournies",
               "Pas de droit de bouchon", "Parking privé dans l'enceinte", "Gare de Lusignan à 3 minutes"],
    "acces": "20 min de Poitiers, 25 min du Futuroscope, gare et aéroport de Poitiers à 25 min.",
    "saisons": [(12,16,31,"H"),(7,1,31,"H"),(8,1,31,"H"),(6,1,30,"M"),(9,1,30,"M"),(5,1,31,"B"),(10,1,31,"B")],
    "default_saison": "C",
    "tarifs": {"H": 3700, "M": 3500, "B": 3100, "C": 2700},
    "periodes": {"H": "Juillet, août et 2e quinzaine de décembre", "M": "Juin et septembre", "B": "Mai et octobre",
                 "C": "Novembre, 1re quinzaine de décembre, janvier à avril"},
    "formule": "Location du vendredi 18 h au dimanche 18 h",
    "options": [("Location prolongée (vendredi 10 h au lundi 11 h)", "350 €"), ("Clé dès le jeudi 18 h", "150 €"),
                ("Draps complets", "250 €"), ("Lits faits", "200 €"), ("Serviettes de toilette", "100 €")],
    "unite": "le week-end",
    "photos": [("persine-01","Le parc arboré et clos"),("persine-02","La salle de réception dressée"),("persine-03","Soirée dans la grande salle"),
               ("persine-04","Le bar bistrot d'origine"),("persine-05","Une chambre à l'étage"),("persine-06","Chambre lumineuse"),
               ("persine-07","Pelouse pour cérémonie laïque"),("persine-08","La cuisine traiteur")],
  },
  {
    "slug": "montbeil", "famille": "mariage",
    "nom": "Château de Montbeil", "court": "Montbeil",
    "lieu": "Boivre-la-Vallée (86)", "adresse": "9 lieu-dit Montbeil, 86470 Boivre-la-Vallée",
    "site": "https://www.chateaudemontbeil.com",
    "accroche": "Un ancien relais de chasse entièrement rénové en 2020, son escalier romantique et son parc à kiosque.",
    "chiffres": [("80", "convives assis"), ("49", "couchages"), ("750 m²", "habitables"), ("5 000 m²", "de parc")],
    "texte": [
      "Ancien relais de chasse d'un riche Poitevin devenu école rurale, Montbeil a été réinvesti en 2020 puis rénové pièce par pièce pour créer un lieu romantique et raffiné.",
      "Passé l'entrée, un salon cosy accueille vos proches avant la salle à manger aux lustres de cristal, qui reçoit jusqu'à 80 convives assis ou 120 debout. Le grand escalier tournant offre un décor rêvé pour les photos.",
      "Dans le parc, le kiosque en fer forgé se prête aux cérémonies laïques. Le chalet de 100 m², climatisé et accessible aux personnes à mobilité réduite, accueille le vin d'honneur et la soirée dansante sans déranger ceux qui dorment au château.",
    ],
    "atouts": ["11 chambres, 49 couchages", "4 salles de bain, dont une PMR au rez-de-chaussée", "Chalet de réception de 100 m² climatisé avec terrasse",
               "Kiosque pour cérémonie laïque", "Cuisine avec chambre froide et accès traiteur à l'arrière", "Petite salle dédiée aux enfants",
               "Liste de prestataires sur demande"],
    "acces": "25 min de Poitiers, 30 min du Futuroscope, 45 min de Niort.",
    "saisons": [(7,1,31,"H"),(8,1,31,"H"),(5,1,31,"M"),(6,1,30,"M"),(9,1,30,"M"),(4,1,30,"B"),(10,1,31,"B"),(12,17,31,"B")],
    "default_saison": "C",
    "tarifs": {"H": 3700, "M": 3500, "B": 3100, "C": 2700},
    "periodes": {"H": "Juillet et août", "M": "Mai, juin et septembre", "B": "Avril, octobre et 2e quinzaine de décembre",
                 "C": "Novembre, décembre jusqu'au 16, janvier à mars"},
    "formule": "Location du vendredi 18 h au dimanche 18 h",
    "options": [("Location prolongée (vendredi 10 h au lundi 10 h)", "350 €"), ("Clé dès le jeudi 18 h", "150 €"),
                ("Grande salle de réception, tout le week-end", "500 €"), ("Draps complets", "350 €"), ("Lits faits", "200 €"),
                ("Serviettes de toilette", "100 €")],
    "unite": "le week-end",
    "photos": [("montbeil-01","La façade et sa fontaine"),("montbeil-02","La salle à manger aux lustres"),("montbeil-03","Le hall d'entrée"),
               ("montbeil-04","Le grand escalier"),("montbeil-05","Le salon"),("montbeil-06","Cérémonie laïque dans le parc"),
               ("montbeil-07","L'escalier vu d'en haut"),("montbeil-08","Une chambre"),("montbeil-09","Salle de bain et sa baignoire"),
               ("montbeil-10","Chambre parentale")],
  },
  {
    "slug": "borderie", "famille": "mariage",
    "nom": "Château de la Borderie", "court": "La Borderie",
    "lieu": "Benest, Charente (16)", "adresse": "Château de la Borderie, 16350 Benest",
    "site": "https://www.chateaudelaborderie.com/fr/",
    "accroche": "Un château privatisé au cœur d'un parc de 19 hectares, avec sa piscine, son gîte et ses chalets.",
    "chiffres": [("120", "convives assis"), ("96", "couchages"), ("140 m²", "salle de réception"), ("19 ha", "de parc")],
    "texte": [
      "Racheté en 2010 puis entièrement rénové, le château de la Borderie se privatise pour un week-end ou un séjour prolongé, avec tous vos invités sur place.",
      "Derrière le hall, deux grands salons et deux salles à manger gardent leurs boiseries et leurs lustres. La salle de réception de 140 m², côté est, s'ouvre par de grandes baies sur la terrasse et le parc. La salle cocktail de 62 m² mène directement à la piscine.",
      "Le château offre 24 couchages dans 9 chambres. Le gîte voisin, avec son dortoir en box lumineux et son appartement familial, et deux chalets à l'orée du parc complètent l'hébergement jusqu'à 96 personnes.",
    ],
    "atouts": ["Château de 9 chambres, 24 couchages", "Gîte, appartement familial et 2 chalets : 96 couchages au total",
               "Salle de réception de 140 m² ouverte sur terrasse", "Salle cocktail de 62 m² côté piscine", "Piscine et parc de 19 hectares",
               "Cuisine dédiée au traiteur, attenante à la salle", "Chambres PMR au château et au gîte", "Liste de prestataires sur demande"],
    "acces": "Gare de Ruffec à 20 min, Angoulême à 50 min, Poitiers à 1 h 10.",
    "saisons": [(7,1,31,"H"),(8,1,31,"H"),(12,16,31,"H"),(5,1,31,"M"),(6,1,30,"M"),(9,1,30,"M"),(10,1,31,"M")],
    "default_saison": "C",
    "tarifs": {"H": 10780, "M": 8085, "C": 6380},
    "periodes": {"H": "Juillet, août et 2e quinzaine de décembre", "M": "Mai, juin, septembre et octobre",
                 "C": "Novembre, 1re quinzaine de décembre, janvier à avril"},
    "formule": "2 nuits au château (24 couchages)",
    "options": [("Nuit supplémentaire : saison creuse", "700 €"), ("Nuit supplémentaire : moyenne saison", "900 €"),
                ("Nuit supplémentaire : haute saison", "1 000 €"), ("Option gîte et chalets", "1 820 €")],
    "unite": "les 2 nuits",
    "photos": [("borderie-01","Le château dans son parc, vu du ciel"),("borderie-13","La piscine au pied du château"),("borderie-14","Première danse dans la salle de réception"),("borderie-15","Table dressée dans la salle de réception"),("borderie-02","La façade côté jardin"),("borderie-03","Le grand salon"),
               ("borderie-04","La petite salle à manger"),("borderie-05","Le salon boisé"),("borderie-06","Le hall et son escalier"),
               ("borderie-07","Une chambre du château"),("borderie-08","Le gîte"),("borderie-09","Les chalets à l'orée du parc"),
               ("borderie-10","La cuisine traiteur"),("borderie-11","L'allée de tilleuls"),("borderie-12","L'arrivée au château")],
  },
  {
    "slug": "melior", "famille": "gite",
    "nom": "Le Clos de Mélior", "court": "Mélior",
    "lieu": "Lusignan (86)", "adresse": "Bourg médiéval de Lusignan, 86600",
    "site": "https://larenaissancemelusine.systeme.io/contact-melior",
    "accroche": "Une demeure du XVe siècle sur les hauteurs de Lusignan, sa grande cheminée et sa piscine chauffée.",
    "chiffres": [("12", "couchages"), ("4", "chambres"), ("chauffée", "piscine"), ("20 min", "du Futuroscope")],
    "texte": [
      "Au Clos de Mélior, les poutres, les murs de pierre et la cheminée monumentale du salon rappellent l'âge de la maison, restaurée avec soin et équipée de tout le confort moderne.",
      "La cuisine ouverte et sa grande table réunissent tout le monde. Dehors, la terrasse en bois et la piscine chauffée regardent le village médiéval de Lusignan.",
      "Le gîte est un bon point de départ pour le Futuroscope, la Vallée des Singes, le Marais poitevin ou le site gallo-romain de Sanxay.",
    ],
    "atouts": ["Piscine chauffée", "Salon avec cheminée monumentale", "Cuisine moderne entièrement équipée", "Terrasse en bois et barbecue",
               "Chambre familiale avec lits superposés"],
    "acces": "Futuroscope 20 min, Poitiers 15 min, Vallée des Singes 20 min, Sanxay 15 min, Marais poitevin 30 min.",
    "saisons": [], "default_saison": "W",
    "tarifs": {"W": 600},
    "periodes": {"W": "Week-end, 2 nuits minimum"},
    "formule": "2 nuits minimum, location surtout le week-end",
    "options": [],
    "unite": "le week-end",
    "photos": [("melior-01","Le salon et sa cheminée en pierre"),("melior-02","La cuisine et la grande table"),("melior-03","Chambre à la cheminée"),
               ("melior-04","Chambre sous les poutres"),("melior-05","Chambre familiale"),("melior-06","L'escalier de pierre")],
  },
  {
    "slug": "elinas", "famille": "gite",
    "nom": "La Villa d'Elinas", "court": "Elinas",
    "lieu": "Lusignan (86)", "adresse": "Hauteurs de Lusignan, 86600",
    "site": "https://elinasvilla.systeme.io/contact",
    "accroche": "Une grande maison de famille avec piscine chauffée, billard, baby-foot et salle de fitness.",
    "chiffres": [("14", "couchages"), ("6", "chambres"), ("4", "salles de bain"), ("chauffée", "piscine")],
    "texte": [
      "La Villa d'Elinas est faite pour les retrouvailles : un billard et un piano dans le grand salon, un baby-foot pour les enfants, une salle de fitness et une salle de yoga, deux salons télé.",
      "Parquet ancien et pierres apparentes d'un côté, cuisine entièrement équipée de l'autre. Les 6 chambres décorées et les 4 salles de bain accueillent 14 personnes.",
      "Le jardin clos et sans vis-à-vis, la terrasse en bois et la piscine chauffée profitent de la vue sur la vallée et le viaduc de Lusignan.",
    ],
    "atouts": ["Piscine chauffée", "Billard, baby-foot et piano", "Salle de fitness et salle de yoga", "Deux salons télé",
               "Jardin clos sans vis-à-vis", "Terrasse en bois et barbecue"],
    "acces": "Futuroscope 20 min, Poitiers 15 min, Vallée des Singes 20 min, Sanxay 15 min, Marais poitevin 30 min.",
    "saisons": [], "default_saison": "W",
    "tarifs": {"W": 800},
    "periodes": {"W": "Week-end, 2 nuits minimum"},
    "formule": "2 nuits minimum, location surtout le week-end",
    "options": [],
    "unite": "le week-end",
    "photos": [("elinas-01","Cuisine ouverte et salle à manger"),("elinas-02","Le salon, son billard et son piano"),("elinas-03","Vue sur le viaduc de Lusignan"),
               ("elinas-04","La chambre violette"),("elinas-05","Chambre sous les poutres"),("elinas-06","Chambre à la girafe"),
               ("elinas-07","La salle de fitness"),("elinas-08","Le baby-foot"),("elinas-09","Salle de bain avec douche et baignoire")],
  },
]

SAISON_NOM = {"H": "Haute saison", "M": "Moyenne saison", "B": "Basse saison", "C": "Saison creuse", "W": "Week-end"}

# Instantané des iCal relevé le 2 novembre 2026 (sert de secours si ical.php ne répond pas).
SNAPSHOT_DATE = "2026-11-02"
SNAPSHOT = {
 "9c1706b6-09d9-4bfd-b23c-378d1f47b67d": "20261106-20261109 20261114-20261130 20261231-20270104 20270122-20270125 20270409-20270413 20270416-20270420 20270505-20270510 20270521-20270525 20270528-20270601 20270604-20270608 20270611-20270615 20270618-20270622 20270625-20270629 20270702-20270706 20270709-20270713 20270716-20270720 20270723-20270727 20270730-20270803 20270820-20270824 20270827-20270831 20270903-20270907 20270917-20270921 20270924-20270928 20271022-20271024 20280513-20280515 20280519-20280523 20280526-20280530 20280623-20280627 20280630-20280703 20280707-20280711 20281021-20281023",
 "6c78fb44-5e4d-4f7f-8407-cd3e5474e7b4": "20261231-20270105 20270305-20270309 20270409-20270413 20270416-20270420 20270423-20270427 20270505-20270510 20270514-20270518 20270521-20270525 20270528-20270601 20270604-20270608 20270612-20270614 20270618-20270622 20270626-20270628 20271111-20271116 20271203-20271207 20280415-20280417 20280428-20280501 20280524-20280529 20280630-20280704 20280902-20280904",
 "283979e1-c327-4fa9-8138-e80e26b155df": "20261224-20261229 20270423-20270426 20270506-20270511 20270513-20270518 20270603-20270608 20270610-20270614 20270618-20270621 20270623-20270708 20270709-20270713 20270717-20270720 20270729-20270806 20270812-20270826 20270903-20270907 20270924-20270927 20280602-20280605 20280630-20280704",
 "2ea51c1a-5ac9-44fc-a307-28838fd3a6d9": "20261205-20261207 20261225-20261228 20261230-20270103 20270122-20270124 20270326-20270330 20270515-20270518 20270528-20270531 20270611-20270614 20270918-20270920 20271022-20271024",
 "b491cb0c-c3e6-4185-98a6-0a85ec198341": "20261127-20261130 20261204-20261207 20261219-20261222 20261224-20261228 20261230-20270104 20270108-20270111 20270115-20270118 20270122-20270125 20270205-20270208 20270326-20270330 20270402-20270405 20270416-20270419 20270505-20270510 20270515-20270518 20270528-20270531 20270723-20270726 20270910-20270913 20271021-20271025",
}
