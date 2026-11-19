<?php
/**
 * gitesvienne.fr : formulaire de contact.
 * 1. envoie la demande à contact@gitesvienne.fr
 * 2. envoie automatiquement au visiteur un e-mail de présentation du domaine avec le lien vers la plaquette
 * L'adresse d'expédition doit appartenir au domaine (contact@gitesvienne.fr) pour ne pas tomber en spam.
 */
header('Content-Type: application/json; charset=utf-8');

$DEST     = 'contact@gitesvienne.fr';
$FROM     = 'contact@gitesvienne.fr';
$SITE     = 'https://gitesvienne.fr';
$SIGNATURE = "Julien Sabatier\nGîtes Vienne, domaines et gîtes autour de Lusignan\ncontact@gitesvienne.fr · 06 18 70 82 19\nhttps://gitesvienne.fr";

// Réponse automatique : true = envoyée, false = désactivée
$AUTO_VISITE = true;   // demandes de visite
$AUTO_DATE   = true;   // demandes de date

$DOMAINES = [
  'persine'  => ['nom' => 'Domaine de Persine', 'le' => 'au Domaine de Persine', 'plaquette' => 'plaquettes/plaquette-domaine-de-persine.pdf',
                 'pitch' => "Ancien bistrot du village de Lusignan restauré dans un esprit chic et champêtre, le domaine dispose d'une salle de réception climatisée de 180 m² ouverte sur une grande terrasse, de 42 couchages et d'un parc clos d'un hectare."],
  'montbeil' => ['nom' => 'Château de Montbeil', 'le' => 'au Château de Montbeil', 'plaquette' => 'plaquettes/plaquette-chateau-de-montbeil.pdf',
                 'pitch' => "Ancien relais de chasse entièrement rénové en 2020, le château offre 49 couchages, une salle à manger de réception, un chalet de 100 m² pour la soirée et un parc avec kiosque pour votre cérémonie laïque."],
  'borderie' => ['nom' => 'Château de la Borderie', 'le' => 'au Château de la Borderie', 'plaquette' => 'plaquettes/plaquette-chateau-de-la-borderie.pdf',
                 'pitch' => "Privatisé au cœur d'un parc de 19 hectares, le château accueille jusqu'à 93 personnes entre le château, le gîte et les chalets, avec une salle de réception de 140 m² ouverte sur le parc et une piscine."],
  'melior'   => ['nom' => 'Le Clos de Mélior', 'le' => 'au Clos de Mélior', 'plaquette' => '',
                 'pitch' => "Demeure de caractère sur les hauteurs de Lusignan, le Clos de Mélior accueille 12 personnes, avec sa grande cheminée, sa cuisine équipée et sa piscine chauffée."],
  'elinas'   => ['nom' => "La Villa d'Elinas", 'le' => "à la Villa d'Elinas", 'plaquette' => '',
                 'pitch' => "Grande maison de famille à Lusignan, la Villa d'Elinas accueille 14 personnes, avec piscine chauffée, billard, baby-foot et salle de fitness."],
];

/* Page de chaque domaine (calendrier à jour + tarifs) */
$PAGES = ['persine' => 'domaine-de-persine/', 'montbeil' => 'chateau-de-montbeil/', 'borderie' => 'chateau-de-la-borderie/',
          'melior' => 'clos-de-melior/', 'elinas' => 'villa-elinas/'];

