"""
Builds 04_prototype/data/app_data.js from the snapshots in data/raw/.

- Activities: CIT-UAI programs for NNA whose audience overlaps 8-17 (age parsed from the
  free-text PUBL_OBJET field). Specialised protection programs (PPF, PIE, DAM, PDE...) are
  NOT listed as activities: kids reach them by referral, and showing them next to "futsal"
  would stigmatise. They are represented by their entry points (OLN, CESFAM, Juventud).
- Places: parks, playgrounds, library, theatre (OSM) + sport venues and schools (CIT-UAI).
- Bike lanes (OSM) and unidades vecinales with Censo 2024 kid counts (for the planner view).
- Demo events: the visor has no events layer, so a few are generated at real venues and
  flagged demo=True.

Run:  python tools/build_app_data.py
"""
import json
import os
import re
from collections import Counter, defaultdict

ROOT = os.path.join(os.path.dirname(__file__), "..")
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "04_prototype", "data", "app_data.js")


def load(name):
    with open(os.path.join(RAW, name), encoding="utf-8") as fh:
        return json.load(fh)["features"]


def pt(f):
    x, y = f["geometry"]["coordinates"][:2]
    return [round(y, 5), round(x, 5)]


# ---------- age parsing ----------
NUM = r"(\d{1,2})"
AGE_PATTERNS = [
    (r"(\d)\s*[°º]?\s*(?:do|to|ro|er)?\s*a\s*(\d)\s*[°º]?\s*(?:do|to|ro|er)?\s*básico", "grades"),
    (rf"(?:desde|de|entre)\s+(?:los\s+)?0?{NUM}\s*(?:años\s*)?(?:hasta|a|y)?\s+(?:los\s+)?{NUM}", "range"),
    (rf"{NUM}\s*(?:-|–)\s*{NUM}\s*años", "range"),
    (rf"(?:desde\s+los|de)\s+0?{NUM}\s*años\s*(?:o\s+más|en\s+adelante)?", "min"),
    (rf"{NUM}\s*años\s*o\s*más", "min"),
    (rf"menores\s+de\s+{NUM}", "max"),
]


def parse_age(*texts):
    text = " ".join(t for t in texts if t).lower()
    for pat, kind in AGE_PATTERNS:
        m = re.search(pat, text)
        if not m:
            continue
        if kind == "grades":  # n° básico is roughly age n+5 to n+6
            return int(m.group(1)) + 5, int(m.group(2)) + 6
        if kind == "range":
            return int(m.group(1)), int(m.group(2))
        if kind == "min":
            return int(m.group(1)), 99
        return 0, int(m.group(1)) - 1
    if re.search(r"niñ|adolesc|nna", text):
        return 0, 17
    if "mayores" in text:
        return 60, 99
    return None


# ---------- activity typing ----------
TYPES = [  # (regex on program name, slug, app category)
    (r"futsal|fútbol|futbol|barrio", "futbol", "deporte"),
    (r"básquet|basquet", "basquet", "deporte"),
    (r"vóley|voley|vóleibol", "voley", "deporte"),
    (r"tenis", "tenis", "deporte"),
    (r"hockey|palín|palin", "hockey", "deporte"),
    (r"patinaje", "patin", "deporte"),
    (r"artes marciales|defensa personal|taich", "marciales", "deporte"),
    (r"parkour|boulder|escalada", "escalada", "deporte"),
    (r"calistenia|funcional|spinning", "fuerza", "deporte"),
    (r"zumba|cheer|ballet|danza|baile", "baile", "arte"),
    (r"rock|batucada|música|musica|orquesta|guitarra", "musica", "arte"),
    (r"robótica|robotica", "robotica", "aprender"),
    (r"preuniversitario|beca|estudios|educación|after school|leer|tan", "estudio", "aprender"),
]
PROTECTION = re.compile(r"\b(PPF|PIE|DAM|PDE|PRM|SENDA)\b|protección especializada|consumo|vulneraci", re.I)
NOT_FOR_KIDS = re.compile(r"cuidador|profesional|organizaciones|mascota|dependencia|personas mayores|"
                          r"víctimas|alarmas|subvenci|fondos|madres, padres|dale ?profe|kinder power", re.I)
