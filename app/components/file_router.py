import os
import pandas as pd
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

def load_document_definitions(file_path: str = "docs/file_name_definitions.csv"):
    """
    Loads document definitions from the CSV file.
    This fulfills Step 1 of the architecture.
    """
    try:
        # Assuming the script is run from the root of the project,
        # and we have an 'app' directory.
        # The path in the original code assumed execution from within 'app/components'.
        # Let's make it more robust by using an absolute path approach or by
        # ensuring the path is relative to the project root.
        # For now, the original path will work if we run main.py from the app folder.
        # Let's adjust for running from the project root.
        df = pd.read_csv(file_path)
        if 'File' not in df.columns or 'Description' not in df.columns:
            raise ValueError("CSV must have 'File' and 'Description' columns.")
        definitions = dict(zip(df['File'], df['Description']))
        return definitions
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return {}
    except Exception as e:
        print(f"An error occurred while loading document definitions: {e}")
        return {}

def route_query_to_files(query: str, doc_definitions: dict):
    """
    Uses GPT-4o to select relevant files based on a user query.
    This fulfills Step 2 (B) of the architecture.
    """
    if not doc_definitions:
        print("Error: Document definitions are empty. Cannot route query.")
        return []

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return []

    client = OpenAI(api_key=api_key)

    documents_prompt_part = "\n".join([f"- {fname}: {desc}" for fname, desc in doc_definitions.items()])

    prompt = f"""
You are an assistant for RevPilot AI, sales automation SaaS platform that helps B2B teams generate more pipeline with less manual work a, that classifies which documents are relevant to a user's question.

Your job is to:
- Read a user's question.
- Carefully review a set of document filenames and their short descriptions.
- Return the filenames of up to 3 documents that best match the question.
- If none match, return an empty list.

---

🧠 User Question:
"{query}"

---

📄 Available Documents:
{documents_prompt_part}

---

🔍 Matching Guidelines:
- Match documents that clearly relate to the intent and meaning of the user's question — not just exact words.
- Prioritize documents where the description or filename contains direct references to the concepts in the question.
- Treat filenames as meaningful indicators of content. If the filename contains a close match to the user’s phrasing, strongly consider selecting it.
- If the question is ambiguous (e.g. “our onboarding”), use common sense: prefer internal documents over customer-facing ones unless stated otherwise.
- Select up to 3 documents. If no documents are clearly relevant, return an empty list.
- Do not fabricate or modify filenames under any circumstance.

---

Output Format:
Respond with a JSON object using this format:

{{"files": ["exact_file_name_1.txt", "exact_file_name_2.txt"]}}

If there are no relevant documents, respond with:

{{"files": []}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that strictly follows instructions and returns JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        llm_output = json.loads(response.choices[0].message.content)
        
        # Check if 'files' key exists and it's a list
        selected_files = llm_output.get("files")
        if selected_files is None or not isinstance(selected_files, list):
            print("LLM response is not in the expected format: missing 'files' key or it's not a list.")
            # The architecture specifies returning an empty list for no relevant documents.
            # So if the model returns {"files": []} or just {}, we handle it.
            if selected_files is None and isinstance(llm_output, dict):
                 return [] # No files found is a valid case.
            return []

        # Validate filenames against the provided definitions
        validated_files = [f for f in selected_files if f in doc_definitions]
        
        return validated_files

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from LLM response.")
        return []
    except Exception as e:
        print(f"An error occurred while routing query: {e}")
        return [] 