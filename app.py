import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Revisión Filológica de Desautomatizaciones", layout="wide")

# Intentar obtener el nombre del archivo de una variable de entorno o usar el valor por defecto
CSV_FILE = os.getenv('CSV_DATA_PATH', 'dp.csv')

def load_data():
    if os.path.exists(CSV_FILE):
        try:
            # Cargamos con separador punto y coma según el formato detectado
            df = pd.read_csv(CSV_FILE, sep=';')
            # Aseguramos que la columna Check exista y sea manejable
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

def main():
    st.title("🔍 Panel de Revisión Filológica")

    if 'df' not in st.session_state:
        st.session_state.df = load_data()
    
    df = st.session_state.df

    if df is None:
        st.info("Por favor, asegúrate de que el archivo dp.csv esté en la carpeta del proyecto.")
        return

    # Lógica para encontrar la primera fila no revisada al inicio
    if 'current_idx' not in st.session_state:
        # Buscamos filas donde Check es nulo o vacío
        non_reviewed = df[df['Check'].isna()]
        if not non_reviewed.empty:
            st.session_state.current_idx = non_reviewed.index[0]
        else:
            st.session_state.current_idx = 0 # Empezar por el principio si todo está revisado

    curr_idx = st.session_state.current_idx

    # --- BARRA DE PROGRESO ---
    total = len(df)
    revisados = df['Check'].notna().sum()
    progreso = revisados / total if total > 0 else 0
    
    st.progress(progreso)
    st.write(f"**Progreso:** {revisados} de {total} filas revisadas ({progreso:.1%})")

    if revisados == total and total > 0:
        st.success("🎉 ¡Felicitaciones! Todas las desautomatizaciones han sido revisadas.")

    # --- NAVEGACIÓN Y DATOS ---
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
        if val_check in ["1.0", "1", "1"]: status_label = "✅ Confirmada"
        elif val_check in ["0.0", "0", "0"]: status_label = "❌ Revocada"
        st.markdown(f"**Estado actual:** {status_label}")

    st.divider()

    # Paremia Canónica (Objeto de estudio)
    st.markdown(f"### Paremia Canónica")
    st.markdown(f"<h1 style='text-align: center; color: #1E88E5;'>{row.get('Paremia_Canonica', 'N/A')}</h1>", unsafe_allow_html=True)

    st.divider()

    # Formulario de edición
    with st.form(key=f"form_{curr_idx}"):
        # Desautomatización (Grande)
        new_desaut = st.text_area("Desautomatización", value=str(row.get('Desautomatizacion', '')), height=150)
        
        # Otros campos (Más pequeños)
        col1, col2 = st.columns(2)
        with col1:
            new_mecanismo = st.text_input("Mecanismo", value=str(row.get('Mecanismo', '') if pd.notna(row.get('Mecanismo')) else ""))
            new_mecanismos_sec = st.text_input("Mecanismos Secundarios", value=str(row.get('Mecanismos_Secundarios', '') if pd.notna(row.get('Mecanismos_Secundarios')) else ""))
            new_patron = st.text_input("Patrón Sintáctico", value=str(row.get('Patron_Sintactico', '') if pd.notna(row.get('Patron_Sintactico')) else ""))
        
        with col2:
            new_dominio = st.text_input("Dominio Meta", value=str(row.get('Dominio_Meta', '') if pd.notna(row.get('Dominio_Meta')) else ""))
            new_elementos = st.text_area("Elementos Sustituidos", value=str(row.get('Elementos_Sustituidos', '') if pd.notna(row.get('Elementos_Sustituidos')) else ""), height=108)

        # Botones Principales dentro del formulario
        c_btn1, c_btn2 = st.columns(2)
        confirmar = c_btn1.form_submit_button("✅ CONFIRMAR", use_container_width=True)
        revocar = c_btn2.form_submit_button("🚫 REVOCAR", use_container_width=True)

        if confirmar or revocar:
            # Actualizar valores en el dataframe
            df.at[curr_idx, 'Desautomatizacion'] = new_desaut
            df.at[curr_idx, 'Mecanismo'] = new_mecanismo
            df.at[curr_idx, 'Mecanismos_Secundarios'] = new_mecanismos_sec
            df.at[curr_idx, 'Patron_Sintactico'] = new_patron
            df.at[curr_idx, 'Dominio_Meta'] = new_dominio
            df.at[curr_idx, 'Elementos_Sustituidos'] = new_elementos
            
            # Asignar Check
            df.at[curr_idx, 'Check'] = 1 if confirmar else 0
            
            save_data(df)
            st.session_state.df = df
            
            # Avanzar automáticamente al siguiente "Pendiente" o al siguiente simple
            if curr_idx < total - 1:
                st.session_state.current_idx += 1
            st.rerun()

    # --- BOTONES DE NAVEGACIÓN SECUNDARIOS ---
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
        st.write(f"<p style='text-align: center;'>Fila {curr_idx + 1} de {total}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()