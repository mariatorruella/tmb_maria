import streamlit as st

st.set_page_config(
    page_title="TMB - Objectes perduts",
    page_icon="🧳",
    layout="centered"
)

st.title("TMB - Objectes perduts")
st.write("Formulari per registrar una reclamació d'un objecte perdut a la xarxa de TMB.")

# -------------------------------------------------------------
# DADES DEL CATÀLEG DE LÍNIES (METRO I BUS)
# -------------------------------------------------------------
METRO_LINES = [
    "METRO_L1", "METRO_L2", "METRO_L3", "METRO_L4", "METRO_L5",
    "METRO_L9N", "METRO_L9S", "METRO_L10N", "METRO_L10S", "METRO_L11"
]

BUS_LINES = [
    # Línies Diagonals (D)
    "D20", "D40", "D50",
    # Línies Horitzontals (H)
    "H2", "H4", "H6", "H8", "H10", "H12", "H14", "H16",
    # Línies Verticals (V)
    "V1", "V3", "V5", "V7", "V9", "V11", "V13", "V15", "V17", "V19",
    "V21", "V23", "V25", "V27", "V29", "V31", "V33",
    # Línies Exprés (X)
    "X1", "X2", "X3",
    # Línies convencionals
    "6", "7", "13", "19", "22", "23", "24", "27", "33", "34", "39",
    "46", "47", "54", "55", "59", "60", "62", "63", "65", "67", "68",
    "70", "76", "78", "94", "95", "96", "97",
    # Línies de proximitat / Bus del Barri
    "107", "109", "112", "113", "114", "115", "116", "117", "118", "119",
    "120", "121", "122", "123", "124", "125", "126", "127", "128", "129",
    "130", "131", "132", "133", "134", "136", "141", "150", "157", "175",
    "180", "182", "183", "185", "191", "192", "196"
]

