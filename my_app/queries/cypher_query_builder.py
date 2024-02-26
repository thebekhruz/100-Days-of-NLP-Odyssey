# class Entity:
#     def __init__(self, entity_id):
#         self.id = entity_id
#         self.label = None
#         self.relationship = None
#         self.attribute_name = None
#         self.attribute_value = None
import streamlit as st

class CypherQueryBuilder:

    # def construct_query(self, entities):
    #     """Constructs a Cypher query based on the given parameters."""
    #     match_clauses = []
    #     for entity in entities:
    #         if entity.label:
    #             st.write(f"Entity label: %s" % entity.label)
    #             match_clauses.append(f"MATCH (n:{entity.label})" if entity.label else "MATCH (n)")
    #             if entity.relationship:
    #                 st.write(f"Relationship: %s" % entity.relationship)
    #                 match_clauses.append(f" - [{entity.relationship}] -> ({entity.related_entity})")



    #     complete_query = " ".join(match_clauses)
    #     return complete_query
    

    def construct_query(self, entities, num_results):
        """Constructs a Cypher query based on the given parameters."""
        query_parts = []

        for entity in entities:
            # Ensure the entity has a label before constructing a part of the match clause
            if entity.label:
                # Construct the base match clause for the entity
                base_match = f"MATCH (n:{entity.label})"
                # If there's a specified relationship, append it to the base match clause
                if entity.relationship and entity.related_entity:
                    # Assume entity.related_entity contains the label of the related entity type
                    related_match = f"-[:{entity.relationship}]->(m:{entity.related_entity})"
                    complete_match = f"{base_match} {related_match}"
                    query_parts.append(complete_match)
                else:
                    query_parts.append(base_match)


        # Add number of rresults to display:
        query_parts.append(f"RETURN n LIMIT {num_results}")


        # Join all query parts together to form the complete query
        complete_query = " ".join(query_parts)
        return complete_query
    


        # st.write(f"Complete Query: {complete_query}")        


    # def construct_full_query(self, label, relationship, attribute_name, attribute_value, date_from_year, date_to_year):
    #     """Constructs a full Cypher query with all parameters."""
    #     match_clause = f"MATCH (n:{label})" if label else "MATCH (n)"
    #     if relationship == "MENTIONED_ON":
    #         relationship_clause = '-[:MENTIONED_ON]->(date:DATE)'
    #     elif relationship == "MENTIONS":
    #         relationship_clause = f"-[:{relationship}]->(a:DOCUMENT)"
    #     elif relationship == "LOCATED_IN":
    #         relationship_clause = f"-[:{relationship}]->(a:LOCATION)"

    #     # match_clause = f"MATCH (entity:{label})"
    #     # relationship_clause = f"-[:{relationship}]->(a:DATE)"
    #     # where_clause = f"WHERE a.year >= {date_from_year} AND a.year <= {date_to_year} AND n.{attribute_name} = '{attribute_value}'"
    #     # return f"{match_clause} {relationship_clause} {where_clause} RETURN n" 


    LABEL_MAPPING = {
        "DOCUMENT ID": "DOCUMENT",
        "PERSON": "PERSON",
        "ORGANISATION": "ORGANISATION",
        "LOCATION": "LOCATION",
        "EVENT": "MISCELLANEOUS"
    }

    @classmethod
    def get_label(cls, label):
        """Retrieve Neo4j label from mapping or return an empty string if not found."""
        return cls.LABEL_MAPPING.get(label, "")


    
    @staticmethod
    def construct_time_filter(label, date_from, date_to):
        """Constructs a query component for date filtering."""
        match_clause = f"MATCH (n:{label})" if label else "MATCH (n)"
        relationship_clause = '-[:MENTIONED_ON]->(date:DATE)'
        where_clause_parts = []
        if date_from:
            where_clause_parts.append(f"date.date >= '{date_from}'")
        if date_to:
            where_clause_parts.append(f"date.date <= '{date_to}'")
        where_clause = "WHERE " + " AND ".join(where_clause_parts) if where_clause_parts else ""
        return match_clause, relationship_clause, where_clause

    @staticmethod
    def construct_entity_query(label, name):
        """Constructs a query component for entity filtering."""
        neo4j_label = CypherQueryBuilder.get_label(label)
        if name:
            match_clause = f"MATCH (n:{neo4j_label} {{name: '{name}'}})" if neo4j_label != "DOCUMENT" else f"MATCH (n:{neo4j_label} {{document_id: '{name}'}})"
        else:
            match_clause = f"MATCH (n:{neo4j_label})"
        return match_clause
    

    @staticmethod
    def construct_variable_query(label, variable_name, variable_value, date_from, date_to, num_results):
        """
        Constructs a query component for searching by specific variables within a node.
        """
        # Assuming `get_label` maps the user-friendly label to a Neo4j label
        neo4j_label = CypherQueryBuilder.get_label(label)
        match_clause = ""
        where_clauses = []
        
        # Construct match clause based on variable name and value
        if variable_name and variable_value:
            match_clause = f"MATCH (n:{neo4j_label} {{{variable_name}: '{variable_value}'}})"
        
        # Construct where clause based on date range
        if date_from:
            where_clauses.append(f"n.date >= '{date_from}'")
        if date_to:
            where_clauses.append(f"n.date <= '{date_to}'")
        
        where_clause = " AND ".join(where_clauses)
        if where_clause:
            where_clause = "WHERE " + where_clause

        query = f"{match_clause} {where_clause} RETURN n LIMIT {num_results}"
        return query.strip()

    # @staticmethod
    # def construct_query(label, name, date_from, date_to, num_results, variable_name=None, variable_value=None):
    #     """
    #     Constructs the final Cypher query based on given parameters, including support for specific variables.
    #     """
    #     if date_from or date_to:
    #         match_clause, relationship, where_clause = CypherQueryBuilder.construct_date_query(date_from, date_to, label)
    #     elif variable_name and variable_value:
    #         match_clause = CypherQueryBuilder.construct_variable_query(label, name, variable_name, variable_value)
    #         relationship, where_clause = "", ""
    #     else:
    #         match_clause = CypherQueryBuilder.construct_entity_query(label, name)
    #         relationship, where_clause = "", ""

    #     query = f"{match_clause} {relationship} {where_clause} RETURN n LIMIT {num_results}"
    #     return query.strip()
