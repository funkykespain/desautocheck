import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Revisión Filológica de Desautomatizaciones", layout="wide")

# Intentar obtener el nombre del archivo de una variable de entorno o usar el valor por defecto
CSV_FILE = os.getenv('CSV_DATA_PATH', 'dp.csv')

MECANISMOS = [
    "",
    "Adición",
    "Anacoluto",
    "Cita",
    "Fusión",
    "Metalogismo",
    "Metaplasmo",
    "Negación",
    "Negación Semántica",
    "Permutación",
    "Sustitución",
    "Truncamiento",
]

DOMINIOS_META = [
    "",
    "Agricultura/Ganadería",
    "Alimentación",
    "Alimentación/Gastronomía",
    "Arte y Realidad",
    "Cine/Entretenimiento",
    "Cine/Literatura",
    "Clima/Meteorología",
    "Cocina",
    "Comercial",
    "Comercial/Promociones",
    "Comercio/Marketing",
    "Compras/Descuentos",
    "Comunicación/Idiomas",
    "Comunicación/Medios",
    "Comunicación/Política",
    "Comunicación/Relaciones",
    "Conducción",
    "Construcción/Arquitectura",
    "Crítica Social",
    "Cultura/Regional",
    "Deportes",
    "Deportes/Atletismo",
    "Deportes/Economía",
    "Deportes/Entrenadores",
    "Deportes/Fútbol",
    "Deportes/Golf",
    "Economía",
    "Economía/Comercio",
    "Economía/Construcción",
    "Economía/Emprendimiento",
    "Economía/Finanzas",
    "Economía/Moneda",
    "Economía/Política",
    "Economía/Social",
    "Educación",
    "Educación/Familia",
    "Educación/Lenguas",
    "Entretenimiento/Internet",
    "Estrategia/Batalla",
    "Fama/Medios",
    "Filosofía/Realidad",
    "Filosofía/Religión",
    "Filosofía/Sociología",
    "Fotografía",
    "Física",
    "Gastronomía",
    "General",
    "General/Coloquial",
    "General/Deportivo",
    "General/Insulto",
    "General/Intelectual",
    "Geografía",
    "Geografía/Control",
    "Geografía/Cultura",
    "Geografía/Historia",
    "Geografía/Topónimos",
    "Geografía/Ubicación",
    "Geografía/Viajes",
    "Geográfico",
    "Geográfico/Local",
    "Intelecto/Conocimiento",
    "Juegos/Azarte",
    "Legislación",
    "Lenguaje y Comunicación",
    "Lingüística/Cultura",
    "Lingüístico/Literario",
    "Literatura",
    "Literatura/Edición",
    "Literatura/Lectura",
    "Literatura/Poesía",
    "Literatura/Referencia Cultural",
    "Marketing/Empresas",
    "Medio Ambiente",
    "Medio Ambiente/Ecología",
    "Medios de Comunicación",
    "Medios de Comunicación y Ética",
    "Medios de Comunicación/Entretenimiento",
    "Medios de comunicación",
    "Moda/Comercio",
    "Moda/Marcas",
    "Moral/Social",
    "Música",
    "Música/Emociones",
    "Música/Entretenimiento",
    "Música/Folklore",
    "Política",
    "Política/Actualidad",
    "Política/Comunicación",
    "Política/Elecciones",
    "Política/Geografía",
    "Política/Internacional",
    "Política/Opinión",
    "Política/Social",
    "Política/Sociedad",
    "Publicidad/Anuncios",
    "Publicidad/Marketing",
    "Publicidad/Salud",
    "Redes Sociales",
    "Redes Sociales/Influencers",
    "Redes Sociales/Medios",
    "Redes Sociales/Profesionales",
    "Relaciones Familiares",
    "Relaciones Interpersonales",
    "Relaciones Sociales",
    "Relaciones personales",
    "Religión",
    "Religión y Pasión",
    "Religión/Familia",
    "Religión/Filosofía",
    "Religión/Ironía",
    "Salud/Longevidad",
    "Salud/Medicina",
    "Seducción/Relaciones",
    "Sexualidad",
    "Social",
    "Sociología",
    "Tecnología/Aviación no tripulada",
    "Tecnología/Comunicación",
    "Tecnología/Información",
    "Tecnología/Informática",
    "Tecnología/Internet",
    "Tecnología/Medios",
    "Tecnología/Música",
    "Tecnología/Resiliencia",
    "Tecnología/Virtualidad",
    "Teoría/Filosofía",
    "Transporte/Innovación",
    "Turismo/Ferias",
    "Turismo/Geografía",
    "Turismo/Viajes",
    "Urbanismo/Limpieza",
    "Valoración/Economía",
    "Velocidad/Movimiento",
    "Ética/Moral",
]


