<?php
/**
 * gitesvienne.fr : lit les calendriers iCal Amenitiz et renvoie les dates réservées en JSON.
 * Cache d'une heure dans le dossier cache/ pour ne pas interroger Amenitiz à chaque visite.
 * Pour changer un lien : modifiez seulement le tableau $ICAL ci-dessous.
 */
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=600');

$BASE = 'https://renaissancemelusine.amenitiz.io/ical-room/';
$ICAL = [
    'persine'  => '9c1706b6-09d9-4bfd-b23c-378d1f47b67d',
    'montbeil' => '6c78fb44-5e4d-4f7f-8407-cd3e5474e7b4',
    'borderie' => '283979e1-c327-4fa9-8138-e80e26b155df',
    'melior'   => '2ea51c1a-5ac9-44fc-a307-28838fd3a6d9',
    'elinas'   => 'b491cb0c-c3e6-4185-98a6-0a85ec198341',
];
$TTL = 3600;
$cacheDir = __DIR__ . '/cache';
if (!is_dir($cacheDir)) @mkdir($cacheDir, 0755, true);
$cacheFile = $cacheDir . '/ical.json';

if (is_file($cacheFile) && (time() - filemtime($cacheFile)) < $TTL) {
    readfile($cacheFile);
    exit;
}

function fetch_url($url) {
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_TIMEOUT => 10, CURLOPT_USERAGENT => 'gitesvienne.fr calendrier']);
        $body = curl_exec($ch);
        $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        return ($code === 200 && $body) ? $body : false;
    }
    $ctx = stream_context_create(['http' => ['timeout' => 10, 'user_agent' => 'gitesvienne.fr calendrier']]);
    return @file_get_contents($url, false, $ctx);
}

function parse_ics($ics) {
    $ics = preg_replace("/\r\n[ \t]/", '', $ics); // lignes repliées
    $out = [];
    if (!preg_match_all('/BEGIN:VEVENT(.*?)END:VEVENT/s', $ics, $ev)) return $out;
    foreach ($ev[1] as $block) {
        if (!preg_match('/DTSTART[^:]*:(\d{8})/', $block, $s)) continue;
        $e = preg_match('/DTEND[^:]*:(\d{8})/', $block, $m) ? $m[1] : date('Ymd', strtotime($s[1] . ' +1 day'));
        $out[] = [(int)$s[1], (int)$e];
    }
    usort($out, function ($a, $b) { return $a[0] - $b[0]; });
    return $out;
}

$old = is_file($cacheFile) ? json_decode(file_get_contents($cacheFile), true) : null;
$result = ['updated' => date('c'), 'domaines' => []];
foreach ($ICAL as $slug => $id) {
    $ics = fetch_url($BASE . $id . '.ics');
    if ($ics !== false && strpos($ics, 'BEGIN:VCALENDAR') !== false) {
        $result['domaines'][$slug] = parse_ics($ics);
    } elseif ($old && isset($old['domaines'][$slug])) {
        $result['domaines'][$slug] = $old['domaines'][$slug]; // on garde la dernière version connue
    }
}
$json = json_encode($result);
@file_put_contents($cacheFile, $json, LOCK_EX);
echo $json;
