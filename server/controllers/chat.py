from config import client, messages, model, fallback_models
from openai.types.chat import ChatCompletionMessage
from fastapi.responses import StreamingResponse
from tool_config import tools, tool_mapping
import json

def stream_response(prompt: str, language: str = "en"):
    language_instruction = {
        "role": "system",
        "content": f"Respond in the given language: {language}"
    }

    messages.append(language_instruction)
    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    def event_stream():
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            extra_body={
                "models": fallback_models
            },
            stream=True
        )

        for chunk in stream:
            if content := chunk.choices[0].delta.content:
                yield content

    return StreamingResponse(event_stream(), media_type="text/plain")

def generate_response(prompt: str, language: str = "en"):
    print(prompt)
    language_instruction = {
        "role": "system",
        "content": f"Respond in the given language: {language}"
    }

    messages.append(language_instruction)
    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_body={
            "models": fallback_models
        },
        tools=tools,
    )

    messages.append(response.choices[0].message)
    print(json.dumps(response.model_dump(), indent=4))

    if hasattr(response.choices[0].message, "tool_calls") and response.choices[0].message.tool_calls:
        tool_calls = response.choices[0].message.tool_calls

        for tool_call in tool_calls:
            print(f"Suggested tool: {tool_call.function.name}\n")
            results = tool_mapping[tool_call.function.name]()

            messages.append({
                "role": "tool",
                "name": tool_call.function.name,
                "content": str(results)
            })

        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
            extra_body={
                "models": fallback_models
            },
            tools=tools
        )

        messages.append(final_response.choices[0].message)
        return final_response
    else:
        messages.append(response.choices[0].message)
        return response

def get_chat_history():
    return messages