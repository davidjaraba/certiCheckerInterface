import streamlit as st
import requests
import pandas as pd

st.title("CERTI CHECKER")

API_URL = "http://localhost:8000/api"  # Cambia esto por la URL de tu API


def list(ent):
    """Obtiene y muestra la lista de certificados."""
    response = requests.get(f"{API_URL}/{ent}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error al obtener los {ent}')
        return []


def create(ent, json):
    """Crea un nuevo certificado."""
    response = requests.post(f"{API_URL}/{ent}", json=json)
    if response.status_code == 201:
        st.success(f'{ent} creado con éxito')
        return True
    else:
        st.error(f'Error al crear el {ent}')
        return False


def delete(ent, cert_id):
    """Elimina un certificado."""
    response = requests.delete(f"{API_URL}/{ent}/{cert_id}")
    if response.status_code == 204:
        st.success(f'{ent} eliminado con éxito')
        return True
    else:
        st.error(f'Error al eliminar el {ent}'+response.text)
        return False


def update(ent, cert_id, json):
    """Actualiza un certificado."""
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f"{API_URL}/{ent}/{cert_id}", json=json, headers=headers)
    if response.status_code == 200:
        st.success(f'{ent} actualizado con exito.')
        return True
    else:
        st.error('Error al actualizar ')
        return False

def manage_certificates():
    entity = 'certificates'
    # Formulario para crear un nuevo certificado
    with st.form("new_certificate"):
        name = st.text_input("Nombre del Certificado")
        submit_button = st.form_submit_button("Crear Certificado")
        if submit_button and name:
            create(entity, {"name": name})
            st.experimental_rerun()

    # Mostrar lista de certificados
    st.header("Lista de Certificados")
    certificates = list(entity)
    if certificates:
        df = pd.DataFrame(certificates)
        st.dataframe(df[['name']])  # Mostrar solo el nombre en la tabla

    # Formulario para eliminar un certificado
    st.header("Eliminar Certificado")
    if certificates:
        cert_names = [cert['name'] for cert in certificates]
        cert_id_map = {cert['name']: cert['id'] for cert in certificates}
        selected_cert = st.selectbox("Seleccione el Certificado a eliminar", cert_names, key='delete')
        if st.button("Eliminar Certificado"):
            cert_id = cert_id_map[selected_cert]
            if delete(entity, cert_id):
                st.experimental_rerun()

    # Formulario para editar un certificado
    st.header("Editar Certificado")
    if certificates:
        editable_cert_name = st.selectbox("Seleccione el Certificado a editar", cert_names, key='edit')
        new_name = st.text_input("Nuevo Nombre del Certificado", value=editable_cert_name, key='new_name')
        if st.button("Guardar Cambios"):
            cert_id = cert_id_map[editable_cert_name]
            if update(entity, cert_id, {"name": new_name}):
                st.experimental_rerun()


def manage_companies():
    entity = 'companies'

    # Formulario para crear una nueva compañía
    with st.form("new_company"):
        name = st.text_input("Nombre de la Compañía")
        submit_button = st.form_submit_button("Crear Compañía")
        if submit_button and name:
            create(entity, {"name": name})
            st.experimental_rerun()

    # Mostrar lista de compañías
    st.header("Lista de Compañías")
    companies = list(entity)
    if companies:
        df = pd.DataFrame(companies)
        st.dataframe(df[['name']])  # Mostrar solo el nombre en la tabla

    # Formulario para eliminar una compañía
    st.header("Eliminar Compañía")
    if companies:
        company_names = [company['name'] for company in companies]
        company_id_map = {company['name']: company['id'] for company in companies}
        selected_company = st.selectbox("Seleccione la Compañía a eliminar", company_names, key='delete_company')
        if st.button("Eliminar Compañía"):
            company_id = company_id_map[selected_company]
            if delete(entity, company_id):
                st.experimental_rerun()

    # Formulario para editar una compañía
    st.header("Editar Compañía")
    if companies:
        editable_company_name = st.selectbox("Seleccione la Compañía a editar", company_names, key='edit_company')
        new_name = st.text_input("Nuevo Nombre de la Compañía", value=editable_company_name, key='new_company_name')
        if st.button("Guardar Cambios"):
            company_id = company_id_map[editable_company_name]
            if update(entity, company_id, {"name": new_name}):
                st.experimental_rerun()


