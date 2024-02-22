import streamlit as st
from neo4j import GraphDatabase, basic_auth

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None

    def connect(self):
        if not self.__driver:
            try:
                self.__driver = GraphDatabase.driver(self.__uri, auth=basic_auth(self.__user, self.__pwd))
                print(self.__driver)
                st.success("Connected to Neo4j successfully!")
            except Exception as e:
                st.error(f"Failed to create the driver: {e}")
        else:
            st.info("Already connected to Neo4j.")


    def close(self):
        if self.__driver is not None:
            self.__driver.close()
            self.__driver = None
            st.info("Connection to Neo4j closed.")
        else:
            st.warning("No active connection to close.")
        
    def query(self, query, parameters=None, db=None):
        if self.__driver is None:
            raise Exception("Driver not initialized!")
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
            return response
        except Exception as e:
            st.error(f"Query failed: {e}")
        finally:
            if session is not None:
                session.close()

    def display_results_in_table(results):
        if results:
            # Assuming results[0] is a dictionary, get keys for column names
            columns = results[0].keys()
            data = [{col: result[col] for col in columns} for result in results]
            st.table(data)
        else:
            st.write("No results found.")


class CypherQueryBuilder:
    def __init__(self):
        pass

    def construct_query(self, label=None, name=None, date_from=None, date_to=None, num_results=10):
        # Start building the query
        query = "MATCH (n"
        query += f":{label}" if label else ""
        query += ")"
        
        # Add WHERE clause if name is provided
        if name:
            query += f" WHERE n.ne_span = '{name}'"
        
        # Add date range condition if dates are provided
        if date_from and date_to:
            query += " AND" if name else " WHERE"
            query += f" n.date >= {date_from} AND n.date <= {date_to}"
        
        # Append RETURN statement with limit on number of results
        query += f" RETURN n LIMIT {num_results}"
        
        return query

                
# Initialize connection object in Streamlit session state if not already done
def display_results_in_table(results):
    if results:
        # Assuming results[0] is a dictionary, get keys for column names
        columns = results[0].keys()
        data = [{col: result[col] for col in columns} for result in results]
        st.table(data)
    else:
        st.write("No results found.")


if 'db_connection' not in st.session_state:
    uri = st.secrets["neo4j_uri"]
    user = st.secrets["neo4j_username"]
    pwd = st.secrets["neo4j_password"]
    st.session_state['db_connection'] = Neo4jConnection(uri, user, pwd)

def main():
    db = st.session_state['db_connection']
    query_builder = CypherQueryBuilder()

    # st.toggle("Enable")

        
    st.title('Cypher Query App')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Connect to Neo4j'):
            db.connect()

    with col2:
        if st.button('Close the connection'):
            db.close()


    # UI elements to capture inputs
    label_option = ["None", "LOCATION", "ORGANISATION", "PERSON", "EVENT"]
    label = st.selectbox("Choose an entity type (or None):", label_option, index=0)  # Default to 'None'
    name = st.text_input("Enter name (optional):")
    date_from = st.number_input("Date from (year, optional):", min_value=1600, max_value=2023, value=1600, step=1, format="%d", key="from_year")
    date_to = st.number_input("Date to (year, optional):", min_value=1600, max_value=2023, value=2023, step=1, format="%d", key="to_year")
    num_results = st.number_input("Number of results (optional):", min_value=1, max_value=100, value=10)

    # Adjusting inputs based on user selections
    adjusted_label = None if label == "None" else label
    adjusted_date_from = None if date_from == 1600 else date_from
    adjusted_date_to = None if date_to == 2023 else date_to
    
    # Button to construct and display the query
    if st.button('Construct Query'):
        constructed_query = query_builder.construct_query(adjusted_label, name if name else None, adjusted_date_from, adjusted_date_to, num_results)
        st.code(constructed_query, language='sql')

    query = st.text_area("Enter your Cypher query here:", height=150)
    if st.button('Execute'):
        if query:
            try:
                results = db.query(query)
                if results:
                    display_results_in_table([result.data() for result in results])
                else:
                    st.write("No results found.")
            except Exception as e:
                st.error(f"Execution error: {e}")
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()