import streamlit as st
from queries.cypher_query_builder import CypherQueryBuilder 
from streamlit_agraph import agraph, Node, Edge
from streamlit_agraph import agraph, Node, Edge, Config
# from db.models import *


class Entity:
    def __init__(self, entity_id):
        self.id = entity_id
        self.label = None
        self.relationship = None
        self.related_entity = None
        self.date_from_year = None
        self.date_to_year = None
        self.attribute_name = None
        self.attribute_value = None

class StreamlitUI:
    LABEL_OPTIONS = ["DOCUMENT ID", "LOCATION", "ORGANISATION", "PERSON", "EVENT"]
    CONNECTION_TYPES = ["Direct", "Indirect"]
    LABEL_MAPPING = {
        "DOCUMENT ID": "DOCUMENT",
        "PERSON": "PERSON",
        "ORGANISATION": "ORGANISATION",
        "LOCATION": "LOCATION",
        "EVENT": "MISCELLANEOUS"
    }
    ENTITY_TO_RELATIONSHIPS = {
        "DOCUMENT": ["MENTIONS", "MENTIONED_ON"],
        "PERSON": ["MENTIONS_ON"],
        "ORGANISATION": ["MENTIONS_ON", "LOCATED_IN"],
        "LOCATION": ["MENTIONED_ON"],
        "MISCELLANEOUS": ["MENTIONED_ON"],
        # Add indirect relationships here if needed
    }

    RELATIONSHIP_TO_ENTITY = {
        "MENTIONS" : [ "PERSON", "ORGANISATION", "LOCATION", "MISCELLANEOUS"],
        "MENTIONS_ON": ["DATE"],
        "LOCATED_IN": ["LOCATION"]

    }



    ENTITY_ATTRIBUTES = {
            "DOCUMENT": ["None", "doc_id", "text"],
            "PERSON": ["None", "name", "wiki_ID"],
            "ORGANISATION": ["None", "name", "wiki_ID"],
            "LOCATION": ["None", "name", "wiki_ID"],
            "EVENT": ["None", "name", "wiki_ID"],
    }
    def __init__(self, db):
        self.db = db
        self.db.connect()
        if 'entities' not in st.session_state:
            st.session_state.entities = [self.create_entity(0)] 
        # self.entities = [Entity(0)]  # Start with one entity


    def create_entity(self, entity_id):
        return Entity(entity_id)


    def get_entity_types(self, entity_id):
        unique_key = f"entity_type_{entity_id}"
        label = st.selectbox("Choose an entity type:", self.LABEL_OPTIONS, index=0, key=unique_key)
        return self.LABEL_MAPPING.get(label, "")
    

    def get_relationship(self, entity_id, label):
        unique_key = f"entity_relationshio_{entity_id}"
        available_relationships = self.ENTITY_TO_RELATIONSHIPS.get(label, [])
        relationship_type = st.selectbox("Choose the relationship type:", available_relationships, index=0, key=unique_key)
        return relationship_type
    

    def get_related_entites(self, entity_id, relationship_type):
        unique_key = f"entity_related_{entity_id}"
        available_entities = self.RELATIONSHIP_TO_ENTITY.get(relationship_type, [])
        related_entity = st.selectbox("Choose the related entity type:", available_entities, index=0, key=unique_key)
        return related_entity

    def get_attributes(self, entity_id, label):
        unique_name_key = f"entity_variable_name_{entity_id}"
        unique_value_key = f"entity_variable_value_{entity_id}"
        attribute_options = self.ENTITY_ATTRIBUTES.get(label, [])
        attribute_name = st.selectbox("Select variable name:", options=attribute_options, index=0, key=unique_name_key)
        attribute_value = st.text_input("Enter variable value:", key=unique_value_key)
        return attribute_name, attribute_value

    

    def get_filters(self, entity_id, label):
        attribute_name, attribute_value, date_from_year, date_to_year = None, None, None, None
        attribute_name, attribute_value = self.get_attributes(entity_id, label)
        date_from_year, date_to_year =  self.choose_date_range(entity_id)
        return attribute_name, attribute_value, date_from_year, date_to_year


    def get_number_of_results(self):
        return st.number_input("Number of results to display:", min_value=1, max_value=100, value=10, key="num_results")
        

    def choose_date_range(self, entity_id):
        date_from_name_key = f"entity_date_from_{entity_id}"
        date_to_name_key = f"entity_date_to_{entity_id}"
        col1, col2 = st.columns(2)
        with col1:
            date_from_year = st.text_input("Date from (Year):", key=date_from_name_key)
        with col2:
            date_to_year = st.text_input("Date to (Year):", key=date_to_name_key)

        date_from_year, date_to_year = self.parse_date(date_from_year), self.parse_date(date_to_year)
        return date_from_year, date_to_year


    @staticmethod
    def parse_date(date_str):
        try:
            return int(date_str) if date_str else None
        except ValueError:
            st.warning("Please enter a valid year.")
            return None


    
    def display_entity_inputs(self):
        st.header("Entity Configuration")
        # all_nodes = PERSON.nodes.all()
        # st.write(all_nodes)
        for i, entity in enumerate(st.session_state.entities):
            with st.expander(f"Entity {i + 1} Details", expanded=True):
                # st.write(f"Entity ID: {entity.id}")
                entity.label = self.get_entity_types(entity.id)
                entity.relationship = self.get_relationship(entity.id, entity.label)
                entity.related_entity = self.get_related_entites(entity.id, entity.relationship)
                entity.attribute_name, entity.attribute_value, entity.date_from_year, entity.date_to_year = self.get_filters(entity.id, entity.label)

                num_results = self.get_number_of_results()
                return num_results


    def add_entity(self):
        entity_id = len(st.session_state.entities)
        st.session_state.entities.append(self.create_entity(entity_id))
        st.success("Added new entity. Configure it below.")


    def display_form(self):
        st.title("Dynamic Cypher Query Builder")
        num_results = self.display_entity_inputs()
        output_type = st.radio("Output type:", ["JSON", "Table", "GRAPH"], index=1, key="output_type", horizontal=True)

        if st.button("Search", use_container_width=True):
            builder = CypherQueryBuilder()
            constructed_query = builder.construct_query(st.session_state.entities, num_results)

            st.code(constructed_query)
            self.execute_query(constructed_query,output_type)



    # def choose_date_range(self):
    #     """
    #     Prompts the user to enter a start and end date, and returns them as integers.

    #     Returns:
    #         A tuple of integers representing the start and end dates, or None if the user entered an invalid date.
    #     """
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         date_from_year_str = st.text_input("Date from:", key="from_year_txt")
    #     with col2:
    #         date_to_year_str = st.text_input("Date to:", key="to_year_txt")

    #     try:
    #         date_from_year = int(date_from_year_str) if date_from_year_str else None
    #     except ValueError:
    #         st.warning("Please enter a valid integer for 'Date from'.")
    #         date_from_year = None

    #     try:
    #         date_to_year = int(date_to_year_str) if date_to_year_str else None
    #     except ValueError:
    #         st.warning("Please enter a valid integer for 'Date to'.")
    #         date_to_year = None

    #     return date_from_year, date_to_year

    

 





        


    def display_query_form(self):
        """Renders UI elements for Cypher query input and returns the necessary components to build a query.

        Returns:
            tuple: A tuple containing the following components of the query:
                label (str): The entity type [PERSON, MISCELLANEOUS, ORGANISATION, LOCATION], or None if not specified
                date_from (int or None): The start date, or None if not specified
                date_to (int or None): The end date, or None if not specified
                variable_name (str or None): The variable name, or None if not specified
                variable_value (str or None): The variable value, or None if not specified
                num_results (int): The number of results to display
        """
        
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
        enable_options = st.columns(4)
        enable_entity_type = enable_options[0].checkbox("Enable Entity Type", value=False)
        enable_relationship_type = enable_options[1].checkbox("Enable Relationship Type", value=False)
        enable_date_range = enable_options[2].checkbox("Enable Date Range", value=False)
        enable_specific_variable = enable_options[3].checkbox("Enable Specific Variable Search", value=False, disabled=not enable_entity_type)

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
    

    def display_results(self, results, output_type):
        """Displays query results based on the output type."""
        if not results:
            st.write("No results found.")
            return

        if output_type == "JSON":
            st.json(results)
        elif output_type == "GRAPH":
            st.write(results)
            nodes, edges = self.process_entities_and_relationships(results)
            self.display_graph(nodes, edges)
        else:  # Default to table view
            table_data = self.prepare_table_data(results)
            st.table(table_data)



    def display_graph(self, nodes, edges):
        """Displays a graph using streamlit-agraph based on the provided nodes and edges."""
        graph_nodes = [Node(id=node['id'], label=node['title'], size=400) for node in nodes]
        graph_edges = [Edge(source=edge['source'], target=edge['target'], label=edge['label']) for edge in edges]

        config = {
            'height': 600,
            'width': 800,
            'directed': False,
            'nodeHighlightBehavior': True,
            'highlightColor': "#F7A7A6",
        }

        agraph(nodes=graph_nodes, edges=graph_edges, config=config)

    def prepare_table_data(self, results):
        """Prepares data for tabular display."""
        table_data = []
        for record in results:
            node = record['n']
            row = {'labels': ', '.join(node.labels)}
            row.update(node._properties)
            table_data.append(row)
        return table_data
    

    def process_entities_and_relationships(self, entities):
        """Transforms entities and their relationships into nodes and edges for visualization."""
        nodes = []
        edges = []

        for entity in entities:
            # Assuming 'entities' is a list of Entity objects
            # Create a Node for each entity
            st.write(entity)
            node_label = entity.label if entity.label else str(entity.id)
            nodes.append(Node(id=str(entity.id), label=node_label, title=node_label, size=400))

            # If the entity has a relationship and a related entity, create an Edge
            if entity.relationship and entity.related_entity:
                edges.append(Edge(source=str(entity.id), target=str(entity.related_entity), label=entity.relationship))

        return nodes, edges

    def execute_query(self, query, output_type=None):
        """Executes the provided query and displays the results."""
        try:
            results = self.db.query(query)
            if results:
                self.display_results(results, output_type)
            else:
                st.write("No results found.")

        except Exception as e:
            st.error(f"Execution error: {e}")





    def construct_and_display_query(self, label, variable_name, variable_value, date_from, date_to, num_results):
        """Constructs and displays a Cypher query based on user inputs.

        Args:
            label (str): The entity type [PERSON, MISCELLANEOUS, ORGANISATION, LOCATION], or None if not specified
            variable_name (str): The variable name, or None if not specified
            variable_value (str): The variable value, or None if not specified
            date_from (int): The start date, or None if not specified
            date_to (int): The end date, or None if not specified
            num_results (int): The number of results to display

        Returns:
            str: The constructed Cypher query, or None if no query could be constructed.
        """

        
        query_builder = CypherQueryBuilder()
        constructed_query = ""


        # Construct and display query
        col1, col2 = st.columns(2)
        with col1:
            constrc_button = st.button('Construct and Display Query', key="construct_query_button", use_container_width=True)
        with col2:
            execute_button = st.button('Execute Constructed Query', key="execute_constructed_query_button", use_container_width=True)


        # Choose output type:
        col1_output_type, col2_clear_output = st.columns(2)
        with col1_output_type:
            output_type = st.radio("Output type:", ["JSON", "Table"], index=1, key="output_type", horizontal=True)
        with col2_clear_output:
            if st.button("Clear Output", key="clear_output_button", use_container_width=True):
                st.empty()
            
        
        # _build_query
        if constrc_button:
            if variable_name and variable_value:
                constructed_query = query_builder.construct_variable_query(label, variable_name, variable_value, date_from, date_to, num_results)
            elif label and (date_from or date_to):
                constructed_query = query_builder.construct_query(label, None, date_from, date_to, num_results)
            else:
                # Handle other cases or show a message indicating that more input is needed
                st.write("Please provide more input to construct the query.")

            if constructed_query:
                st.code(constructed_query)  
                st.session_state['constructed_query'] = constructed_query
                return constructed_query

        if 'constructed_query' in st.session_state and execute_button:
            if output_type == 'JSON':
                self.execute_query(st.session_state['constructed_query'], output_type="json")
            else:
                self.execute_query(st.session_state['constructed_query'])