KID_AUDIENCE = re.compile(r"niñ|adolesc|nna|jóvenes|jovenes|años", re.I)
ENTRY_POINTS = re.compile(r"Oficina Local de la Niñez|Oficina Municipal de Juventud|CESFAM|CESAM|Consultorio|Ruka", re.I)


def activity_type(name, cat):
    for pat, slug, appcat in TYPES:
        if re.search(pat, name, re.I):
            return slug, appcat
    return ("arte", "arte") if "Arte" in cat else ("estudio", "aprender")


def how_to_join(via, req):
    """Rewrite the municipal enrollment fields in words a 10 year old understands."""
    v, r = (via or "").lower(), (req or "").lower()
    if "oficinadelaninez@" in v:
        join = "Inscríbete escribiendo a oficinadelaninez@loespejo.cl"
    elif "derivaci" in v:
        join = "Te inscribe tu colegio (cupos limitados)"
    elif "establecimiento" in v:
        join = "Pregunta en tu colegio"
    elif "online" in v:
        join = "Llega directo o inscríbete online"
    elif "espont" in v:
        join = "Llega directo y pregunta, no necesitas inscribirte antes"
    else:
        join = "Pregunta en la oficina que lo organiza"
    if "ningun requisito" in r or "ningún requisito" in r:
        need = "Sin requisitos, solo tener la edad"
    elif "residir" in r or "vivan o estudien" in r:
        need = "Vivir o estudiar en Lo Espejo"
    elif "san lucas" in r:
        need = "Ser estudiante del Colegio San Lucas"
    else:
        need = None
    return join, need


def clean(s, n=None):
    s = re.sub(r"\s+", " ", (s or "").replace(" ", " ")).strip()
    return s[:n].rsplit(" ", 1)[0] + "…" if n and len(s) > n else s


def build_activities():
    groups, help_points, skipped = {}, [], Counter()
    for f in load("programas_nna.geojson"):
        p = f["properties"]
        name, cat = clean(p["PROGRAMA"]), p["CATEGORÍA"] or ""
        audience = clean(p["PUBL_OBJET"])
        org = clean(p.get("ORGANIZACIÓN_IMPLEMENTADORA") or p.get("ORG_ORI"))
        if ENTRY_POINTS.search(name):
            help_points.append({"id": f"h{p['FID']}", "name": name, "org": org,
                                "address": clean(p["DIREC_ESP"]), "ll": pt(f),
                                "desc": clean(p["DESC_P_RES"], 160)})
            continue
        if (PROTECTION.search(name + " " + audience)
                or cat in ("Apoyos específicos y protección social", "Salud y bienestar integral")):
            skipped["protection/health referral"] += 1
            continue
        desc = p["DESC_P_RES"] or ""
        adult_first = re.match(r"(profesionales|mujeres cuidadoras|personas cuidadoras|organizaciones)",
                               audience, re.I)  # "Profesionales que trabajan con niños" is not for kids
        if adult_first or NOT_FOR_KIDS.search(name + " " + desc) or (
                NOT_FOR_KIDS.search(audience) and not KID_AUDIENCE.search(audience)):
            skipped["adults/caregivers"] += 1
            continue
        ages = parse_age(audience, desc)
        if ages and ages[1] == 99 and re.search(r"niñ|adolesc", audience, re.I):
            ages = (ages[0], 17)  # "ballet desde los 4 años" for an NNA audience
        if ages is None or ages[1] < 8 or ages[0] > 17:
            skipped["age outside 8-17"] += 1
            continue
        slug, appcat = activity_type(name, cat)
        name = re.sub(r"^Escuelas Abiertas\s*/\s*", "", name)
        name = re.sub(r"\s*-\s*Niñeces$", "", name)
        site = {"address": clean(p["DIREC_ESP"]), "schedule": clean(p.get("HORARIO")), "ll": pt(f)}
        key = (name.lower(), audience.lower())
        if key in groups:  # same program at another site: one activity, several sedes
            groups[key]["sites"].append(site)
            continue
        join, need = how_to_join(p.get("V_INGRESO"), p.get("REQUISITO"))
        groups[key] = {
            "id": f"a{p['FID']}", "name": name, "type": slug, "cat": appcat,
            "join": join, "need": need,
            "ages": [max(ages[0], 5), min(ages[1], 29)], "audience": audience,
            "desc": clean(desc, 180), "org": org, "free": True,
            "link": (p.get("LINK_REF") or "").strip() or None, "sites": [site],
        }
    return list(groups.values()), help_points, skipped


