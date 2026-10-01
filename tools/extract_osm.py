"""
Complements the CIT-UAI visor with what it lacks: parks, plazas, playgrounds, bike lanes,
libraries and cultural venues in Lo Espejo, from OpenStreetMap (Overpass API).

Writes ../data/raw/osm_lo_espejo.geojson. Data (c) OpenStreetMap contributors, ODbL.
Run:  python tools/extract_osm.py
"""
import json
import os
import urllib.parse
import urllib.request

ENDPOINTS = ["https://overpass-api.de/api/interpreter",
             "https://overpass.private.coffee/api/interpreter",
             "https://maps.mail.ru/osm/tools/overpass/api/interpreter"]
QUERY = """
[out:json][timeout:120][bbox:{bbox}];
(
  nwr["leisure"~"^(park|playground|pitch|sports_centre|skatepark|fitness_station|garden)$"];
  nwr["amenity"~"^(library|arts_centre|community_centre|theatre|social_centre)$"];
  way["highway"="cycleway"];
  way["cycleway"~"^(lane|track|shared_lane)$"];
  way["cycleway:right"~"^(lane|track)$"];
  way["cycleway:left"~"^(lane|track)$"];
  way["cycleway:both"~"^(lane|track)$"];
);
out tags geom;
"""
# Bounding box of the 15 unidades vecinales (S, W, N, E) plus a ~300 m margin, so bike lanes
# and parks on the comuna edge are kept. Points are then clipped to the comuna polygons.
BBOX = (-33.5421, -70.7094, -33.4990, -70.6680)
UV = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "unidades_vecinales.geojson")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "osm_lo_espejo.geojson")


def kind(tags):
    if tags.get("highway") == "cycleway" or any(k.startswith("cycleway") for k in tags):
        return "ciclovia"
    return tags.get("leisure") or tags.get("amenity")


def rings():
    out = []
    for f in json.load(open(UV, encoding="utf-8"))["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        out += [p[0] for p in polys]
    return out


def inside(pt, ring):
    x, y, hit = pt[0], pt[1], False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


def in_comuna(geom, rs):
    pts = [geom["coordinates"]] if geom["type"] == "Point" else geom["coordinates"]
    return any(inside(p, r) for p in pts for r in rs)


def main():
    q = QUERY.replace("{bbox}", ",".join(map(str, BBOX)))
    for endpoint in ENDPOINTS:  # public servers fail transiently; try mirrors in order
        req = urllib.request.Request(endpoint, data=urllib.parse.urlencode({"data": q}).encode(),
                                     headers={"User-Agent": "KidsAppLoEspejo/0.1 (CIT-UAI prototype)"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                els = json.load(r)["elements"]
            break
        except (OSError, ValueError) as err:
            print(f"{endpoint} failed: {err}")
    else:
        raise SystemExit("all Overpass endpoints failed")
    feats, rs = [], rings()
    for e in els:
        tags = e.get("tags", {})
        k = kind(tags)
        if k == "ciclovia" and e.get("geometry"):
            geom = {"type": "LineString", "coordinates": [[p["lon"], p["lat"]] for p in e["geometry"]]}
        elif "bounds" in e:  # `out geom` gives bounds, not center, for ways and relations
            b = e["bounds"]
            geom = {"type": "Point", "coordinates": [(b["minlon"] + b["maxlon"]) / 2,
                                                     (b["minlat"] + b["maxlat"]) / 2]}
        elif "lat" in e:
            geom = {"type": "Point", "coordinates": [e["lon"], e["lat"]]}
        else:
            continue
        if not in_comuna(geom, rs):
            continue
        feats.append({"type": "Feature", "geometry": geom,
                      "properties": {"osm_id": f"{e['type']}/{e['id']}", "kind": k,
                                     "name": tags.get("name"), "sport": tags.get("sport")}})
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": feats}, fh, ensure_ascii=False)
    from collections import Counter
    print(Counter(f["properties"]["kind"] for f in feats))


if __name__ == "__main__":
    main()
