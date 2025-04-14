#!/bin/bash
read -p "Prompt: " PROMPT
read -p "Language: " LANGUAGE

curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -N \
  -d "{\"prompt\": \"$PROMPT\", \"language\": \"$LANGUAGE\"}"
