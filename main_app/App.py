import streamlit as st
from db.neo4j_connection import Neo4jConnection, Neo4jConnector

from ui.sidebar_ui import SidebarUI
from ui.container_ui import ContainerUI

st.set_page_config(page_title="Document Search",
                    page_icon="🕵🏽‍♂️",
                    layout="wide",
                    initial_sidebar_state="expanded")

class App:
    def __init__(self):
        """Initializes the application, ensuring the database connection is established."""
        if 'initialized' not in st.session_state:
            st.session_state['neo4j_connection'] = Neo4jConnector.initialize_connection()
            st.session_state['initialized'] = True


    def run(self):
        """Runs the main application logic."""


        sidebar = SidebarUI()
        container = ContainerUI()
        selected_entity, selected_relationship, target_entity, number_of_results_to_explore, outputType = sidebar.get_sidebar()
        
        st.write(f"Selected Entity: {selected_entity.name},\n Selected Relationship: {selected_relationship.name},\n Target Entity: {target_entity.name},\n Number of Results: {number_of_results_to_explore},\n Output Type: {outputType}")
        
        container.get_filters(subject=selected_entity, target=target_entity)

        container.display_search_and_filter_buttons(st.session_state['db_connection'])


    def semantic_search(self):
        from neo4j import GraphDatabase
        query = st.text_input('Input your query here:')
        

        driver = Neo4jConnector()
        driver.initialize_connection()





if __name__ == "__main__":
    app = App()
    app.run()
    # app.semantic_search()

    # people = DOCUMENT.mentions_person.fil
    # documents = get_10_documents_with_person_mentions()
 
#     db_connection = st.session_state['db_connection']
    
#     test(db_connection)
#     # new_form(db_connection)
#     # load_search_page(db_connection)
#     # Define the navigation menu
#     menu = ["Search App", "Semantic Search App", "Documentation"]
#     choice = st.sidebar.selectbox("Menu", menu)
#     if choice == "Search":
#         load_search_page(db_connection)
#     elif choice == "Semantic Search":
#         st.header("Welcome to Page 1")
#         # Add content for Page 1 here
#     elif choice == "Documentation":
#         load_search_page()
#         # Add content for Page 2 here


# def load_search_page(db_connection):
#     # Initialize the UI class with the database connection
#     ui = StreamlitUI(db_connection)

#     # Initialize CypherQueryBuilder instance
#     label, date_from, date_to, num_results, variable_name, variable_value = ui.display_query_form()
#     ui.construct_and_display_query(label, variable_name, variable_value, date_from, date_to, num_results)


#     # Execute custom or constructed query
#     custom_query = ui.display_direct_query_input()
#     execute_section = st.container()
#     with execute_section:
#         if st.button('Execute Custom Query'):
#             ui.execute_query(custom_query)


# def new_form(db_connection):
#     ui = StreamlitUI(db_connection)
#     ui.display_form()

# def test(db_connection):
#     all_nodes = PERSON.nodes.get(doc_id = 1)
#     st.wrtie(all_nodes)
# def get_10_documents_with_person_mentions():
#     for document in DOCUMENT.nodes:
#         if document.mentions_person:
#             st.write(document)



