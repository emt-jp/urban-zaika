"""
Build outreach prospect lists around both branches from the Google Places API.

The outreach templates in marketing/outreach-templates.md need somewhere to be sent. This turns
them into an actual call list: mosques and prayer spaces, halal groceries, nearby offices for the
忘年会 pitch, event venues, and the competing halal/Indian restaurants we are measured against.

Costs money. Each search is one Places "Text Search (Pro)" request — roughly US$0.03 — and a full
run is about 30 of them, so a few tens of cents. It reads the key from the environment and never
writes it anywhere:

    export GOOGLE_MAPS_API_KEY="$(cat ~/.config/urban-zaika/places_key)"
    python3 scripts/places-prospects.py

Writes prospects-<category>.csv and prospects.md next to each other in --out (default: a
gitignored marketing/prospects/ directory — the output is public data but it is a lead list, and
this repo is public).
"""
import argparse
import csv
import json
import os
import pathlib
import sys

import urllib.error
import urllib.request

TEXT_ENDPOINT = 'https://places.googleapis.com/v1/places:searchText'
NEARBY_ENDPOINT = 'https://places.googleapis.com/v1/places:searchNearby'

FIELDS = [
    'places.id',
    'places.displayName',
    'places.formattedAddress',
    'places.nationalPhoneNumber',
    'places.websiteUri',
    'places.rating',
    'places.userRatingCount',
    'places.googleMapsUri',
    'places.primaryTypeDisplayName',
    'places.businessStatus',
    'places.location',
]

BRANCHES = {
    'kita-ku': {'label': '十条店 (Jujo)', 'address': '東京都北区上十条5-14-6'},
    'edogawa': {'label': '上一色店 (Kamiisshiki)', 'address': '東京都江戸川区上一色1-8-21'},
}

# Nearby search, not text search: a text query for "mosque in Kita-ku" ranks by prominence and
# happily returns Tokyo Camii in Shibuya, or a masjid in Yamanashi. A radius restriction is the
# only thing that keeps a prospect list walkable.
# (category, included types, radius in metres, why we want it)
SEARCHES = [
    ('mosques', ['mosque'], 7000, 'Catering leads — committees rebook the same caterer'),

    ('offices', ['corporate_office'], 1500, '忘年会 catering pitch'),
    ('venues', ['event_venue', 'community_center', 'banquet_hall'], 3000,
     'Venues and halls that need caterers'),
    ('competitors', ['indian_restaurant', 'pakistani_restaurant', 'middle_eastern_restaurant'],
     2500, 'Who we are measured against'),
]

# (category, text query, radius bias in metres, why)
TEXT_SEARCHES = [
    ('halal-shops', 'ハラルフード ハラル食材店', 5000, 'Flyers and reciprocal referral'),
    ('halal-shops', 'halal grocery meat shop', 5000, 'Flyers and reciprocal referral'),
]

OURS = ('urban zaika', 'アーバンザイカ', 'urban zaiqa', 'suhana')


