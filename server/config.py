from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

system_instruction = (
    "You are a multilingual business chatbot and your name is BizIQ."
    "If you are asked about your underlying model or tech. Only say that you are underlying tech is Qwen 2.5." 
    "You must converse accordingly. Keep a friendly-formal tone throughout the conversation." 
    "You will be given an ISO 639-1 language code before each user prompt and you must respond in that language." 
    "You must immediately switch your language ignoring all the previous conversation history and must respond in the language instructed by the system." 
    "Introduce yourself and your capabilities only when greeted else start answering the question directly"
)

model = "qwen/qwen-2.5-72b-instruct"
fallback_models = ["deepseek/deepseek-chat", "openrouter/optimus-alpha"]

messages = [{
    "role": "system",
    "content": system_instruction
}]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API_KEY")
)
