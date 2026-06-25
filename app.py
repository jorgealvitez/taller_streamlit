import streamlit as st
import pandas as pd
import requests
from io import BytesIO, StringIO

st.title("Extractor de tablas desde una URL")

url = st.text_input("Ingresa el enlace de la página web:")

if st.button("Extraer tablas"):
    if not url:
        st.warning("Por favor ingresa una URL.")
    else:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            tablas = pd.read_html(StringIO(response.text))

            if not tablas:
                st.warning("No se encontraron tablas en esa página.")
            else:
                st.success(f"Se encontraron {len(tablas)} tabla(s).")
                st.session_state["tablas"] = tablas

        except Exception as e:
            st.error(f"Error al procesar la página: {e}")

if "tablas" in st.session_state:
    tablas = st.session_state["tablas"]

    for i, df in enumerate(tablas):
        st.subheader(f"Tabla {i + 1}")
        st.dataframe(df)

    # Generar Excel con todas las tablas en hojas separadas
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for i, df in enumerate(tablas):
            df.to_excel(writer, sheet_name=f"Tabla_{i + 1}", index=False)

    st.download_button(
        label="Descargar todas las tablas en Excel",
        data=buffer.getvalue(),
        file_name="tablas_extraidas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