def post(endpoint, body, key, fields):
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode(),
        headers={
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': key,
            'X-Goog-FieldMask': ','.join(fields),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        # the body carries the real reason (quota, restriction, bad field mask)
        print(f'  ! HTTP {e.code}: {e.read().decode()[:220]}', file=sys.stderr)
        return {}


def geocode(address, key):
    data = post(TEXT_ENDPOINT, {'textQuery': address, 'languageCode': 'ja', 'maxResultCount': 1},
                key, ['places.location', 'places.formattedAddress'])
    places = data.get('places') or []
    if not places:
        sys.exit(f'could not locate {address}')
    loc = places[0]['location']
    return loc['latitude'], loc['longitude']


def metres(lat1, lng1, lat2, lng2):
    from math import radians, sin, cos, asin, sqrt
    dlat, dlng = radians(lat2 - lat1), radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return round(2 * 6371000 * asin(sqrt(a)))


def flatten(place, branch, why, origin):
    loc = place.get('location') or {}
    return {
        'branch': branch,
        'metres': metres(origin[0], origin[1], loc.get('latitude', 0), loc.get('longitude', 0))
                  if loc else '',
        'name': (place.get('displayName') or {}).get('text', ''),
        'address': place.get('formattedAddress', '').replace('日本、', ''),
        'phone': place.get('nationalPhoneNumber', ''),
        'website': place.get('websiteUri', ''),
        'rating': place.get('rating', ''),
        'reviews': place.get('userRatingCount', ''),
        'type': (place.get('primaryTypeDisplayName') or {}).get('text', ''),
        'status': place.get('businessStatus', ''),
        'maps': place.get('googleMapsUri', ''),
        'why': why,
        'id': place.get('id', ''),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='marketing/prospects')
    args = ap.parse_args()

    key = os.environ.get('GOOGLE_MAPS_API_KEY')
    if not key:
        sys.exit('GOOGLE_MAPS_API_KEY is not set — see the docstring')

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    rows, seen, calls = {}, set(), 0
    for slug, branch in BRANCHES.items():
        origin = geocode(branch['address'], key)
        calls += 1
        print(f'{slug}: {origin[0]:.5f}, {origin[1]:.5f}')

        for category, types, radius, why in SEARCHES:
            body = {
                'includedTypes': types,
                'maxResultCount': 20,
                'languageCode': 'ja',
                'rankPreference': 'DISTANCE',
                'locationRestriction': {
                    'circle': {
                        'center': {'latitude': origin[0], 'longitude': origin[1]},
                        'radius': float(radius),
                    }
                },
            }
            data = post(NEARBY_ENDPOINT, body, key, FIELDS)
            calls += 1
            found = data.get('places', [])
            kept = 0
            for pl in found:
                pid = pl.get('id')
                name = ((pl.get('displayName') or {}).get('text') or '').lower()
                if not pid or pid in seen or any(o in name for o in OURS):
                    continue
                seen.add(pid)
                rows.setdefault(category, []).append(flatten(pl, branch['label'], why, origin))
                kept += 1
            print(f'  {category:12} {len(found):3} found, {kept:3} kept  (r={radius}m)')

        for category, query, radius, why in TEXT_SEARCHES:
            body = {
                'textQuery': query,
                'languageCode': 'ja',
                'maxResultCount': 20,
                'locationBias': {
                    'circle': {
                        'center': {'latitude': origin[0], 'longitude': origin[1]},
                        'radius': float(radius),
                    }
                },
            }
            data = post(TEXT_ENDPOINT, body, key, FIELDS)
            calls += 1
            kept = 0
            for pl in data.get('places', []):
                pid = pl.get('id')
                name = ((pl.get('displayName') or {}).get('text') or '').lower()
                if not pid or pid in seen or any(o in name for o in OURS):
                    continue
                row = flatten(pl, branch['label'], why, origin)
                # a bias is not a restriction — Shin-Okubo outranks everything on prominence
                if row['metres'] != '' and row['metres'] > radius * 1.5:
                    continue
                seen.add(pid)
                rows.setdefault(category, []).append(row)
                kept += 1
            print(f'  {category:12} {kept:3} kept  "{query}"')

    for category, items in sorted(rows.items()):
        items.sort(key=lambda r: (r['metres'] if r['metres'] != '' else 1 << 30))
        path = out / f'prospects-{category}.csv'
        with path.open('w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=list(items[0].keys()))
            w.writeheader()
            w.writerows(items)
        print(f'wrote {path} ({len(items)})')

    write_digest(out / 'prospects.md', rows)
    print(f"wrote {out / 'prospects.md'}")

    total = sum(len(v) for v in rows.values())
    print(f'\n{total} unique places from {calls} API calls (~US${calls * 0.032:.2f})')


TITLES = {
    'mosques': 'Mosques and prayer spaces — catering leads',
    'halal-shops': 'Halal groceries — flyers and reciprocal referral',
    'offices': 'Offices within 1.5 km — 忘年会 pitch',
    'venues': 'Venues and halls — they need caterers',
    'competitors': 'Competing Indian, Pakistani and halal restaurants',
}


def write_digest(path, rows):
    """A CSV is for filtering; this is for walking out of the door with."""
    from datetime import date
    out = [
        '# Prospect list',
        '',
        f'Generated {date.today().isoformat()} by `scripts/places-prospects.py` from the Google '
        'Places API, ranked by walking distance from each branch. Phone numbers and ratings are '
        "Google's, so check them before a cold call — listings go stale.",
        '',
        'Send the messages in `outreach-templates.md`. Record who was contacted and when: most of '
        'these need a second approach before they answer.',
        '',
    ]

    walkable = sorted(
        (r for cat in ('mosques', 'halal-shops') for r in rows.get(cat, [])
         if r['metres'] != '' and r['metres'] <= 1500),
        key=lambda r: r['metres'])
    if walkable:
        out += ['## Do these on foot this week', '',
                'Everything below is within 1.5 km of a branch. An afternoon covers the lot.', '',
                '| Distance | Place | Phone | Branch |', '|---|---|---|---|']
        out += [f"| {r['metres']} m | {r['name']} | {r['phone'] or '—'} | {r['branch']} |"
                for r in walkable]
        out += ['']

    for cat, items in sorted(rows.items()):
        out += [f'## {TITLES.get(cat, cat)}', '',
                '| Distance | Name | Phone | Rating | Address |', '|---|---|---|---|---|']
        for r in items:
            rating = f"{r['rating']} ({r['reviews']})" if r['rating'] else '—'
            d = f"{r['metres']} m" if r['metres'] != '' else '—'
            out += [f"| {d} | [{r['name']}]({r['maps']}) | {r['phone'] or '—'} | {rating} | "
                    f"{r['address']} |"]
        out += ['']

    path.write_text('\n'.join(out), encoding='utf-8')


if __name__ == '__main__':
    main()
