from controllers import metrics

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_data",
            "description": "Get all of the business metrics from the database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

tool_mapping = {
    "get_data": metrics.get_data
}