# -------------------------------------------------------------
# DICCIONARI DE TAXONOMIA EN CATALÀ (30 CATEGORIES)
# -------------------------------------------------------------
TAXONOMIA = {
    "Bosses i equipatge": [
        "Motxilla", "Bossa de mà / Bossa", "Bandolera", "Ronyonera", "Bossa de roba (tote bag)", 
        "Bossa d'esport", "Bossa de viatge", "Maleta", "Maletí", "Bossa de la compra", 
        "Carret de la compra", "Bossa tèrmica / nevera portàtil", "Portavestits", 
        "Bossa de cordons", "Bossa de platja", "Altres", "No identificable"
    ],
    "Carteres i contenidors personals": [
        "Cartera o bitlletera", "Moneder", "Targeter", "Portadocumentació", 
        "Portapassaport", "Necesser", "Joier portàtil", "Altres", "No identificable"
    ],
    "Documentació, targetes i diners": [
        "Document d'identitat (DNI / NIE)", "Passaport", "Permís de conduir", "Targeta sanitària", 
        "Targeta bancària", "Targeta de transport (T-mobilitat, etc.)", "Acreditació o carnet", 
        "Targeta d'accés", "Entrada o bitllet en paper", "Document solt", 
        "Conjunt de documents", "Xec", "Bitllet de diners", "Moneda", 
        "Conjunt de diners", "Altres", "No identificable"
    ],
    "Claus i dispositius d'accés": [
        "Clau mecànica individual", "Conjunt de claus", "Clau de vehicle amb comandament", 
        "Comandament d'accés / pàrquing", "Identificador electrònic / clauer RFID", 
        "Clauer sense claus", "Cadenat", "Pany o bombí", "Altres", "No identificable"
    ],
    "Dispositius electrònics personals": [
        "Telèfon mòbil", "Tauleta", "Ordinador portàtil", "Lector electrònic (e-reader)", 
        "Rellotge intel·ligent (smartwatch)", "Polsera d'activitat", "Consola portàtil", 
        "Calculadora", "Traductor electrònic", "Localitzador d'objectes (AirTag, etc.)", 
        "Dispositiu GPS", "Altres", "No identificable"
    ],
    "Àudio, fotografia i vídeo": [
        "Auriculars de diadema", "Auriculars amb cable", "Auricular sense fil individual", 
        "Conjunt d'auriculars sense fil", "Estoig de càrrega d'auriculars", "Altaveu", 
        "Reproductor d'àudio", "Ràdio", "Micròfon", "Càmera fotogràfica", "Càmera de vídeo", 
        "Càmera d'acció", "Objectiu", "Flaix", "Trípode", "Estabilitzador", "Prismàtics", 
        "Altres", "No identificable"
    ],
    "Accessoris electrònics i informàtica": [
        "Carregador de paret", "Carregador de vehicle", "Bateria externa (powerbank)", 
        "Bateria extraïble", "Cable", "Adaptador", "Concentrador USB / hub", "Memòria USB (pendrive)", 
        "Targeta de memòria (SD / microSD)", "Disc dur extern", "Ratolí", "Teclat", 
        "Llapis tàctil / digital", "Comandament de videojocs", "Comandament a distància", 
        "Suport per a dispositiu", "Component informàtic", "Lector de targetes", 
        "Altres", "No identificable"
    ],
    "Fundes i estoigs protectors": [
        "Funda de mòbil", "Funda de tauleta", "Funda de portàtil", "Funda d'ulleres", 
        "Funda de càmera", "Funda d'instrument", "Funda de paraigua", 
        "Estoig protector genèric", "Altres", "No identificable"
    ],
    "Roba": [
        "Abric", "Jaqueta / caçadora", "Americana / blazer", "Armilla", "Impermeable", 
        "Ponxo", "Sudadera", "Jersei", "Càrdigan", "Samarreta", "Camisa", "Blusa", 
        "Pantalons", "Pantalons curts", "Faldilla", "Vestit", "Mono", "Roba interior", 
        "Mitjons", "Mitges", "Banyador", "Pijama", "Conjunt de peces", 
        "Altres", "No identificable"
    ],
    "Complements de vestir": [
        "Gorra", "Barret", "Gorro de llana", "Boina", "Bufanda", "Mocador de coll / fulard", 
        "Braga de coll", "Guant individual", "Parell de guants", "Cinturó", "Corbata", 
        "Pajarita", "Tirants", "Ventall", "Orelleres", "Passamuntanyes", "Accessori per als cabells", 
        "Altres", "No identificable"
    ],
    "Calçat": [
        "Bambes / vambes esportives", "Sabates", "Botes", "Botins", "Sandàlies", 
        "Xancletes", "Sabatilles d'estar per casa", "Esclops", "Escarpins", 
        "Altres", "No identificable"
    ],
    "Ulleres": [
        "Ulleres graduades / vidre transparent", "Ulleres de sol", "Ulleres amb clip solar", 
        "Montura sense vidres", "Altres", "No identificable"
    ],
    "Joieria i rellotgeria convencional": [
        "Rellotge de polsera", "Rellotge de butxaca", "Anell", "Polsera", "Collaret", 
        "Cadena", "Penjoll", "Arrecada individual", "Parella d'arrecades", "Braçalet / fermall", 
        "Bessons de camisa", "Agulla de corbata", "Pírcing", "Altres", "No identificable"
    ],
    "Paraigües i para-sols": [
        "Paraigua plegable", "Paraigua llarg", "Paraigua de tipus no identificable", 
        "Para-sol", "Altres", "No identificable"
    ],
    "Llibres, papereria i material escolar": [
        "Llibre", "Revista", "Diari", "Quadern / llibreta", "Agenda", "Carpeta", 
        "Arxivador", "Estoig escolar", "Bolígraf", "Llapis", "Retolador", 
        "Portamines", "Goma d'esborrar", "Maquineta de fer punta", "Regle", 
        "Escaire o cartabó", "Compàs", "Tisores", "Grapadora", "Cola de pegar", 
        "Material artístic / pintures", "Llenç", "Làmina o plànol", "Altres", "No identificable"
    ],
    "Alimentació i recipients": [
        "Ampolla reutilitzable", "Ampolla d'un sol ús", "Termo", "Got tèrmic", "Tassa", 
        "Got", "Tàper / carmanyola", "Caixa de menjar", "Coberts", "Recipient alimentari", 
        "Aliment envasat", "Aliment sense envasar", "Beguda envasada", "Altres", "No identificable"
    ],
    "Higiene i cura personal": [
        "Raspall de dents", "Dentifrici", "Pinta", "Raspall de cabells", "Cosmètic / maquillatge", 
        "Perfume / colònia", "Crema", "Protector solar", "Desodorant", "Producte d'higiene íntima", 
        "Mocadors de paper", "Tovalloletes", "Maquineta d'afaitar d'un sol ús", "Maquineta d'afaitar elèctrica", 
        "Tallacabells", "Assecador de cabells", "Planxa de cabells", "Arrissador", "Mirall de mà", 
        "Tallaungles", "Pinces", "Lents de contacte en envàs", "Estoig de lents de contacte", 
        "Mascareta", "Altres", "No identificable"
    ],
    "Salut i ajudes personals": [
        "Medicament en envàs", "Pastiller", "Inhalador", "Ploma d'injecció (insulina/adrenalina)", 
        "Material sanitari", "Farmaciola", "Termòmetre", "Mesurador sanitari (tensió/glucosa)", 
        "Audiòfon", "Pròtesi dental", "Pròtesi externa", "Òrtesi o fèrula", 
        "Bastó", "Muleta", "Caminador", "Cadira de rodes", "Coixí de suport", 
        "Altres", "No identificable"
    ],
    "Nadons i puericultura": [
        "Cotxet de nadó", "Cadireta de passeig", "Portanadons", "Cadira infantil", 
        "Biberó", "Xumet", "Mossegador", "Pitet", "Bolquer", "Canviador portàtil", 
        "Accessori de cotxet", "Altres", "No identificable"
    ],
    "Joguines i jocs": [
        "Peluix", "Nina", "Figura d'acció", "Vehicle de joguina", "Joguina de construcció", 
        "Joc de taula", "Baralla de cartes", "Trencaclosques / puzle", "Joguina electrònica", 
        "Joguina sensorial", "Pilota de joguina", "Altres", "No identificable"
    ],
    "Esport, platja i activitats a l'aire lliure": [
        "Pilota esportiva", "Raqueta", "Pala de pàdel", "Bat", "Pal de golf", "Estoreta (ioga/fitness)", 
        "Banda elàstica", "Pesa / manuella", "Corda de saltar", "Casc esportiu", "Protecció esportiva", 
        "Ulleres de natació", "Ulleres d'esquí", "Aleta de busseig", "Tub de busseig", 
        "Taula de natació", "Flotador", "Esquís", "Taula de surf de neu", "Bastó de senderisme", 
        "Canya de pescar", "Carret de pesca", "Sac de dormir", "Tenda de campanya", 
        "Llanterna", "Frontal de llum", "Brúixola", "Cadira plegable", "Matalàs de platja", 
        "Accessori esportiu", "Altres", "No identificable"
    ],
    "Mobilitat personal": [
        "Bicicleta", "Bicicleta elèctrica", "Patinet mecànic", "Patinet elèctric", 
        "Monopatí / skate", "Patins de línia o 4 rodes", "Monocicle", "Bomba d'inflat", 
        "Llum de bicicleta", "Component de bicicleta o patinet", "Altres", "No identificable"
    ],
    "Instruments musicals": [
        "Guitarra", "Uaquelale", "Violí", "Viola", "Violoncel", "Flauta", 
        "Clarinet", "Saxòfon", "Trompeta", "Harmònica", "Teclat musical / piano portàtil", 
        "Instrument de percussió", "Arc", "Baquetes", "Boquilla", "Afinador", 
        "Metrònom", "Faristol", "Altres", "No identificable"
    ],
    "Llar, decoració i tèxtils": [
        "Tovallola", "Manta", "Llençol", "Coixí de sofà", "Coixí de llit", "Cortina", 
        "Estovalles", "Drap de cuina", "Plat", "Bol", "Vaixella sencera", "Estri de cuina", 
        "Olla", "Paella", "Llum de sobretaula", "Bombeta", "Marc de foto", "Quadre", 
        "Mirall", "Figura decorativa", "Objecte religiós", "Glaçera / gerro", "Test", 
        "Planta", "Ram de flors", "Catifa", "Mobles petits", "Altres", "No identificable"
    ],
    "Aparells elèctrics i equips voluminosos": [
        "Televisor", "Monitor de pantalla", "Impressora", "Escàner", "Ordinador de sobretaula", 
        "Projector", "Planxa de roba", "Ventilador", "Calefactor", "Aspiradora", 
        "Cafetera", "Bullidor d'aigua", "Torradora", "Batedora", "Màquina de cosir", 
        "Altres", "No identificable"
    ],
    "Eines i material de treball": [
        "Martell", "Tornavís", "Alicates", "Clau d'eina (anglesa, fixa)", "Cinta mètrica", 
        "Nivell", "Trepat / trepant", "Tornavís elèctric", "Serra", "Cúter", 
        "Joc d'eines", "Caixa d'eines", "Brotxa", "Rodet de pintar", 
        "Material de ferreteria", "Peça mecànica", "Instrument de mesura", 
        "Altres", "No identificable"
    ],
    "Accessoris per a animals": [
        "Corretja", "Collar", "Arnès", "Transportí", "Muserola", "Menjadora", 
        "Abeurador", "Joguina d'animal", "Roba per a mascota", "Bossa de menjar per a animal", 
        "Altres", "No identificable"
    ],
    "Paquets i embalatges": [
        "Caixa tancada", "Paquet embolicat", "Sobre tancat", "Tub portadocumentació", 
        "Bossa de contingut no visible", "Embalatge buit", "Altres", "No identificable"
    ],
    "Altres objectes identificables": ["Altres"],
    "No identificable": ["No identificable"]
}