function fail($msg, $code = 400) { http_response_code($code); echo json_encode(['ok' => false, 'error' => $msg]); exit; }
function clean($k, $max = 200) { return trim(mb_substr(str_replace(["\r", "\n"], ' ', (string)($_POST[$k] ?? '')), 0, $max)); }
function journal($t) { @file_put_contents(__DIR__ . '/cache/contact.log', date('Y-m-d H:i:s') . " $t\n", FILE_APPEND | LOCK_EX); }
function enc($s) { return '=?UTF-8?B?' . base64_encode($s) . '?='; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('Méthode non autorisée', 405);
if (!empty($_POST['site'])) { echo json_encode(['ok' => true]); exit; } // piège à robots

// Limite : 5 envois par heure et par adresse IP
$dir = __DIR__ . '/cache'; if (!is_dir($dir)) @mkdir($dir, 0755, true);
$f = $dir . '/rl_' . md5($_SERVER['REMOTE_ADDR'] ?? '') . '.txt';
$hits = is_file($f) ? array_filter(explode(',', file_get_contents($f)), function ($t) { return $t > time() - 3600; }) : [];
if (count($hits) >= 5) fail('Trop de demandes, merci de réessayer plus tard.', 429);
$hits[] = time(); @file_put_contents($f, implode(',', $hits));

$objet = in_array(clean('objet', 10), ['visite', 'appel'], true) ? clean('objet', 10) : 'date';
$nom = clean('nom'); $email = clean('email'); $tel = clean('tel', 40);
$dom = clean('domaine', 20); $type = clean('type', 40);
$arr = clean('arrivee', 10); $dep = clean('depart', 10);
$vdate = clean('visite_date', 10); $vmom = clean('visite_moment', 30);
$nb = clean('invites', 6); $couch = clean('couchages', 6);
$message = trim(mb_substr((string)($_POST['message'] ?? ''), 0, 4000));

if ($nom === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) fail('Nom ou e-mail manquant.');

$fr = function ($d) { return preg_match('/^\d{4}-\d{2}-\d{2}$/', $d) ? date('d/m/Y', strtotime($d)) : ''; };
$D = $DOMAINES[$dom] ?? null;
$domNom = $D ? $D['nom'] : 'Non précisé';

/* ---------- Rendez-vous téléphonique de 15 minutes ---------- */
if ($objet === 'appel') {
    date_default_timezone_set('Europe/Paris');
    $rd = clean('rdv_date', 10); $rh = clean('rdv_heure', 5);
    if ($tel === '') fail('Merci d\'indiquer votre numéro de téléphone.');
    if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $rd) || !preg_match('/^(\d{2}):(00|15|30|45)$/', $rh, $hm)) fail('Merci de choisir le jour et l\'heure du rendez-vous.');
    $h = (int)$hm[1];
    if ($h < 9 || $h > 19) fail('Les rendez-vous sont possibles de 9 h à 20 h.');
    $t = strtotime("$rd $rh:00");
    if ($t === false || $t < time() + 30 * 60 || $t > time() + 62 * 86400) fail('Ce créneau n\'est plus disponible, merci d\'en choisir un autre.');
    $slot = "$rd $rh";
    // Enregistrement du créneau (verrou pour éviter deux réservations simultanées)
    $rf = $dir . '/rdv.json';
    $fh = fopen($rf, 'c+');
    if (!$fh) fail("L'envoi a échoué.", 500);
    flock($fh, LOCK_EX);
    $all = json_decode(stream_get_contents($fh), true) ?: [];
    if (isset($all[$slot])) { flock($fh, LOCK_UN); fclose($fh); fail('Ce créneau vient d\'être réservé, merci d\'en choisir un autre.', 409); }
    $lim = date('Y-m-d H:i', time() - 7 * 86400);
    foreach ($all as $k => $v) if ($k < $lim) unset($all[$k]);
    $all[$slot] = ['nom' => $nom, 'tel' => $tel, 'email' => $email, 'le' => date('Y-m-d H:i')];
    ksort($all);
    ftruncate($fh, 0); rewind($fh); fwrite($fh, json_encode($all, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
    fflush($fh); flock($fh, LOCK_UN); fclose($fh);

    $JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
    $MOIS = ['', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
    $quand = $JOURS[(int)date('w', $t)] . ' ' . (int)date('j', $t) . ' ' . $MOIS[(int)date('n', $t)] . ' à ' . str_replace(':', ' h ', $rh);
    $fin = $t + 15 * 60;
    $gcal = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
          . '&text=' . rawurlencode("Appel $nom ($tel)")
          . '&dates=' . date('Ymd\THis', $t) . '/' . date('Ymd\THis', $fin) . '&ctz=Europe/Paris'
          . '&details=' . rawurlencode("Rendez-vous téléphonique pris sur gitesvienne.fr\nDomaine : $domNom\nType : $type\nTéléphone : $tel\nE-mail : $email" . ($message ? "\n\nMessage : $message" : ''));
    $body = "Nouveau rendez-vous téléphonique pris sur gitesvienne.fr\n\n"
          . "QUAND : " . ucfirst($quand) . " (15 minutes)\nAPPELER : $nom au $tel\n\n"
          . "Ajouter à mon agenda (Google Agenda) :\n$gcal\n\n"
          . "Domaine : $domNom\nType : $type\nDate de l'événement : " . ($fr($arr) ?: '-') . ($fr($dep) ? ' au ' . $fr($dep) : '') . "\n"
          . "Invités : " . ($nb ?: '-') . "\nCouchages : " . ($couch ?: '-') . "\n\nE-mail : $email\n\nMessage :\n" . ($message ?: '-') . "\n\n"
          . "Si ce créneau ne vous convient pas, rappelez le client pour en proposer un autre.\n"
          . "(Une confirmation a été envoyée automatiquement au client.)\n";
    $sujet = "RDV téléphonique " . date('d/m', $t) . " à " . str_replace(':', 'h', $rh) . " - $nom";

    // 1. Notification à Julien : Brevo via Make (sans présentation automatique), secours par le serveur
    $okMake = false;
    if (function_exists('curl_init')) {
        $ch = curl_init('https://hook.eu1.make.com/mirb58ifkyinqffw2iarovve3gcv83ad');
        curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 10,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_POSTFIELDS => json_encode(['cle' => 'gv-7Rk2pQx9', 'objet' => 'appel', 'domaine' => $dom, 'nom' => $nom, 'email' => $email,
                                               'notif_sujet' => $sujet, 'notif_texte' => $body, 'presentation' => 'non'])]);
        curl_exec($ch);
        $okMake = curl_getinfo($ch, CURLINFO_HTTP_CODE) === 200;
        curl_close($ch);
    }
    if (!$okMake) {
        $headers = "From: " . enc('Gîtes Vienne') . " <$FROM>\r\nReply-To: " . enc($nom) . " <$email>\r\nMIME-Version: 1.0\r\n"
                 . "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n";
        $okMake = @mail($DEST, enc($sujet), quoted_printable_encode($body), $headers, '-f' . $FROM);
    }
    journal("appel $slot $email : " . ($okMake ? 'ok' : 'ECHEC'));

    // 2. Confirmation au client
    $corps = "Bonjour $nom,\n\nVotre rendez-vous téléphonique est bien noté : je vous appellerai le $quand, au $tel, "
           . "pour un échange d'environ 15 minutes sur votre projet.\n\n"
           . "Si cet horaire ne m'était finalement pas possible, je vous rappellerai pour vous proposer un autre créneau. "
           . "Vous pouvez aussi répondre à ce message pour le modifier.\n\n"
           . "En attendant, les photos, les tarifs et les dates libres de nos domaines sont sur notre site :\n$SITE/" . ($PAGES[$dom] ?? '') . "\n\n"
           . "À très bientôt,\n\n" . $SIGNATURE . "\n";
    $hC = "From: " . enc('Julien Sabatier, Gîtes Vienne') . " <$FROM>\r\nReply-To: $FROM\r\nAuto-Submitted: auto-replied\r\nMIME-Version: 1.0\r\n"
        . "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n";
    $ok2 = @mail($email, enc("Votre rendez-vous téléphonique du " . date('d/m', $t) . " à " . str_replace(':', ' h ', $rh)), quoted_printable_encode($corps), $hC, '-f' . $FROM);
    journal("confirmation appel -> $email : " . ($ok2 ? 'ok' : 'ECHEC'));

    echo json_encode(['ok' => true]); exit;
}

