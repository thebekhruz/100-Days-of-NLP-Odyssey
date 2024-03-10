# sidebar_ui.py
import streamlit as st
from db.enums import EntityType, RelationshipType, RELATIONSHIP_MAPPINGS

class SidebarUI:
    
    def __init__(self):
        pass

   
    def get_sidebar(self):
        st.sidebar.header("Semantic Search")

        # Convert enum members to strings for display
        subject_entity_options = [entity.name for entity in EntityType]
        subject_entity_help = "Select the starting entity type for the semantic search. This will define the starting point of the Cypher query node `(n:Entity)`."
        subject_entity = st.sidebar.selectbox("Choose the subject entity", subject_entity_options, key="subject_entity", help=subject_entity_help)

        # Get the selected entity enum
        selected_entity = EntityType[subject_entity]

        # Get the possible relationships for the selected entity
        possible_relationships = RELATIONSHIP_MAPPINGS.get(selected_entity, {})
        relationship_options = [rel.name for rel in possible_relationships]
        relationship_to_explore_help = "Choose the relationship type that connects your subject entity to the target entity. This represents the Cypher relationship type `-[:Relationship]->`."
        relationship_to_explore = st.sidebar.selectbox("Choose the relationship to explore", relationship_options, key="relationship_to_explore", help=relationship_to_explore_help)

        # Get the selected relationship enum
        selected_relationship = RelationshipType[relationship_to_explore]

        # Determine possible target entities based on the selected relationship
        possible_target_entities = possible_relationships[selected_relationship]
        target_entity_options = [entity.name for entity in possible_target_entities]
        target_entity_help = "Select the target entity type that you wish to find a relationship with. It completes the Cypher pattern `(n)-[:Relationship]->(m:Entity)`."
        target_entity = st.sidebar.selectbox("Choose the target entity", target_entity_options, key="target_entity", help=target_entity_help)

        output_type_help = "Select the format you would like the output to be displayed in."
        output_type = st.sidebar.selectbox("Select view:",["Json", "Table", "Graph"], index=1, key="output_type",help= output_type_help)


        number_of_results_to_explore_help = "Set the maximum number of relationship instances you wish to retrieve from the query. This limits the results returned by the Cypher query."
        number_of_results_to_explore = st.sidebar.number_input("Number of results to display", min_value=1, max_value=100, value=10, key="number_of_results_to_explore", help=number_of_results_to_explore_help)



        return selected_entity, selected_relationship, EntityType[target_entity], number_of_results_to_explore, output_type



if __name__ == "__main__":
    ui = SidebarUI()
    ui.display_sidebar()

