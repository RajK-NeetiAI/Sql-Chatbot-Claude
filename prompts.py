from datetime import datetime


def get_tools(database_schema_string: str, database_definitions: str) -> list[dict]:
    tools = [
        {
            "name": "ask_database",
            "description": "Use this function to answer user questions about Production data. Input should be a fully formed MySQL query.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f'''Generate a PostgreSQL query to extract information based on a user's question. \
# Parameters: \
# - Database Schema: {database_schema_string} \
# - Data Definitions: {database_definitions} \
# - Current Date: Use today's date in the format 'YYYY-MM-DD' where needed in the query. \

# Instructions: \
# 1. Construct an SQL query using only the tables and columns listed in the provided schema. \
# 2. When comparing string use LIKE to maximise the search. \
# 2. Ensure the query avoids assumptions about non-existent columns. \
# 3. Consider performance and security best practices, such as avoiding SQL injection risks. \
# 4. Format the query in plain text for direct execution in a PostgreSQL database. \

# Example Query: \
# If the user asks for the number of employees in each department, the query should look like this: \
# "SELECT department_id, COUNT(*) FROM employees GROUP BY department_id;"'''
                    }
                },
                "required": ["query"],
            }
        }
    ]
    return tools


def get_failed_sql_query_system_prompt(query: str, formatted_chat_history: list[dict]) -> str:
    failed_sql_query_system_prompt = f'''Consider yourselk as a helpful data analyst of Neeti AI. \
A user has asked a question: {query}, in the context of the following chat history: \
{formatted_chat_history}, politely reply that you don't have the answer for the question.'''
    return failed_sql_query_system_prompt


def get_format_sql_response_system_prompt() -> str:
    sql_response_system_prompt = "Consider yourself as a helpful data analyst Neeti AI. \
You help user get information about the data and answer their question."
    return sql_response_system_prompt


def get_system_prompt() -> str:
    system_prompt = "You are a data analyst of Neeti AI. You help user get information about the database."
    return system_prompt