/* ---------- 1. Message pour vous ---------- */
$lignes = ($objet === 'visite')
  ? "DEMANDE DE VISITE\nJour souhaité : " . ($fr($vdate) ?: '-') . ($vmom ? " ($vmom)" : '') . "\nDate de l'événement : " . ($fr($arr) ?: '-') . ($fr($dep) ? ' au ' . $fr($dep) : '') . "\n"
  : "DEMANDE DE DATE\nArrivée : " . ($fr($arr) ?: '-') . "\nDépart : " . ($fr($dep) ?: '-') . "\n";
/* Lien WhatsApp avec un premier message déjà rédigé (mobiles uniquement) */
$wa = '';
$td = preg_replace('/\D/', '', $tel);
if (preg_match('/^0([67]\d{8})$/', $td, $m)) $wa = '33' . $m[1];
elseif (preg_match('/^(?:00)?(33[67]\d{8})$/', $td, $m)) $wa = $m[1];
elseif (preg_match('/^\s*(?:\+|00)/', $tel) && preg_match('/^(?:00)?([1-9]\d{8,14})$/', $td, $m) && strpos($m[1], '33') !== 0) $wa = $m[1];
$waTexte = '';
if ($wa) {
    $waMsg = "Bonjour $nom, je suis Julien Sabatier, Gîtes Vienne. Merci pour votre demande " . ($objet === 'visite' ? 'de visite ' : '')
           . "concernant " . ($D ? $D['nom'] : 'nos domaines') . " sur gitesvienne.fr, je viens de vous envoyer notre présentation par e-mail.\n\n"
           . "Nos disponibilités à jour et nos tarifs :\n$SITE/" . ($PAGES[$dom] ?? '') . "\n\n"
           . "Je reste disponible ici pour toute question, pour vérifier vos dates ou organiser une visite.";
    $waTexte = "RÉPONDRE SUR WHATSAPP (message déjà rédigé, à relire puis envoyer) :\nhttps://wa.me/$wa?text=" . rawurlencode($waMsg) . "\n\n";
}
$body = "Nouvelle demande depuis gitesvienne.fr\n\n$waTexte" . "Domaine : $domNom\nType : $type\n$lignes"
      . "Invités : " . ($nb ?: '-') . "\nCouchages : " . ($couch ?: '-') . "\n\n"
      . "Nom : $nom\nE-mail : $email\nTéléphone : " . ($tel ?: '-') . "\n\nMessage :\n" . ($message ?: '-') . "\n\n"
      . (($objet === 'visite' ? $AUTO_VISITE : $AUTO_DATE) ? "(Un e-mail de présentation a été envoyé automatiquement au client.)\n" : '');
