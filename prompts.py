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
                        "description": f"""MySQL query extracting info to answer the user's question. \
MySQL should be written using this database schema: \
{database_schema_string} \
The query should be returned in plain text, not in JSON. \
Use limit of 10 when creating a query. \
Consider today's date as {datetime.now().strftime("%b %d, %Y")}. \
Don't assume any column names that are not in the database schema, use the \
following data definitions instead: \
{database_definitions}"""
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
