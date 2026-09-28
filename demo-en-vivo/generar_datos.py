"""Generate a FICTITIOUS graduate employability survey for the UFRO talk demo.

All data is synthetic, produced with a fixed random seed (42) so it is fully
reproducible. It must never be presented as real. The story baked in on
purpose: graduates who report using AI at work tend to find their first job a
little faster, and "Uso de IA" shows up often among requested skills.

Run:
    python generar_datos.py
Outputs (next to this script):
    encuesta_egresados.csv
    resultados.json
"""

import json
import numpy as np
import pandas as pd

SEED = 42
N = 300

rng = np.random.default_rng(SEED)

CARRERAS = [
    "Agronomía",
    "Ingeniería Civil Industrial",
    "Ingeniería Civil Informática",
    "Enfermería",
    "Kinesiología",
    "Derecho",
    "Ingeniería Comercial",
    "Pedagogía en Inglés",
]

HABILIDADES = [
    "Excel",
    "Comunicación efectiva",
    "Uso de IA",
    "Inglés",
    "Trabajo en equipo",
    "Análisis de datos",
    "Gestión de proyectos",
]

# Probability that a graduate of each career reports using AI at work.
# Tech / data-adjacent careers skew higher, on purpose, for a believable story.
PROB_USA_IA = {
    "Agronomía": 0.35,
    "Ingeniería Civil Industrial": 0.50,
    "Ingeniería Civil Informática": 0.72,
    "Enfermería": 0.30,
    "Kinesiología": 0.32,
    "Derecho": 0.28,
    "Ingeniería Comercial": 0.48,
    "Pedagogía en Inglés": 0.40,
}

# Base mean months to first job per career (before the AI adjustment).
BASE_MESES = {
    "Agronomía": 7.0,
    "Ingeniería Civil Industrial": 6.0,
    "Ingeniería Civil Informática": 4.5,
    "Enfermería": 5.0,
    "Kinesiología": 6.5,
    "Derecho": 7.5,
    "Ingeniería Comercial": 6.2,
    "Pedagogía en Inglés": 6.8,
}

# Weight given to "Uso de IA" as a requested skill, per career (tech-heavy
# careers mention it more often), used alongside the other six skills.
PESO_IA_HABILIDAD = {
    "Agronomía": 1.5,
    "Ingeniería Civil Industrial": 2.5,
    "Ingeniería Civil Informática": 4.0,
    "Enfermería": 1.0,
    "Kinesiología": 1.0,
    "Derecho": 1.2,
    "Ingeniería Comercial": 2.8,
    "Pedagogía en Inglés": 1.3,
}

rows = []
for i in range(1, N + 1):
    carrera = rng.choice(CARRERAS)
    anio_egreso = int(rng.choice([2023, 2024, 2025], p=[0.30, 0.35, 0.35]))

    usa_ia = rng.random() < PROB_USA_IA[carrera]
    usa_ia_str = "Sí" if usa_ia else "No"

    base = BASE_MESES[carrera]
    ajuste_ia = -1.6 if usa_ia else 0.0
    meses = rng.normal(loc=base + ajuste_ia, scale=2.3)
    meses = float(np.clip(meses, 1, 18))
    meses = round(meses, 1)

    trabaja_en_area = "Sí" if rng.random() < (0.80 if usa_ia else 0.72) else "No"

    # 1-3 skills, "Uso de IA" weighted per career, rest roughly uniform.
    pesos = np.array(
        [PESO_IA_HABILIDAD[carrera] if h == "Uso de IA" else 1.0 for h in HABILIDADES]
    )
    pesos = pesos / pesos.sum()
    n_skills = int(rng.choice([1, 2, 3], p=[0.25, 0.45, 0.30]))
    elegidas = rng.choice(HABILIDADES, size=n_skills, replace=False, p=pesos)
    habilidades_str = "; ".join(elegidas.tolist())

    rows.append(
        {
            "id": i,
            "carrera": carrera,
            "anio_egreso": anio_egreso,
            "meses_primer_empleo": meses,
            "trabaja_en_su_area": trabaja_en_area,
            "usa_ia_en_el_trabajo": usa_ia_str,
            "habilidades_pedidas": habilidades_str,
        }
    )

df = pd.DataFrame(rows)

# ~6% blanks in meses_primer_empleo (incomplete responses).
n_blank_meses = round(N * 0.06)
idx_blank_meses = rng.choice(df.index, size=n_blank_meses, replace=False)
df.loc[idx_blank_meses, "meses_primer_empleo"] = np.nan

# A few blanks in usa_ia_en_el_trabajo too (people who skipped the question).
n_blank_ia = 7
idx_blank_ia = rng.choice(df.index, size=n_blank_ia, replace=False)
df.loc[idx_blank_ia, "usa_ia_en_el_trabajo"] = np.nan

csv_path = "encuesta_egresados.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------------------
# Compute the real numbers the video/report will show.
# ---------------------------------------------------------------------------
n_total = len(df)
n_excluidos = int(df["meses_primer_empleo"].isna().sum())

df_validas = df.dropna(subset=["meses_primer_empleo"])

media_por_carrera = (
    df_validas.groupby("carrera")["meses_primer_empleo"].mean().round(2).sort_values()
)

media_general = round(float(df_validas["meses_primer_empleo"].mean()), 2)

pct_en_su_area = round(
    100 * (df["trabaja_en_su_area"] == "Sí").sum() / n_total, 1
)

# Most requested skill (share of respondents whose list contains it).
conteo_habilidades = {}
for lista in df["habilidades_pedidas"]:
    for h in [x.strip() for x in lista.split(";")]:
        conteo_habilidades[h] = conteo_habilidades.get(h, 0) + 1
habilidad_top, habilidad_top_n = max(conteo_habilidades.items(), key=lambda kv: kv[1])
habilidad_top_pct = round(100 * habilidad_top_n / n_total, 1)

df_ia = df_validas.dropna(subset=["usa_ia_en_el_trabajo"])
media_meses_usa_ia = (
    df_ia[df_ia["usa_ia_en_el_trabajo"] == "Sí"]["meses_primer_empleo"].mean()
)
media_meses_no_ia = (
    df_ia[df_ia["usa_ia_en_el_trabajo"] == "No"]["meses_primer_empleo"].mean()
)

resultados = {
    "ficticio": True,
    "n_total": n_total,
    "n_excluidos_meses_primer_empleo": n_excluidos,
    "media_meses_por_carrera": {k: v for k, v in media_por_carrera.items()},
    "media_meses_general": media_general,
    "pct_trabaja_en_su_area": pct_en_su_area,
    "habilidad_mas_pedida": habilidad_top,
    "habilidad_mas_pedida_pct": habilidad_top_pct,
    "conteo_habilidades": conteo_habilidades,
    "media_meses_usa_ia_si": round(float(media_meses_usa_ia), 2),
    "media_meses_usa_ia_no": round(float(media_meses_no_ia), 2),
}

with open("resultados.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(json.dumps(resultados, ensure_ascii=False, indent=2))
