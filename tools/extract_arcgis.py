"""
Snapshot every layer behind the CIT-UAI visor "OPORTUNIDADES NNA COMUNIDAD".

Visor:    https://experience.arcgis.com/experience/27567a41504b4bb9a488e677e846fb4f
Web map:  624a05d73dc24fa6b3a4b7b32ce8bea2 (MAPA_EL_SAUCE), owner CIT_UAI_PROYECTOS

Writes, per layer, into ../data/raw/:
  <slug>.schema.json   field list, geometry type, record count
  <slug>.geojson       all features in WGS84 (skipped for layers > MAX_FEATURES)

Run:  python tools/extract_arcgis.py
Only uses the public REST API; no credentials. Re-run to refresh the snapshot.
"""
import json
import os
import urllib.parse
import urllib.request

BASE = "https://services.arcgis.com/JZxvGBwvCaXCwa4l/arcgis/rest/services"
LAYERS = {
    "programas_nna":        "Programas_Lo_Espejo_NNA_vista/FeatureServer/0",
    "programas_nna_edicion": "Programas_Lo_Espejo_NNA/FeatureServer/0",
    "resumen_programas":    "Resumen_Programas_Lo_Espejo/FeatureServer/0",
    "resumen_prog_le":      "RESUMEN_PROG_LE/FeatureServer/0",
    "beneficiarios":        "Beneficiarios_programas/FeatureServer/0",
    "unidades_vecinales":   "UV_LO_ESPEJO/FeatureServer/0",
    "manzanas_uv":          "MZ_UV_LO_ESPEJO/FeatureServer/0",
    "mbht_2017":            "MBHT_2017_Lo_Espejo/FeatureServer/0",
    "ctx_bomberos":         "EL_SAUCE_Shape_contexto/FeatureServer/0",
    "ctx_colegios":         "EL_SAUCE_Shape_contexto/FeatureServer/1",
    "ctx_carabineros":      "EL_SAUCE_Shape_contexto/FeatureServer/2",
    "ctx_deporte":          "EL_SAUCE_Shape_contexto/FeatureServer/3",
    "ctx_jardines":         "EL_SAUCE_Shape_contexto/FeatureServer/4",
    "ctx_pdi":              "EL_SAUCE_Shape_contexto/FeatureServer/5",
    "ctx_salud":            "EL_SAUCE_Shape_contexto/FeatureServer/8",
    "ctx_servicios":        "EL_SAUCE_Shape_contexto/FeatureServer/9",
}
MAX_FEATURES = 6000
# Layers designed to hold personal data of minors: keep the schema, never the rows.
SCHEMA_ONLY = {"beneficiarios"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def get(url, **params):
    params.setdefault("f", "json")
    full = url + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(full, timeout=60) as r:
        return json.load(r)


def query_all(url, page):
    feats, offset = [], 0
    while True:
        res = get(url + "/query", where="1=1", outFields="*", outSR=4326,
                  f="geojson", resultOffset=offset, resultRecordCount=page)
        batch = res.get("features", [])
        feats += batch
        if len(batch) < page:
            return feats
        offset += page


def main():
    os.makedirs(OUT, exist_ok=True)
    summary = {}
    for slug, path in LAYERS.items():
        url = f"{BASE}/{path}"
        try:
            meta = get(url)
            count = get(url + "/query", where="1=1", returnCountOnly="true").get("count")
        except Exception as e:  # layer removed or private
            summary[slug] = {"error": str(e)}
            print(f"{slug:24} ERROR {e}")
            continue
        schema = {
            "url": url,
            "name": meta.get("name"),
            "geometryType": meta.get("geometryType"),
            "count": count,
            "fields": [{"name": f["name"], "alias": f.get("alias"), "type": f["type"]}
                       for f in meta.get("fields", [])],
        }
        with open(os.path.join(OUT, f"{slug}.schema.json"), "w", encoding="utf-8") as fh:
            json.dump(schema, fh, ensure_ascii=False, indent=1)
        if slug not in SCHEMA_ONLY and count is not None and count <= MAX_FEATURES:
            page = meta.get("maxRecordCount") or 1000
            gj = {"type": "FeatureCollection", "features": query_all(url, min(page, 2000))}
            with open(os.path.join(OUT, f"{slug}.geojson"), "w", encoding="utf-8") as fh:
                json.dump(gj, fh, ensure_ascii=False)
        summary[slug] = {"count": count, "geometry": schema["geometryType"],
                         "fields": len(schema["fields"])}
        print(f"{slug:24} {str(count):>6}  {schema['geometryType']}")
    with open(os.path.join(OUT, "_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