# -------------------------------------------------------------
# COLORS EN CATALÀ (I MAPEI AL VALOR CANÒNIC)
# -------------------------------------------------------------
# Mostrem l'etiqueta en català a l'usuari i guardem el canònic a la base de dades
COLORS_MAP = {
    "Negre": "negro",
    "Blanc": "blanco",
    "Gris": "gris",
    "Blau": "azul",
    "Verd": "verde",
    "Vermell": "rojo",
    "Groc": "amarillo",
    "Taronja": "naranja",
    "Rosa": "rosa",
    "Lila / Morat": "morado",
    "Marró": "marron",
    "Beix / Crema": "beige",
    "Daurat": "dorado",
    "Platejat": "plateado"
}

# -------------------------------------------------------------
# ETIQUETES DE DETALLS VISUALS EN CATALÀ
# -------------------------------------------------------------
ETIQUETES_DISPONIBLES = [
    # Estat visible
    "Estat: Amb rascades / esgarrapades",
    "Estat: Trencat / amb esquerdes",
    "Estat: Desgastat",
    "Estat: Amb taques / brut",
    "Estat: Peça absent o que falta",
    
    # Trets distintius
    "Trets: Amb adhesius / enganxines",
    "Trets: Amb pedaç / brodat",
    "Trets: Amb clauer",
    "Trets: Amb inicials o nom escrit",
    "Trets: Amb penjoll o adorn",
    "Trets: Logotip visible",
    
    # Materials i acabats
    "Material: Cuir / pell",
    "Material: Metall / metàl·lic",
    "Material: Plàstic / silicona",
    "Material: Teixit / roba",
    "Material: Fusta",
    "Material: Vidre / ceràmica",
    "Acabat: Brillant",
    "Acabat: Mate",
    "Acabat: Transparent / translúcid",
    "Acabat: Reflectant / fluorescent",
    
    # Estampats
    "Estampat: Llis",
    "Estampat: Ratlles",
    "Estampat: Quadres",
    "Estampat: Estampat floral",
    "Estampat: Dibuix / il·lustració",
    "Estampat: Multicolor",
    
    # Elements i tancament
    "Tancament: Cremallera",
    "Tancament: Botó / gafet",
    "Tancament: Velcro",
    "Tancament: Sivella",
    "Element: Nanses / tirants",
    "Element: Butxaques",
    "Element: Rodes",
    
    # Presentació
    "Presentació: Dins d'una funda",
    "Presentació: Plegat",
    "Presentació: En caixa / embalatge"
]

