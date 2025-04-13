from config import client, messages, model, fallback_models

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

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_body={
            "models": fallback_models
        }
    )

    return completion
