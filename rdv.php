<?php
/**
 * gitesvienne.fr : créneaux de rendez-vous téléphonique déjà réservés.
 * Les rendez-vous sont enregistrés par contact.php dans cache/rdv.json.
 * Renvoie uniquement les créneaux à venir, sans aucune donnée personnelle.
 */
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
date_default_timezone_set('Europe/Paris');

$f = __DIR__ . '/cache/rdv.json';
$all = is_file($f) ? (json_decode(@file_get_contents($f), true) ?: []) : [];
$now = date('Y-m-d H:i');
$taken = [];
foreach ($all as $slot => $info) {
    if ($slot >= $now) $taken[] = $slot;
}
sort($taken);
echo json_encode(['taken' => $taken]);
