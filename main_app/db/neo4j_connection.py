import streamlit as st
from neo4j import GraphDatabase
from neomodel import config

# Database connection management
class Neo4jConnection:
    """Handles the connection to Neo4j database."""
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None

    def connect(self):
        """Establishes a connection to the Neo4j database."""
        if not self.__driver:
            try:
                self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
                st.success("Connected to Neo4j successfully!")
            except Exception as e:
                st.error(f"Failed to create the driver: {e}")
        else:
            st.info("Already connected to Neo4j.")



    def close(self):
        """Closes the connection to the Neo4j database."""
        if self.__driver:
            self.__driver.close()
            self.__driver = None
            st.info("Connection to Neo4j closed.")
        else:
            st.warning("No active connection to close.")

    def run_query(self, query, parameters=None, db=None):
        """Executes a Cypher query against the Neo4j database."""
        if not self.__driver:
            raise Exception("Driver not initialized!")
        with (self.__driver.session(database=db) if db else self.__driver.session()) as session:
            return list(session.run(query, parameters))
        


class Neo4jConnector:
    """Handles Neo4j database connection."""

    @staticmethod
    def initialize_connection():
        """Initializes the Neo4j database connection."""
        try:
            uri = st.secrets["neo4j"]["uri"]
            user = st.secrets["neo4j"]["username"]
            pwd = st.secrets["neo4j"]["password"]

            # Initialize and connect
            connection = Neo4jConnection(uri, user, pwd)
            connection.connect()

            # Configure neomodel
            config.DATABASE_URL = f"bolt://{user}:{pwd}@{uri.split('://')[1]}"

            # Store connection in session state
            st.session_state['db_connection'] = connection

        except Exception as e:
            st.error(f"Failed to initialize connection: {e}")