import anthropic

import config

client = anthropic.Anthropic(
    api_key=config.CLOUDE_API_KEY
)

response = client.beta.tools.messages.create(
    model=config.CLOUDE_MODEL,
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either \"celsius\" or \"fahrenheit\""
                    }
                },
                "required": ["location"]
            }
        }
    ],
    messages=[
        {
            "role": "user", "content": "What is the weather like today?"
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "<thinking>I need to use get_weather, and the user wants SF, which is likely San Francisco, CA.</thinking>"
                },
                {
                    "type": "tool_use",
                    "id": "msg_01QTz7uReVbyUE8j7NSyjtfT",
                    "name": "get_weather",
                    "input": {"location": "San Francisco, CA", "unit": "celsius"}
                }
            ]
        },
        {
            "role": "user", "content": "I am here in gandhinagar, gujarat"
        }
    ]
)

print(response)
