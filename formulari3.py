import json
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="TMB - Objectes perduts",
    page_icon="🧳",
    layout="centered"
)

# -------------------------------------------------------------
# CONTROL DEL COMPTADOR D'ID (7 DÍGITS ASCENDENT)
# -------------------------------------------------------------
def obtenir_seguent_id(fitxer="counter.txt", valor_inicial=1):
    ruta_fitxer = Path(__file__).parent / fitxer
    if not ruta_fitxer.exists():
        seguent_id = valor_inicial
    else:
        try:
            with open(ruta_fitxer, "r", encoding="utf-8") as f:
                contingut = f.read().strip()
                seguent_id = int(contingut) + 1 if contingut else valor_inicial
        except (ValueError, OSError):
            seguent_id = valor_inicial

    with open(ruta_fitxer, "w", encoding="utf-8") as f:
        f.write(str(seguent_id))

    return str(seguent_id).zfill(7)

# -------------------------------------------------------------
# CARREGAR DADES
# -------------------------------------------------------------
@st.cache_data
def carregar_cataleg():
    ruta = Path(__file__).parent / "catalogo.json"
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

data = carregar_cataleg()

# Línies de transport
lineas = data.get("transporte", {}).get("lineas", [])
METRO_LINES = [l["id"] for l in lineas if l.get("medio") == "metro" and l.get("activa", True)]
BUS_LINES = [l["nombre"] for l in lineas if l.get("medio") == "bus" and l.get("activa", True)]

# Taxonomia
subcats_comunes = data.get("subcategories_comunes", ["Altres", "No identificable"])
TAXONOMIA = {
    cat["nombre"]: cat.get("subcategorias", []) + [s for s in subcats_comunes if s not in cat.get("subcategorias", [])]
    for cat in data.get("categorias", [])
}

# -------------------------------------------------------------
# FORMULARI
# -------------------------------------------------------------
st.title("TMB - Objectes perduts")
st.write("Formulari per registrar una reclamació d'un objecte perdut a la xarxa de TMB.")

st.subheader("1. Dades de la pèrdua")
loss_date = st.date_input("Dia de la pèrdua")
transport = st.radio("Mitjà de transport", ["Metro", "Bus"], horizontal=True)

if transport == "Metro":
    lines = st.multiselect("Línia o línies de metro", METRO_LINES, placeholder="Tria línies...")
else:
    lines = st.multiselect("Línia o línies d'autobús", BUS_LINES, placeholder="Tria línies...")

st.divider()

st.subheader("2. Característiques de l'objecte")
category = st.selectbox("Categoria", list(TAXONOMIA.keys()))
subcategory = st.selectbox("Subcategoria", TAXONOMIA[category])

colors_selected = st.multiselect(
    "Colors principals (màxim 2)",
    data.get("colors", []),
    max_selections=data.get("max_colors", 2),
    placeholder="Tria fins a 2 colors"
)

brand = st.text_input("Marca (opcional)", max_chars=data.get("max_marca", 100))

st.divider()

st.subheader("3. Detalls i etiquetes visuals")
tags = st.multiselect("Etiquetes opcionals", data.get("etiquetes", []))
description = st.text_area(
    "Descripció escrita / detalls addicionals",
    max_chars=data.get("max_detalls", 500),
    help="Obligatori si la subcategoria és 'Altres'."
)
photo = st.file_uploader("Foto (opcional)", type=["jpg", "jpeg", "png"])

st.divider()

st.subheader("4. Dades de contacte")
contact_email = st.text_input("Correu electrònic")
contact_phone = st.text_input("Telèfon")
consent = st.checkbox("Autoritzo TMB a conservar les dades i contactar-me si es troba una coincidència.")

submitted = st.button("Enviar sol·licitud", type="primary")

# -------------------------------------------------------------
# ENVIAMENT I ASSIGNACIÓ D'ID
# -------------------------------------------------------------
if submitted:
    detalls_parts = []
    if tags:
        detalls_parts.append("Etiquetes: " + ", ".join(tags))
    if description.strip():
        detalls_parts.append(description.strip())
    detalls_finals = ". ".join(detalls_parts)

    linies_canoniques = [f"BUS_{l}" for l in lines] if transport == "Bus" else lines

    if not category:
        st.error("Cal indicar una categoria.")
    elif subcategory == "Altres" and not detalls_finals.strip():
        st.error("Per a la subcategoria 'Altres' és obligatori afegir etiquetes o descriure l'objecte.")
    elif not consent:
        st.error("Cal donar consentiment per conservar la sol·licitud.")
    else:
        # Generem el següent identificador de 7 dígits
        nou_id = obtenir_seguent_id()

        registre = {
            "id_reclamacio": nou_id,
            "categoria": category,
            "subcategoria": subcategory,
            "colors": colors_selected,
            "marca": brand.strip() if brand.strip() else None,
            "detalls": detalls_finals,
            "linia": linies_canoniques,
            "dia_de_perdua": str(loss_date),
            "contacte": {
                "email": contact_email.strip(),
                "telefon": contact_phone.strip()
            }
        }
        
        st.success(f"Sol·licitud registrada correctament! El teu codi de seguiment és: **#{nou_id}**")
        st.json(registre)
