from config import client, messages, model, fallback_models
from fastapi.responses import StreamingResponse

def generate_response(prompt: str, language: str = "en"):
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
