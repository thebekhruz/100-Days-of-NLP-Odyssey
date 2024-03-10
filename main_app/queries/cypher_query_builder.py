from db.neo4j_connection import Neo4jConnection  # Import the connection class
import streamlit as st


class CypherQueryBuilder:

    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, connection, subject_entity, relationship_to_explore, target_entity, number_of_results_to_explore):
        query = f"""
        MATCH (n:{subject_entity})-[r:{relationship_to_explore}]->(m:{target_entity})
        RETURN n, r, m LIMIT {number_of_results_to_explore}
        """
        result = self.connection.run_query(query) 
        return result
    
    def execute_query_with_filters(self, connection, subject_entity, relationship_to_explore, target_entity, number_of_results_to_explore, attribute_type=None, attribute_value=None, date_from=None, date_to=None):
        # Start with a base MATCH clause
        match_clause = f"MATCH (n:{subject_entity})-[r:{relationship_to_explore}]->(m:{target_entity})"
        # Initialize a list to hold WHERE clause conditions
        where_conditions = []

        # Add attribute_type_type filter condition if provided
        if attribute_type and attribute_value:
            # Use CONTAINS for easier user experience
            where_conditions.append(f"n.{attribute_type} CONTAINS '{attribute_value}'")
            


        # Include date filtering if any date criteria are provided
        if date_from or date_to:
            # Extend the MATCH clause to include the Date entity
            match_clause += " MATCH (n)-[:MENTIONED_ON]->(d:DATE)"

        # Add date filter conditions if provided
        if date_from:
            where_conditions.append(f"d.date >= '{date_from}'")
        if date_to:
            where_conditions.append(f"d.date <= '{date_to}'")

        # Combine all conditions into a single WHERE clause if there are any
        where_clause = ""
        if where_conditions:
            where_clause = f" WHERE {' AND '.join(where_conditions)}"

        # Build the complete query with MATCH, WHERE, and LIMIT clauses
        query = f"""
        {match_clause}
        {where_clause}
        RETURN n, r, m LIMIT {number_of_results_to_explore}
        """


        # Execute the query using the connection
        result = self.connection.run_query(query) 
        return result




# # class Entity:
# #     def __init__(self, entity_id):
# #         self.id = entity_id
# #         self.label = None
# #         self.relationship = None
# #         self.attribute_type_name = None
# #         self.attribute_type_value = None
# import streamlit as st

# class CypherQueryBuilder:

    

#     # def construct_query(self, entities):
#     #     """Constructs a Cypher query based on the given parameters."""
#     #     match_clauses = []
#     #     for entity in entities:
#     #         if entity.label:
#     #             st.write(f"Entity label: %s" % entity.label)
#     #             match_clauses.append(f"MATCH (n:{entity.label})" if entity.label else "MATCH (n)")
#     #             if entity.relationship:
#     #                 st.write(f"Relationship: %s" % entity.relationship)
#     #                 match_clauses.append(f" - [{entity.relationship}] -> ({entity.related_entity})")



#     #     complete_query = " ".join(match_clauses)
#     #     return complete_query
    

#     def construct_query(self, entities, num_results):
#         """Constructs a Cypher query based on the given parameters."""
#         query_parts = []

#         for entity in entities:
#             # Ensure the entity has a label before constructing a part of the match clause
#             if entity.label:
#                 # Construct the base match clause for the entity
#                 base_match = f"MATCH (n:{entity.label})"
#                 if entity.relationship and entity.related_entity:
#                     related_match = f"-[:{entity.relationship}]->(m:{entity.related_entity})"
#                     complete_match = f"{base_match} {related_match}"
#                     query_parts.append(complete_match)
#                 else:
#                     query_parts.append(base_match)


#         # Add number of rresults to display:
#         query_parts.append(f"RETURN n LIMIT {num_results}")


#         # Join all query parts together to form the complete query
#         complete_query = " ".join(query_parts)
#         return complete_query
    


#         # st.write(f"Complete Query: {complete_query}")        


