import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_answer(question: str, context: str, citation_filenames: list):
    """
    Generates an answer to a question based on the provided context from files.

    This function implements Step 4 and 5 of the architecture.

    Args:
        question (str): The user's question.
        context (str): The formatted string containing the content of all source documents.
        citation_filenames (list): The list of filenames used for context, for citation purposes.

    Returns:
        dict: A dictionary containing the answer and citations, e.g.,
              {"answer": "...", "citations": ["file1.txt"]}.
              Returns an empty dictionary on failure.
    """
    if not question or not context:
        return {}

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return {}

    client = OpenAI(api_key=api_key)

    prompt = f"""You are an assistant answering internal team questions using provided SOPs and documentation.

Below are 1–3 full documents. Use only this content to answer the user's question. If an answer is not found, say so.

- Cite document names in-line like (source: onboarding.txt).
- Do not hallucinate.
- Be concise and specific.

{context}
---
QUESTION: {question}
---
Based on the documents provided, generate a structured JSON response with two keys:
1. "answer": A string containing the direct answer to the question.
2. "citations": A JSON list of the exact filenames of the documents you used to formulate the answer.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides answers in structured JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        llm_output = json.loads(response.choices[0].message.content)

        # Basic validation of the returned object
        if "answer" in llm_output and "citations" in llm_output:
            # Further validation: ensure citations are a subset of source files
            llm_output["citations"] = [c for c in llm_output["citations"] if c in citation_filenames]
            return llm_output
        else:
            print("Warning: LLM response did not contain 'answer' and 'citations' keys.")
            return {"answer": "The model did not return a valid response.", "citations": []}

    except Exception as e:
        print(f"An error occurred while generating the answer: {e}")
        return {}

if __name__ == '__main__':
    # Example usage for testing the component directly
    print("--- Testing gpt_prompter.py ---")

    # Mock data based on previous steps
    test_question = "How do I onboard a new customer?"
    test_filenames = ["customer_onboarding.txt"]
    
    # Mock file loader output
    from doc_loader import load_file_contents
    test_context = load_file_contents(test_filenames, base_path="../../docs/")

    if test_context:
        print(f"\nQuestion: {test_question}")
        print(f"Using files: {test_filenames}")
        final_response = generate_answer(test_question, test_context, test_filenames)
        print("\n--- Final Structured Response ---")
        print(json.dumps(final_response, indent=2))
    else:
        print("\nCould not load test context. Aborting test.") 