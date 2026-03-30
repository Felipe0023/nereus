import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuración de la página
st.set_page_config(page_title="NEREUS Web", layout="wide")

# 1. Estilo y Logo
st.image("https://cdn-icons-png.flaticon.com/512/3175/3175211.png", width=100)
st.title("NEREUS Geo-Analytics Panel")

# 2. Sidebar (Barra lateral) para Entradas y Parámetros
st.sidebar.header("1. Configuración")
uploaded_file = st.sidebar.file_uploader("Subir CSV de Datos", type=["csv"])

st.sidebar.header("2. Parámetros")
v1 = st.sidebar.number_input("Ancho Longitud/Latitud", value=1000)
v2 = st.sidebar.number_input("Intervalo Profundidad", value=20)

# 3. Lógica Principal
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Procesamiento rápido
    if 'K' in df.columns:
        df['log10_K'] = np.log10(df['K'].replace(0, 1e-10))
    
    # Mostrar Estadísticas
    st.subheader("Resumen de Datos")
    col1, col2 = st.columns(2)
    col1.metric("Total Registros", len(df))
    
    if 'Tipo_Roca' in df.columns:
        st.write("Frecuencia por Tipo de Roca:")
        st.dataframe(df['Tipo_Roca'].value_counts())

    # Gráfico 3D Interactivo
    st.subheader("Visualización 3D: Permeabilidad")
    if all(c in df.columns for c in ['Longitud', 'Latitud', 'Altitud', 'log10_K']):
        fig = px.scatter_3d(df, x='Longitud', y='Latitud', z='Altitud',
                            color='log10_K', title="Modelo de Permeabilidad",
                            color_continuous_scale='Turbo')
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Esperando que se suba un archivo CSV...")