#     # def construct_full_query(self, label, relationship, attribute_type_name, attribute_type_value, date_from_year, date_to_year):
#     #     """Constructs a full Cypher query with all parameters."""
#     #     match_clause = f"MATCH (n:{label})" if label else "MATCH (n)"
#     #     if relationship == "MENTIONED_ON":
#     #         relationship_clause = '-[:MENTIONED_ON]->(date:DATE)'
#     #     elif relationship == "MENTIONS":
#     #         relationship_clause = f"-[:{relationship}]->(a:DOCUMENT)"
#     #     elif relationship == "LOCATED_IN":
#     #         relationship_clause = f"-[:{relationship}]->(a:LOCATION)"

#     #     # match_clause = f"MATCH (entity:{label})"
#     #     # relationship_clause = f"-[:{relationship}]->(a:DATE)"
#     #     # where_clause = f"WHERE a.year >= {date_from_year} AND a.year <= {date_to_year} AND n.{attribute_type_name} = '{attribute_type_value}'"
#     #     # return f"{match_clause} {relationship_clause} {where_clause} RETURN n" 


#     LABEL_MAPPING = {
#         "DOCUMENT ID": "DOCUMENT",
#         "PERSON": "PERSON",
#         "ORGANISATION": "ORGANISATION",
#         "LOCATION": "LOCATION",
#         "EVENT": "MISCELLANEOUS"
#     }

#     @classmethod
#     def get_label(cls, label):
#         """Retrieve Neo4j label from mapping or return an empty string if not found."""
#         return cls.LABEL_MAPPING.get(label, "")


    
#     @staticmethod
#     def construct_time_filter(label, date_from, date_to):
#         """Constructs a query component for date filtering."""
#         match_clause = f"MATCH (n:{label})" if label else "MATCH (n)"
#         relationship_clause = '-[:MENTIONED_ON]->(date:DATE)'
#         where_clause_parts = []
#         if date_from:
#             where_clause_parts.append(f"date.date >= '{date_from}'")
#         if date_to:
#             where_clause_parts.append(f"date.date <= '{date_to}'")
#         where_clause = "WHERE " + " AND ".join(where_clause_parts) if where_clause_parts else ""
#         return match_clause, relationship_clause, where_clause

#     @staticmethod
#     def construct_entity_query(label, name):
#         """Constructs a query component for entity filtering."""
#         neo4j_label = CypherQueryBuilder.get_label(label)
#         if name:
#             match_clause = f"MATCH (n:{neo4j_label} {{name: '{name}'}})" if neo4j_label != "DOCUMENT" else f"MATCH (n:{neo4j_label} {{document_id: '{name}'}})"
#         else:
#             match_clause = f"MATCH (n:{neo4j_label})"
#         return match_clause
    

#     @staticmethod
#     def construct_variable_query(label, variable_name, variable_value, date_from, date_to, num_results):
#         """
#         Constructs a query component for searching by specific variables within a node.
#         """
#         # Assuming `get_label` maps the user-friendly label to a Neo4j label
#         neo4j_label = CypherQueryBuilder.get_label(label)
#         match_clause = ""
#         where_clauses = []
        
#         # Construct match clause based on variable name and attribute_type_value
#         if variable_name and variable_value:
#             match_clause = f"MATCH (n:{neo4j_label} {{{variable_name}: '{variable_value}'}})"
        
#         # Construct where clause based on date range
#         if date_from:
#             where_clauses.append(f"n.date >= '{date_from}'")
#         if date_to:
#             where_clauses.append(f"n.date <= '{date_to}'")
        
#         where_clause = " AND ".join(where_clauses)
#         if where_clause:
#             where_clause = "WHERE " + where_clause

#         query = f"{match_clause} {where_clause} RETURN n LIMIT {num_results}"
#         return query.strip()

#     # @staticmethod
#     # def construct_query(label, name, date_from, date_to, num_results, variable_name=None, variable_value=None):
#     #     """
#     #     Constructs the final Cypher query based on given parameters, including support for specific variables.
#     #     """
#     #     if date_from or date_to:
#     #         match_clause, relationship, where_clause = CypherQueryBuilder.construct_date_query(date_from, date_to, label)
#     #     elif variable_name and variable_value:
#     #         match_clause = CypherQueryBuilder.construct_variable_query(label, name, variable_name, variable_value)
#     #         relationship, where_clause = "", ""
#     #     else:
#     #         match_clause = CypherQueryBuilder.construct_entity_query(label, name)
#     #         relationship, where_clause = "", ""

#     #     query = f"{match_clause} {relationship} {where_clause} RETURN n LIMIT {num_results}"
#     #     return query.strip()