$sujet = ($objet === 'visite' ? 'Visite' : 'Demande') . " $domNom" . ($objet === 'date' && $arr ? ' du ' . $fr($arr) : '') . " - $nom";
/* ---------- Envoi principal : Brevo via Make (domaine authentifié, e-mails signés) ---------- */
$auto = ($objet === 'visite') ? $AUTO_VISITE : $AUTO_DATE;
$payload = ['cle' => 'gv-7Rk2pQx9', 'objet' => $objet, 'domaine' => $dom, 'nom' => $nom, 'email' => $email,
            'notif_sujet' => $sujet, 'notif_texte' => $body, 'presentation' => $auto ? 'oui' : 'non'];
$okMake = false;
if (function_exists('curl_init')) {
    $ch = curl_init('https://hook.eu1.make.com/mirb58ifkyinqffw2iarovve3gcv83ad');
    curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 10,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'], CURLOPT_POSTFIELDS => json_encode($payload)]);
    curl_exec($ch);
    $okMake = curl_getinfo($ch, CURLINFO_HTTP_CODE) === 200;
    curl_close($ch);
}
journal("make $objet $dom $email : " . ($okMake ? 'ok' : 'ECHEC, envoi direct'));
if ($okMake) { echo json_encode(['ok' => true]); exit; }

