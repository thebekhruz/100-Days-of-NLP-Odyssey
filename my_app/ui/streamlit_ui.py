import streamlit as st
from queries.cypher_query_builder import CypherQueryBuilder 

class StreamlitUI:
    def __init__(self, db):
        self.db = db
        self.db.connect()



    def choose_entity_type(self):
        label_option = ["DOCUMENT ID", "LOCATION", "ORGANISATION", "PERSON", "EVENT"]
        label = st.selectbox("Choose an entity type (or None):", label_option, index=0)
        return label


    def choose_date_range(self):
        col1, col2 = st.columns(2)
        with col1:
            date_from_year_str = st.text_input("Date from:", key="from_year_txt")
        with col2:
            date_to_year_str = st.text_input("Date to:", key="to_year_txt")

        try:
            date_from_year = int(date_from_year_str) if date_from_year_str else None
        except ValueError:
            st.warning("Please enter a valid integer for 'Date from'.")
            date_from_year = None

        try:
            date_to_year = int(date_to_year_str) if date_to_year_str else None
        except ValueError:
            st.warning("Please enter a valid integer for 'Date to'.")
            date_to_year = None

        return date_from_year, date_to_year


    def display_query_form(self):
        """Renders UI elements for Cypher query input and returns the necessary components to build a query."""
        label, date_from, date_to, variable_name, variable_value  = None, None, None, None, None

        # Use a dict to map labels to their respective text inputs for efficiency
        entity_type_to_variables = {
            "DOCUMENT ID": ["doc_id", "text"],
            "PERSON": ["name", "wiki_ID"],
            "ORGANISATION": ["name", "wiki_ID"],
            "LOCATION": ["name", "wiki_ID"],
            "EVENT": ["name", "wiki_ID"],
        }

        # Simplified UI layout using Streamlit columns for options
        enable_options = st.columns(3)
        enable_entity_type = enable_options[0].checkbox("Enable Entity Type", value=False)
        enable_date_range = enable_options[1].checkbox("Enable Date Range", value=False)
        enable_specific_variable = enable_options[2].checkbox("Enable Specific Variable Search", value=False, disabled=not enable_entity_type)

        # Conditional UI elements based on user selections
        if enable_entity_type:
            label = self.choose_entity_type()

        if enable_date_range:
            date_from, date_to = self.choose_date_range()

        if enable_specific_variable and label:
                variable_options = entity_type_to_variables.get(label, [])
                if variable_options:
                    variable_name = st.selectbox("Select variable name:", options=variable_options, key="variable_name")
                    variable_value = st.text_input("Enter variable value:", key="variable_value")

        num_results = st.number_input("Number of results to display:", min_value=1, max_value=100, value=10, key="num_results")

        # Adjusted return statement to include the new inputs
        return label, date_from, date_to, num_results, variable_name, variable_value




    def display_direct_query_input(self):
        """Renders a text area for inputting a direct Cypher query."""
        return st.text_area("Or, enter your Cypher query here:", height=150)
    

    def display_results_in_table(self, results):
        """Displays query results in a Streamlit table."""
        if results:
            table_data = []
            for record in results:
                # 'n' is the variable name for the node in the Cypher query
                node = record['n']
                row = {'labels': ', '.join(node.labels),}
                row.update(node._properties)
                table_data.append(row)

            st.json(table_data)
        else:
            st.write("No results found.")


    def execute_query(self, query):
        """Executes the provided query and displays the results."""
        try:

            results = self.db.query(query)
            if results:
                self.display_results_in_table(results)
            else:
                st.write("No results found.")

        except Exception as e:
            st.error(f"Execution error: {e}")


