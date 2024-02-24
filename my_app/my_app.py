import streamlit as st
from db.neo4j_connection import Neo4jConnection
from queries.cypher_query_builder import CypherQueryBuilder
from ui.streamlit_ui import StreamlitUI




def load_search_page(db_connection):
    # Initialize the UI class with the database connection
    ui = StreamlitUI(db_connection)

    # Initialize CypherQueryBuilder instance
    query_builder = CypherQueryBuilder()
    label, date_from, date_to, num_results, variable_name, variable_value = ui.display_query_form()

    constructed_query = ""  # Initialize to avoid reference before assignment

    # Construct and display the query based on user inputs
    if st.button('Construct and Display Query'):
        # Check if specific variable search is enabled
        if variable_name and variable_value:
            constructed_query = query_builder.construct_variable_query(label, variable_name, variable_value, date_from, date_to, num_results)
        elif label and (date_from or date_to):
            # Assuming there's a method to handle this case
            constructed_query = query_builder.construct_query(label, None, date_from, date_to, num_results)
        else:
            # Handle other cases or show a message indicating that more input is needed
            st.write("Please provide more input to construct the query.")

        if constructed_query:  # Ensure we have a query to display
            st.code(constructed_query)  # Display the constructed query
            st.session_state['constructed_query'] = constructed_query  # Save in session state

    # Execute custom or constructed query
    custom_query = ui.display_direct_query_input()
    execute_section = st.container()
    with execute_section:
        if st.button('Execute Custom Query'):
            ui.execute_query(custom_query)
        elif 'constructed_query' in st.session_state and st.button('Execute Constructed Query'):
            ui.execute_query(st.session_state['constructed_query'])



def main():
    # Initialize Neo4j connection using Streamlit's session state
    if 'db_connection' not in st.session_state:
        uri = st.secrets["neo4j_uri"]
        user = st.secrets["neo4j_username"]
        pwd = st.secrets["neo4j_password"]
        st.session_state['db_connection'] = Neo4jConnection(uri, user, pwd)
    

    db_connection = st.session_state['db_connection']
    load_search_page(db_connection)
    # Define the navigation menu
    menu = ["Search App", "Semantic Search App", "Documentation"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Search":
        load_search_page(db_connection)
    elif choice == "Semantic Search":
        st.header("Welcome to Page 1")
        # Add content for Page 1 here
    elif choice == "Documentation":
        load_search_page()
        # Add content for Page 2 here


if __name__ == "__main__":
    main()