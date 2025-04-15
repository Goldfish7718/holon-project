from config import client, messages, model, fallback_models
from fastapi.responses import StreamingResponse
from tool_config import tools, tool_mapping
import json
import sys

def stream_response(prompt: str, language: str = "en"):
    print("Stream response hit")
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

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        extra_body={
            "models": fallback_models
        },
        stream=True
    )

    full_content = ""
    final_tool_calls = []

    for event in stream:
        event_delta = event.choices[0].delta

        if event_delta.tool_calls is None or len(event_delta.tool_calls) is 0:
            full_content += event_delta.content
            sys.stdout.write(event_delta.content)
            sys.stdout.flush()
        else:
            for tool_call in event_delta.tool_calls:
                if tool_call.id:
                    final_tool_calls.append(tool_call)

    messages.append({
        "role": "assistant",
        "content": full_content,
        "tool_calls": final_tool_calls
    })

    if final_tool_calls:
        for tool_call in final_tool_calls:
            results = tool_mapping[tool_call.function.name]()

            messages.append({
                "role": "tool",
                "name": tool_call.function.name,
                "content": str(results)
            })

        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            extra_body={
                "models": fallback_models
            },
            stream=True
        )

        final_content = ""

        for event in stream:
            event_delta = event.choices[0].delta

            final_content += event_delta.content
            sys.stdout.write(event_delta.content)
            sys.stdout.flush()

        messages.append({
            "role": "assistant",
            "content": final_content
        })
            
    # return StreamingResponse(event_stream(), media_type="text/plain")

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