from config import client, messages, model, fallback_models
from fastapi.responses import StreamingResponse
from tool_config import tools, tool_mapping
import json
import sys

def stream_response(prompt: str, language: str = "en"):
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

    def event_stream():
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
            if hasattr(event_delta, 'content') and event_delta.content is not None:
                chunk = event_delta.content
                full_content += chunk
                yield chunk

            if event_delta.tool_calls:
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
                print(json.dumps(results, indent=4))

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(results)
                })

            final_response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                extra_body={
                    "models": fallback_models
                },
                stream=True
            )

            for event in final_response:
                if hasattr(event.choices[0].delta, 'content') and event.choices[0].delta.content is not None:
                    yield event.choices[0].delta.content

    return StreamingResponse(event_stream(), media_type="text/event-stream")

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