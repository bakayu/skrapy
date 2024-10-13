from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")

template = (
    "You are tasked with extracting specific information from the following text content: {dom_list}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {prompt}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parseLocal(dom_list, prompt):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_list, start=1):
        response = chain.invoke(
            {"dom_list": chunk, "prompt": prompt}
        )
        print(f"Parsed batch: {i} of {len(dom_list)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)