/* ---------- Secours : envoi direct par le serveur ---------- */
$headers = "From: " . enc('Gîtes Vienne') . " <$FROM>\r\nReply-To: " . enc($nom) . " <$email>\r\nMIME-Version: 1.0\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n";
$ok1 = @mail($DEST, enc($sujet), quoted_printable_encode($body), $headers, '-f' . $FROM);
journal("demande $objet $dom -> $DEST : " . ($ok1 ? 'ok' : 'ECHEC'));
if (!$ok1) fail("L'envoi a échoué.", 500);

/* ---------- 2. Présentation envoyée au visiteur ---------- */
if (($objet === 'visite' && $AUTO_VISITE) || ($objet === 'date' && $AUTO_DATE)) {
    $lieu = $D ? $D['le'] : 'à nos domaines';
    $pres = $D ? $D['pitch'] . "\n\n" : '';
    $plaq = ($D && $D['plaquette']) ? "Vous trouverez la plaquette complète du domaine (espaces, chambres, tarifs et prestataires) à cette adresse :\n$SITE/" . $D['plaquette'] . "\n\n"
          : "Vous pouvez retrouver les photos, les tarifs et les disponibilités sur notre site :\n$SITE/" . ($dom ? "#$dom" : '') . "\n\n";
    if ($objet === 'visite') {
        $quand = $fr($vdate) ? ' le ' . $fr($vdate) . ($vmom && $vmom !== 'Peu importe' ? ' (' . mb_strtolower($vmom) . ')' : '') : '';
        $corps = "Bonjour $nom,\n\nNous vous remercions de l'intérêt que vous portez $lieu et de votre souhait de le visiter.\n\n"
               . $pres . $plaq
               . "Je reviens vers vous très rapidement pour convenir ensemble d'un rendez-vous" . ($quand ? ", si possible$quand" : '') . ". "
               . "Vous pouvez dès à présent répondre à ce message pour m'indiquer vos disponibilités.\n\n"
               . "Dans l'attente de vous accueillir, je vous prie d'agréer mes salutations distinguées.\n\n";
        $sujetC = "Votre visite " . ($D ? $D['le'] : 'de nos domaines');
    } else {
        $periode = $fr($arr) ? ' du ' . $fr($arr) . ($fr($dep) ? ' au ' . $fr($dep) : '') : '';
        $corps = "Bonjour $nom,\n\nNous avons bien reçu votre demande$periode et vous remercions de l'intérêt que vous portez $lieu.\n\n"
               . $pres . $plaq
               . "Je vérifie la disponibilité et je reviens vers vous très rapidement avec une proposition. "
               . ($D && $dom !== 'melior' && $dom !== 'elinas' ? "Une visite du domaine est également possible sur rendez-vous : il vous suffit de répondre à ce message.\n\n" : "\n\n")
               . "Je vous prie d'agréer mes salutations distinguées.\n\n";
        $sujetC = "Votre demande " . ($D ? $D['le'] : 'à nos domaines');
    }
    $corps .= $SIGNATURE . "\n";
    $hC = "From: " . enc('Julien Sabatier, Gîtes Vienne') . " <$FROM>\r\nReply-To: $FROM\r\nAuto-Submitted: auto-replied\r\nMIME-Version: 1.0\r\n"
        . "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n";
    $ok2 = @mail($email, enc($sujetC), quoted_printable_encode($corps), $hC, '-f' . $FROM);
    journal("presentation -> $email : " . ($ok2 ? 'ok' : 'ECHEC'));
}

echo json_encode(['ok' => true]);
