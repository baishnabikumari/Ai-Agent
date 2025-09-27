from Backend.model import query_openai, query_groq

def get_response(user_input: str, mode="auto") -> str:
    if mode == "openai":
        return query_openai(user_input)
    elif mode == "groq":
        return query_groq(user_input)
    else:
        response = query_openai(user_input)
        if "Error" in response:
            response = query_groq(user_input)
        return response