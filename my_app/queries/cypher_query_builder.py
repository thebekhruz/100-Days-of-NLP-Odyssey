class CypherQueryBuilder:
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
    def construct_date_query(date_from, date_to, label):
        """Constructs a query component for date filtering."""
        neo4j_label = CypherQueryBuilder.get_label(label)
        match_clause = f"MATCH (n:{neo4j_label})" if neo4j_label else "MATCH (n)"
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

    @staticmethod
    def construct_query(label, name, date_from, date_to, num_results, variable_name=None, variable_value=None):
        """
        Constructs the final Cypher query based on given parameters, including support for specific variables.
        """
        if date_from or date_to:
            match_clause, relationship, where_clause = CypherQueryBuilder.construct_date_query(date_from, date_to, label)
        elif variable_name and variable_value:
            match_clause = CypherQueryBuilder.construct_variable_query(label, name, variable_name, variable_value)
            relationship, where_clause = "", ""
        else:
            match_clause = CypherQueryBuilder.construct_entity_query(label, name)
            relationship, where_clause = "", ""

        query = f"{match_clause} {relationship} {where_clause} RETURN n LIMIT {num_results}"
        return query.strip()