def build_places():
    places = []
    for f in load("osm_lo_espejo.geojson"):
        p, g = f["properties"], f["geometry"]
        if g["type"] != "Point":
            continue
        k = p["kind"]
        kind = {"park": "parque", "garden": "parque", "playground": "juegos",
                "fitness_station": "maquinas", "skatepark": "skate", "library": "biblioteca",
                "theatre": "cultura", "arts_centre": "cultura", "community_centre": "sede",
                "social_centre": "sede", "sports_centre": "cancha"}.get(k)
        if not kind:
            continue  # OSM pitches are covered by the CIT-UAI sport layer
        name = p["name"] or {"parque": "Plaza del barrio", "juegos": "Juegos infantiles",
                             "maquinas": "Máquinas de ejercicio", "sede": "Sede vecinal",
                             "cancha": "Recinto deportivo"}.get(kind, "Lugar")
        places.append({"id": "o" + p["osm_id"].split("/")[1], "name": name, "kind": kind,
                       "named": bool(p["name"]), "ll": pt(f), "src": "OSM"})
    for f in load("ctx_deporte.geojson"):
        p = f["properties"]
        tipo = p.get("tipo") or "Cancha"
        name = p["NOMBRE"] if p["NOMBRE"] and p["NOMBRE"] != "SIN NOMBRE" else tipo
        places.append({"id": f"d{p['FID']}", "name": name.title() if name.isupper() else name,
                       "kind": "cancha", "sub": tipo, "named": p["NOMBRE"] != "SIN NOMBRE",
                       "ll": pt(f), "src": "CIT-UAI"})
    return places


SCHOOL_FIXES = [  # MINEDUC names are abbreviated and unaccented; kids search by the real name
    (r"Centro Duc\.cardenal", "Centro Educacional Cardenal"), (r"\bEsc\. ?", "Escuela "),
    (r"\bPart\. ?", "Particular "), (r"\bPoliv\. ?", "Polivalente "), (r"\bBas\. ", "Básica "),
    (r"\bBasica\b", "Básica"), (r"\bEsp\. ", "Especial "), (r"\bEduc\. ", "Educacional "),
    (r"\bEducacion\b", "Educación"), (r"Jose Maria", "José María"), (r"Hernan Olguin", "Hernán Olguín"),
    (r"Republica", "República"), (r"Salomon", "Salomón"), (r"\bRaul\b", "Raúl"), (r"\bJesus\b", "Jesús"),
    (r"Politecnico", "Politécnico"), (r"\bCorazon\b", "Corazón"), (r"O´higgins", "O'Higgins"),
    (r"\b(De|Del|Los|La|Of)\b", lambda m: m.group(1).lower()), (r"\bbasica\b", "Básica"),
    (r"Particular (\w)", lambda m: "Particular " + m.group(1).upper()), (r"\s+", " "),
]


def pretty_school(n):
    for pat, rep in SCHOOL_FIXES:
        n = re.sub(pat, rep, n)
    return n.strip()


def build_schools():
    out = []
    for f in load("ctx_colegios.geojson"):
        p = f["properties"]
        n = pretty_school(clean(p["NOM_RBD"]))
        if re.search(r"p[aá]rv|adultos", n, re.I):
            continue
        out.append({"id": f"s{p['ID_RBD']}", "name": n, "rbd": p["ID_RBD"],
                    "dep": "municipal" if p["COD_DEPE2"] == 1 else "subvencionado", "ll": pt(f)})
    return sorted(out, key=lambda s: s["name"])


def build_bike():
    return [[[round(y, 5), round(x, 5)] for x, y in f["geometry"]["coordinates"]]
            for f in load("osm_lo_espejo.geojson") if f["geometry"]["type"] == "LineString"]