def manage_urls():
    entity = 'urls'

    # Formulario para crear una nueva URL
    with st.form("new_url"):
        url = st.text_input("URL")
        company_id = st.selectbox("Seleccionar Compañía", [company['id'] for company in list('companies')],
                                  format_func=lambda x: f"ID: {x}")
        submit_button = st.form_submit_button("Crear URL")
        if submit_button and url and company_id:
            create(entity, {"url": url, "company_id": company_id})
            st.experimental_rerun()

    # Mostrar lista de URLs
    st.header("Lista de URLs")
    urls = list(entity)
    companies = list('companies')
    if urls:
        df = pd.DataFrame(urls)
        df['company_name'] = df['company_id'].apply(lambda x: next((item['name'] for item in companies if item['id'] == x), None))
        st.dataframe(df[['url', 'company_name']])

    # Formulario para eliminar una URL
    st.header("Eliminar URL")
    if urls:
        url_names = [url['url'] for url in urls]
        selected_url = st.selectbox("Seleccione la URL a eliminar", url_names, key='delete_url')
        if st.button("Eliminar URL"):
            if delete(entity, selected_url):
                st.experimental_rerun()

    st.header("Editar Asignación de Compañía para URL")
    if urls:
        # Crear una lista de URLs para seleccionar
        url_names = [url['url'] for url in urls]
        selected_url = st.selectbox("Seleccione la URL para editar su compañía asignada", url_names, key='edit_url')

        # Cargar las compañías disponibles para asignación
        companies = list('companies')  # Asegúrate de que esta función devuelve correctamente las compañías
        company_ids = [company['id'] for company in companies]
        company_names = [company['name'] for company in companies]
        company_id_map = {company['name']: company['id'] for company in companies}

        # Seleccionar la nueva compañía para la URL seleccionada
        default_index = company_ids.index(urls[url_names.index(selected_url)][
                                              'company_id'])  # Encuentra el índice actual de la compañía para establecer como predeterminado
        new_company = st.selectbox("Seleccione la nueva compañía para la URL", company_names, index=default_index,
                                   format_func=lambda x: f"ID: {company_id_map[x]} - {x}")

        # Botón para guardar cambios
        if st.button("Guardar Cambios de Compañía"):
            new_company_id = company_id_map[new_company]
            if update(entity, selected_url, {"company_id": new_company_id}):
                st.experimental_rerun()


def manage_resources():
    entity = 'resources'
    resource_types = ['IMG', 'DOC', 'HTML']

    # Formulario para crear un nuevo recurso
    with st.form("new_resource"):
        resource_type = st.selectbox("Seleccionar tipo", resource_types, format_func=lambda x: x)
        url_id = st.selectbox("Seleccionar URL", [url['url'] for url in list('urls')], format_func=lambda x: x)
        path_file = st.text_input("Ruta del Archivo")
        submit_button = st.form_submit_button("Crear Recurso")
        if submit_button and resource_type and url_id and path_file:
            create(entity, {"type": resource_type, "url_id": url_id, "path_file": path_file})
            st.experimental_rerun()

    # Mostrar lista de recursos
    st.header("Lista de Recursos")
    resources = list(entity)
    if resources:
        df = pd.DataFrame(resources)
        st.dataframe(df[['type', 'url_id', 'path_file']])  # Mostrar datos esenciales del recurso

    # Formulario para eliminar un recurso
    st.header("Eliminar Recurso")
    if resources:
        resource_ids = [resource['id'] for resource in resources]
        selected_resource = st.selectbox("Seleccione el Recurso a eliminar", resource_ids, key='delete_resource')
        if st.button("Eliminar Recurso"):
            if delete(entity, selected_resource):
                st.experimental_rerun()

    # Formulario para editar un recurso
    st.header("Editar Recurso")
    if resources:
        editable_resource_id = st.selectbox("Seleccione el Recurso a editar", resource_ids, key='edit_resource')
        editable_resource = next((res for res in resources if res['id'] == editable_resource_id), None)
        # new_type = st.text_input("Nuevo Tipo de Recurso", value=editable_resource['type'], key='new_type')
        default_index = resource_types.index(editable_resource['type'])
        new_type = st.selectbox("Seleccionar tipo", resource_types, format_func=lambda x: x,
                                index=default_index, key='new_type')
        new_path_file = st.text_input("Nueva Ruta del Archivo", value=editable_resource['path_file'],
                                      key='new_path_file')
        if st.button("Guardar Cambios"):
            update_data = {"type": new_type, "path_file": new_path_file}
            if update(entity, editable_resource_id, update_data):
                st.experimental_rerun()

def main():
    st.title('Administración')
    # if 'current_page' not in st.session_state:
    #     st.session_state['current_page'] = 'home'

    # Crea un menú lateral para la navegación
    page = st.sidebar.radio("Navegar a", ('Administrar Certificados', 'Administrar Compañías', 'Administrar URLs', 'Administrar Recursos'))

    # Actualiza la página actual basada en la selección del usuario
    if page == 'Inicio':
        st.session_state['current_page'] = 'home'
    elif page == 'Administrar Certificados':
        st.session_state['current_page'] = 'certificates'
    elif page == 'Administrar Compañías':
        st.session_state['current_page'] = 'companies'
    elif page == 'Administrar URLs':
        st.session_state['current_page'] = 'urls'
    elif page == 'Administrar Recursos':
        st.session_state['current_page'] = 'resources'


    if st.session_state['current_page'] == 'certificates':
        manage_certificates()
    elif st.session_state['current_page'] == 'companies':
        manage_companies()
    elif st.session_state['current_page'] == 'urls':
        manage_urls()
    elif st.session_state['current_page'] == 'resources':
        manage_resources()
    # elif st.session_state['current_page'] == 'other_model':





if __name__ == "__main__":
    main()
