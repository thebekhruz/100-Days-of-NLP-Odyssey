import streamlit as st
from db.model_utils import ModelUtils
from db.enums import EntityType
from queries.cypher_query_builder import CypherQueryBuilder 
from ui.results_displayer import ResultsDisplayer


ENTITY_ATTRIBUTES = {
            "DOCUMENT": [ "doc_id", "text"],
            "PERSON": [ "name", "wiki_ID"],
            "ORGANISATION": [ "name", "wiki_ID"],
            "LOCATION": [ "name", "wiki_ID"],
            "EVENT": [ "name", "wiki_ID"],
    }
class ContainerUI():
    def __init__(self):
        pass

    @staticmethod
    def parse_date(date_str):
        try:
            return int(date_str) if date_str else None
        except ValueError:
            st.warning("Please enter a valid year.")
            return None


    def get_filters(self, subject = None, target=None):
    
        returns = []
        col0, col1, col2, col3, col4 = st.columns(5)
        subject_entity, attribute_type, attribute_value, date_from, date_to = None, None, None, None, None
        with col0:
            subject_entity = st.selectbox(
                "Select Entity",
                options= [st.session_state["subject_entity"], st.session_state['target_entity']],
                index = None,
                key="subject_entity_filter",
                help="Select the entity type you are interested in filtering by."
            )
            

        with col1:
            attribute_type = st.selectbox(
                "Attribute Type",
                options=ENTITY_ATTRIBUTES.get(subject_entity, []),
                key="attribute_type_filter",
                help="Select the type of attribute for the entity to filter by."
            )

        with col2:
            attribute_value = st.text_input(
                "Enter attribute value:",
                key="attribute_value",
                help="Enter the value of the selected attribute to filter by."
            )

        with col3:
            date_from = st.text_input(
                "Date from (Year):",
                key='date_from',
                help="Enter the starting year for the date range filter."
            )

        with col4:
            date_to = st.text_input(
                "Date to (Year):",
                key='date_to',
                help="Enter the ending year for the date range filter."
            )
        # Parsing dates after user input
        date_from_parsed, date_to_parsed = self.parse_date(date_from), self.parse_date(date_to)


        return subject_entity, attribute_type, attribute_value, date_from_parsed, date_to_parsed



    def display_search_and_filter_buttons(self, connection):
        container = st.container(height = 500, border=True)

        col1, col2 = st.columns(2)
        with col1:
            try:
                if st.button("Apply filters", use_container_width=True, key="filter_button"):
                    builder = CypherQueryBuilder(st.session_state['db_connection'])
                    st.write(st.session_state['subject_entity'],st.session_state['relationship_to_explore'])

                    results_from_execution = builder.execute_query_with_filters(
                        connection,
                        subject_entity = st.session_state['subject_entity'],
                        relationship_to_explore = st.session_state['relationship_to_explore'],
                        target_entity = st.session_state['target_entity'],
                        number_of_results_to_explore = st.session_state['number_of_results_to_explore'],
                        attribute_type = st.session_state['attribute_type_filter'],
                        attribute_value=st.session_state['attribute_value'],
                        date_from=st.session_state['date_from'],
                        date_to=st.session_state['date_to']
                    )
                    ResultsDisplayer(container, results_from_execution, st.session_state['output_type'])
            except Exception as e:
                st.warning('Please add attributes')

        with col2:
            if st.button("Search", use_container_width=True, key="search_button"):
                builder = CypherQueryBuilder(st.session_state['db_connection'])
                results_from_execution = builder.execute_query(
                    connection,
                    st.session_state['subject_entity'],
                    st.session_state['relationship_to_explore'],
                    st.session_state['target_entity'],
                    st.session_state['number_of_results_to_explore']
                )
                ResultsDisplayer(container, results_from_execution, st.session_state['output_type'])
                
