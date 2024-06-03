import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000/api"


class Home:
    def __init__(self):
        st.title("CERTI Checker")


def list(ent):
    """Obtiene y muestra la lista de certificados."""
    response = requests.get(f"{API_URL}/{ent}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error al obtener los {ent}')
        return []


def main():
    st.set_page_config(
        page_title="Certi Checker",
        page_icon="♥"
    )

    st.header("CERTI Checker")

    st.write('En un mundo donde la sostenibilidad es más crucial que nunca, EcoCert Tracker emerge como tu aliado '
             'confiable para descubrir y validar certificados de sostenibilidad en sitios web de empresas y '
             'productos. Nuestra misión es empoderarte con información precisa y actualizada para que puedas tomar '
             'decisiones informadas sobre a quién apoyar en el mercado.')

    st.subheader("Empresas")

    companies = list('companies')
    if companies:
        # Convertimos la lista de diccionarios a un DataFrame
        df = pd.DataFrame(companies)

        # Crear una nueva columna en el DataFrame que formatea los nombres como enlaces HTML
        df['link'] = df.apply(lambda row: f'<a href="companies/?id={row["id"]}" target="_blank">{row["name"]}</a>',
                              axis=1)

        # Mostrar los nombres como enlaces clicables en Streamlit usando Markdown
        st.markdown("### Lista de Compañías")
        st.markdown(df[['link']].to_html(escape=False, index=False), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
