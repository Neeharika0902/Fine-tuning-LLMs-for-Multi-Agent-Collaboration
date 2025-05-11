"""
Database utility functions for the multi-agent chatbot system
"""
import re
import snowflake.connector
from server.config import SF_USER, SF_PASSWORD, SF_ACCOUNT, SF_DATABASE, SF_SCHEMA, SF_WAREHOUSE

def extract_sql_from_query(query):
    """
    Extract SQL code from a query string that contains SQL code between ```sql and ``` markers

    Parameters:
    query (str): The input string containing SQL code

    Returns:
    str: The extracted SQL code or None if no SQL code found
    """
    # Define regex pattern to match SQL code between ```sql and ``` markers
    pattern = r"```sql\s*(.*?)\s*```"

    # Search for the pattern in the query
    match = re.search(pattern, query, re.DOTALL)

    # Return the extracted SQL code if found, otherwise None
    if match:
        return match.group(1).strip()
    else:
        return None

def execute_snowflake_query(sql_query):
    """
    Execute a SQL query in Snowflake and return the results

    Parameters:
    sql_query (str): The SQL query to execute

    Returns:
    dict: The query results including column names and data
    """
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=SF_USER,
            password=SF_PASSWORD,
            account=SF_ACCOUNT,
            database=SF_DATABASE,
            schema=SF_SCHEMA,
            warehouse=SF_WAREHOUSE
        )

        # Create a cursor
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(sql_query)

        # Get column names
        column_names = [desc[0] for desc in cursor.description]

        # Fetch all results
        results = cursor.fetchall()
        
        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return results
        return {
            "column_names": column_names,
            "data": results,
            "row_count": len(results),
            "status": "success"
        }

    except Exception as e:
        # Handle any errors
        return {
            "error": str(e),
            "status": "error"
        }

def process_and_execute_sql_query(input_query):
    """
    Process a string containing SQL code, extract the SQL, and execute it in Snowflake

    Parameters:
    input_query (str): The input string containing SQL code

    Returns:
    dict: The query results or error information
    """
    # Extract SQL from the input query
    sql_query = extract_sql_from_query(input_query)

    # Check if SQL was found
    if not sql_query:
        return {
            "error": "No SQL code found in the input. Please ensure SQL is wrapped in ```sql ... ``` tags.",
            "status": "error"
        }

    # Execute the SQL query
    result = execute_snowflake_query(sql_query)

    return result