# -------------------------------------------------------------
# FORMULARI STREAMLIT
# -------------------------------------------------------------
with st.form("lost_object_form"):

    # 1. Dades de la pèrdua
    st.subheader("1. Dades de la pèrdua")
    loss_date = st.date_input("Dia de la pèrdua")
    transport = st.radio("Mitjà de transport", ["Metro", "Bus"])

    if transport == "Metro":
        lines = st.multiselect("Línia o línies de metro", METRO_LINES)
    else:
        lines = st.multiselect(
            "Línia o línies d'autobús", 
            BUS_LINES, 
            placeholder="Selecciona una o més línies (ex: D20, H6, V1, 59...)"
        )

    # 2. Característiques de l'objecte
    st.subheader("2. Característiques de l'objecte")
    category = st.selectbox("Categoria", list(TAXONOMIA.keys()))
    subcategory = st.selectbox("Subcategoria", TAXONOMIA[category])

    colors_selected = st.multiselect(
        "Colors principals (màxim 2)",
        list(COLORS_MAP.keys()),
        max_selections=2,
        placeholder="Tria fins a 2 colors"
    )

    brand = st.text_input("Marca (opcional, màx. 100 caràcters)", max_chars=100)

    # 3. Etiquetes i detalls visuals
    st.subheader("3. Detalls i etiquetes visuals")
    tags = st.multiselect(
        "Etiquetes opcionals de característiques de l'objecte",
        ETIQUETES_DISPONIBLES,
        placeholder="Afegeix etiquetes descriptives (estat, material, acabat...)"
    )

    description = st.text_area(
        "Descripció escrita / detalls addicionals (màx. 500 caràcters)",
        max_chars=500,
        help="Si la subcategoria triada és 'Altres', cal descriure l'objecte obligatòriament aquí."
    )

    photo = st.file_uploader(
        "Foto (opcional)", 
        type=["jpg", "jpeg", "png"]
    )

    # 4. Dades de contacte
    st.subheader("4. Dades de contacte")
    contact_email = st.text_input("Correu electrònic")
    contact_phone = st.text_input("Telèfon")

    consent = st.checkbox(
        "Autoritzo TMB a conservar les dades i contactar-me si es troba una coincidència."
    )

    submitted = st.form_submit_button("Enviar sol·licitud")