def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE, sep=';')
            if 'Check' not in df.columns:
                df['Check'] = None
            return df
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            return None
    else:
        st.error(f"No se encontró el archivo {CSV_FILE} en la ruta especificada.")
        return None


def save_data(df):
    try:
        df.to_csv(CSV_FILE, sep=';', index=False)
    except Exception as e:
        st.error(f"Error al guardar los datos: {e}")


def safe_index(options, value):
    """Devuelve el índice del valor en la lista, o 0 si no se encuentra."""
    val = str(value).strip() if pd.notna(value) and str(value).strip() != "nan" else ""
    return options.index(val) if val in options else 0


def main():
    # CSS para reducir espacios verticales globales
    st.markdown("""
        <style>
            .block-container { padding-top: 1rem !important; padding-bottom: 0.5rem !important; }
            h1 { margin-bottom: 0 !important; font-size: 1.6rem !important; }
            .stProgress { margin-bottom: 0.2rem !important; }
            .stAlert { padding: 0.4rem 0.6rem !important; }
            div[data-testid="stVerticalBlock"] > div { gap: 0.3rem !important; }
            hr { margin: 0.4rem 0 !important; }
            .stTextArea textarea { min-height: 60px !important; }
            .stForm { padding: 0.5rem !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 Panel de Revisión Filológica")

    if 'df' not in st.session_state:
        st.session_state.df = load_data()

    df = st.session_state.df

    if df is None:
        st.info("Por favor, asegúrate de que el archivo dp.csv esté en la carpeta del proyecto.")
        return

    if 'current_idx' not in st.session_state:
        non_reviewed = df[df['Check'].isna()]
        if not non_reviewed.empty:
            st.session_state.current_idx = non_reviewed.index[0]
        else:
            st.session_state.current_idx = 0

    curr_idx = st.session_state.current_idx

    # --- BARRA DE PROGRESO ---
    total = len(df)
    revisados = df['Check'].notna().sum()
    progreso = revisados / total if total > 0 else 0

    st.progress(progreso)
    st.caption(f"Progreso: {revisados} de {total} filas revisadas ({progreso:.1%})")

    if revisados == total and total > 0:
        st.success("🎉 ¡Felicitaciones! Todas las desautomatizaciones han sido revisadas.")

    if total == 0:
        st.warning("El archivo CSV parece estar vacío.")
        return

    row = df.iloc[curr_idx]

    # Información ID superior
    col_id1, col_id2, col_status = st.columns([1, 1, 2])
    with col_id1:
        st.info(f"**ID_Ref:** {row.get('ID_Ref', 'N/A')}")
    with col_id2:
        st.info(f"**Paremia_ID:** {row.get('Paremia_ID', 'N/A')}")
    with col_status:
        val_check = str(row.get('Check', ''))
        status_label = "⏳ Pendiente"
        if val_check in ["1.0", "1"]:
            status_label = "✅ Confirmada"
        elif val_check in ["0.0", "0"]:
            status_label = "❌ Revocada"
        st.markdown(f"**Estado actual:** {status_label}")

    st.divider()

    # Paremia Canónica
    st.markdown(
        f"<p style='text-align:center; color:#1E88E5; font-size:1.5rem; font-weight:700; margin:0.2rem 0 0.4rem 0;'>"
        f"{row.get('Paremia_Canonica', 'N/A')}</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # Formulario de edición
    with st.form(key=f"form_{curr_idx}"):
        new_desaut = st.text_area(
            "Desautomatización candidata",
            value=str(row.get('Desautomatizacion', '')),
            height=90,
            help=(
                "Texto extraído del corpus en el que la paremia canónica aparece modificada. "
                "Revisa que la modificación sea real e intencional, no un error tipográfico o paráfrasis casual."
            ),
        )

        col1, col2 = st.columns(2)
        with col1:
            new_mecanismo = st.selectbox(
                "Mecanismo Principal",
                options=MECANISMOS,
                index=safe_index(MECANISMOS, row.get('Mecanismo')),
                help=(
                    "Procedimiento retórico o lingüístico predominante mediante el cual se produce la desautomatización. "
                    "Elige el que mejor explique la transformación central del enunciado."
                ),
            )
            new_mecanismos_sec = st.text_input(
                "Mecanismos Secundarios",
                value=str(row.get('Mecanismos_Secundarios', '') if pd.notna(row.get('Mecanismos_Secundarios')) else ""),
                help=(
                    "Si la desautomatización combina más de un procedimiento, anota aquí los complementarios separados por coma. "
                    "Déjalo vacío si solo opera un mecanismo."
                ),
            )
            new_patron = st.text_input(
                "Patrón Sintáctico",
                value=str(row.get('Patron_Sintactico', '') if pd.notna(row.get('Patron_Sintactico')) else ""),
                help=(
                    "Estructura gramatical esquemática de la desautomatización (p. ej. SN + V + Adj). "
                    "Ayuda a identificar recurrencias estructurales entre ejemplos distintos."
                ),
            )

        with col2:
            new_dominio = st.selectbox(
                "Dominio Meta",
                options=DOMINIOS_META,
                index=safe_index(DOMINIOS_META, row.get('Dominio_Meta')),
                accept_new_options=True,
                help=(
                    "Ámbito temático o discursivo al que apunta la desautomatización en su contexto "
                    "(economía, política, gastronomía…). Refleja el tema del texto donde aparece, "
                    "no el de la paremia original. Puedes escribir un dominio nuevo si no está en la lista."
                ),
            )
            new_elementos = st.text_area(
                "Elementos Sustituidos",
                value=str(row.get('Elementos_Sustituidos', '') if pd.notna(row.get('Elementos_Sustituidos')) else ""),
                height=70,
                help=(
                    "Palabras o segmentos de la paremia canónica que han sido reemplazados, añadidos o suprimidos. "
                    "Anótalos en el orden en que aparecen en la paremia original, separados por → si hay sustitución directa "
                    "(p. ej. perro → gato)."
                ),
            )

        c_btn1, c_btn2 = st.columns(2)
        confirmar = c_btn1.form_submit_button("✅ CONFIRMAR", use_container_width=True)
        revocar = c_btn2.form_submit_button("🚫 REVOCAR", use_container_width=True)

        if confirmar or revocar:
            df.at[curr_idx, 'Desautomatizacion'] = new_desaut
            df.at[curr_idx, 'Mecanismo'] = new_mecanismo
            df.at[curr_idx, 'Mecanismos_Secundarios'] = new_mecanismos_sec
            df.at[curr_idx, 'Patron_Sintactico'] = new_patron
            df.at[curr_idx, 'Dominio_Meta'] = new_dominio
            df.at[curr_idx, 'Elementos_Sustituidos'] = new_elementos
            df.at[curr_idx, 'Check'] = 1 if confirmar else 0

            save_data(df)
            st.session_state.df = df

            if curr_idx < total - 1:
                st.session_state.current_idx += 1
            st.rerun()

    # --- BOTONES DE NAVEGACIÓN ---
    st.write("---")
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

    with nav_col1:
        if st.button("⬅️ Atrás", use_container_width=True):
            if curr_idx > 0:
                st.session_state.current_idx -= 1
                st.rerun()

    with nav_col3:
        if st.button("Adelante ➡️", use_container_width=True):
            if curr_idx < total - 1:
                st.session_state.current_idx += 1
                st.rerun()

    with nav_col2:
        st.write(
            f"<p style='text-align: center;'>Fila {curr_idx + 1} de {total}</p>",
            unsafe_allow_html=True,
        )

    # --- BOTÓN DE DESCARGA ---
    st.sidebar.divider()
    st.sidebar.subheader("Exportar resultados")
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "rb") as file:
            st.sidebar.download_button(
                label="📥 Descargar CSV final",
                data=file,
                file_name="dp_revisado.csv",
                mime="text/csv",
            )
    else:
        st.sidebar.warning("No se encontró el archivo CSV para exportar.")


if __name__ == "__main__":
    main()