from langchain_cerebras import ChatCerebras

class LlmStruct:
    def __new__(cls):
        LlmStruct = ChatCerebras(model='llama-3.3-70b', temperature=0.7, max_tokens=800)
        return LlmStruct