def build_uv():
    kids = defaultdict(lambda: [0, 0, 0])
    for f in load("manzanas_uv.geojson"):
        p = f["properties"]
        k = kids[p["t_uv_nom"]]
        k[0] += p["n_per"] or 0
        k[1] += p["n_edad_6_1"] or 0
        k[2] += p["n_edad_14_"] or 0
    out = []
    for f in load("unidades_vecinales.geojson"):
        p, g = f["properties"], f["geometry"]
        ring = (g["coordinates"][0][0] if g["type"] == "MultiPolygon" else g["coordinates"][0])
        step = max(1, len(ring) // 70)
        ring = ring[::step] + [ring[0]]
        pop, a, b = kids[p["t_uv_nom"]]
        out.append({"uv": p["t_uv_nom"], "pop": pop, "kids": round(a * 0.75 + b),
                    "ring": [[round(y, 5), round(x, 5)] for x, y in ring]})
    return out


def demo_events(places):
    by_name = {p["name"]: p for p in places}
    venue = lambda n, fallback: by_name.get(n, fallback)
    anfi = venue("Anfiteatro Violeta Parra", places[0])
    bib = venue("Biblioteca Municipal de Lo Espejo", places[0])
    parque = venue("Parque Violeta Parra", places[0])
    gim = next((p for p in places if p.get("sub") == "Gimnasio municipal"), places[0])
    return [
        {"id": "e1", "demo": True, "name": "Tocata de bandas escolares", "type": "musica",
         "desc": "Las bandas de los colegios de Lo Espejo tocan en vivo.",
         "date": "2026-10-09", "time": "17:00", "place": anfi["name"], "ll": anfi["ll"], "ages": [10, 17]},
        {"id": "e2", "demo": True, "name": "Cine bajo las estrellas", "type": "cine",
         "desc": "Película al aire libre con tu barrio. Trae un cojín.",
         "date": "2026-10-10", "time": "19:30", "place": parque["name"], "ll": parque["ll"], "ages": [8, 17]},
        {"id": "e3", "demo": True, "name": "Copa Futsal de Barrio", "type": "futbol",
         "desc": "Torneo entre barrios. Arma tu equipo o ven a alentar.",
         "date": "2026-10-17", "time": "11:00", "place": gim["name"], "ll": gim["ll"], "ages": [8, 16]},
        {"id": "e4", "demo": True, "name": "Club de cómics y manga", "type": "estudio",
         "desc": "Dibuja, lee y comparte tus cómics favoritos.",
         "date": "2026-10-14", "time": "16:30", "place": bib["name"], "ll": bib["ll"], "ages": [9, 15]},
    ]


def main():
    acts, help_points, skipped = build_activities()
    places = build_places()
    data = {
        "meta": {
            "generated": "2026-09-28",
            "sources": [
                "CIT-UAI, visor OPORTUNIDADES NNA COMUNIDAD (ArcGIS Online), capas Programas_Lo_Espejo_NNA_vista, EL_SAUCE_Shape_contexto, UV_LO_ESPEJO, MZ_UV_LO_ESPEJO",
                "INE, Censo de Población y Vivienda 2024, datos por manzana (vía capa MZ_UV_LO_ESPEJO)",
                "© OpenStreetMap contributors (ODbL): parques, juegos, ciclovías, biblioteca, anfiteatro",
            ],
            "skipped": dict(skipped),
        },
        "activities": acts, "help": help_points, "places": places,
        "schools": build_schools(), "bike": build_bike(), "uv": build_uv(),
        "events": demo_events(places),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("// Generated by tools/build_app_data.py. Do not edit by hand.\n")
        fh.write("window.APP_DATA = ")
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write(";\n")
    print(f"activities {len(acts)} ({sum(len(a['sites']) for a in acts)} sites)  help {len(help_points)}  places {len(places)}  "
          f"schools {len(data['schools'])}  bike {len(data['bike'])}  uv {len(data['uv'])}")
    print("skipped", dict(skipped))
    print("by cat", Counter(a["cat"] for a in acts), "by type", Counter(a["type"] for a in acts))
    print("size KB", os.path.getsize(OUT) // 1024)


if __name__ == "__main__":
    main()
