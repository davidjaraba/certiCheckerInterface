import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000/api"


def get_company(company_id):
    """Obtiene y muestra un certificado."""
    response = requests.get(f"{API_URL}/companies/{company_id}?last_certs=true")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error al obtener la compañia')
        return []


def get_company_urls(company_id):
    """Obtiene el URLs de los """
    response = requests.get(f"{API_URL}/urls/?company_id={company_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error al obtener')
        return []


def create_company(company_id, url):
    """Crea un nuevo certificado."""
    response = requests.post(f"{API_URL}/urls", json={"url": url, "company_id": company_id})
    if response.status_code == 201:
        st.success(f'Company creada con éxito')
        return True
    else:
        st.error(f'Error al crear el company ' + response.text)
        return False


def main():
    company_id = st.query_params['id']
    company = get_company(company_id)

    if company:
        st.title(company['name'])

        ass_urls = get_company_urls(company_id)

        if ass_urls:
            df = pd.DataFrame(ass_urls)

            # Mostrar el título de la sección
            st.markdown("### URLs Asociadas")

            # Iterar sobre cada fila del DataFrame para crear y mostrar cada enlace como un elemento de la lista
            for index, row in df.iterrows():
                # Formatear la URL y el nombre de la compañía en un enlace HTML
                link = f'- <a href="companies/?id={row["url"]}" target="_blank">{row["url"]}</a>'
                # Mostrar el enlace con Markdown en Streamlit
                st.markdown(link, unsafe_allow_html=True)

        with st.form("new_url"):
            url = st.text_input("URL")
            submit_button = st.form_submit_button("Crear URL")
            if submit_button and url and company_id:
                create_company(company_id, url)
                st.experimental_rerun()

        if company['companycertificates']:
            st.markdown(f"### Certificados encontrados {len(company['companycertificates'])}")
            sorted_certificates = sorted(company['companycertificates'],
                                         key=lambda cert: cert.get('certificate', {}).get('name',
                                                                                          'Unknown Certificate'))
            for cert in sorted_certificates:
                # Asumimos que cada 'cert' es un diccionario con 'certificate_name' y 'url'
                cert_data = cert.get('certificate', 'Unknown Certificate')
                cert_name = cert_data.get('name', 'Unknown Certificate')
                resource_id = cert.get('resource_id', 'NORESOURCE')
                if resource_id:
                    link = f'{cert_name} - <a href="../resources/?id={resource_id}" target="_blank">Ver certificado</a>'
                    # Mostrar el enlace con Markdown en Streamlit
                    st.markdown(link, unsafe_allow_html=True)
                else:
                    st.markdown(f"- **{cert_name}**: No disponible")
        else:
            st.markdown("### No se encontraron certificados")


if __name__ == "__main__":
    main()