# -------------------------------------------------------------
# LÒGICA DE VALIDACIÓ I PROCESSAMENT
# -------------------------------------------------------------
if submitted:
    # Agrupar les etiquetes seleccionades i la descripció al camp detalls
    detalls_parts = []
    if tags:
        detalls_parts.append("Etiquetes: " + ", ".join(tags))
    if description.strip():
        detalls_parts.append(description.strip())
    detalles_finals = ". ".join(detalls_parts)

    # Mapeig dels colors triats al valor canònic que requereix el catàleg
    colores_canonicos = [COLORS_MAP[c] for c in colors_selected]

    # Prefix normalitzat de línies per a la base de dades
    linies_canoniques = [f"BUS_{l}" for l in lines] if transport == "Bus" else lines

    # Validacions
    if not category:
        st.error("Cal indicar una categoria.")
    elif subcategory == "Altres" and not detalles_finals.strip():
        st.error("Per a la subcategoria 'Altres' és obligatori afegir etiquetes o descriure l'objecte.")
    elif not consent:
        st.error("Cal donar consentiment per conservar la sol·licitud.")
    else:
        registre = {
            "categoria": category,
            "subcategoria": subcategory,
            "colores": colores_canonicos,
            "marca": brand.strip() if brand.strip() else None,
            "detalles": detalles_finals,
            "linea": linies_canoniques,
            "dia_de_perdua": str(loss_date),
            "contacte": {
                "email": contact_email.strip(),
                "telefon": contact_phone.strip()
            }
        }
        st.success("Sol·licitud registrada correctament.")
        st.json(registre)
