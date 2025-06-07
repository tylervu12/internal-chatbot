import gradio as gr
import os
from dotenv import load_dotenv
from .components.file_router import load_document_definitions, route_query_to_files
from .components.doc_loader import load_file_contents
from .components.gpt_prompter import generate_answer

load_dotenv()

# --- 1. LOAD GLOBAL OBJECTS ---
# Load document definitions once at startup
DOC_DEFINITIONS = load_document_definitions("docs/file_name_definitions.csv")
AVAILABLE_FILES = list(DOC_DEFINITIONS.keys())

# --- 2. DEFINE CORE CHATBOT LOGIC ---
def get_bot_response(user_question, selected_files):
    """
    Main function to power the chatbot.
    Orchestrates the 4 steps of the backend logic.
    """
    if not user_question:
        return "Please enter a question.", "", ""

    # Step 2: Route query to files (if none selected)
    if not selected_files:
        print("No files selected by user. Routing query...")
        selected_files = route_query_to_files(user_question, DOC_DEFINITIONS)
        if not selected_files:
            return "Our documents do not seem to contain an answer to that question. Please try rephrasing or selecting a document.", "", ""
    
    # Step 3: Load file contents
    print(f"Loading content from: {selected_files}")
    context_str = load_file_contents(selected_files)
    if not context_str:
        return "Could not load the content of the selected files.", "", ""

    # Step 4: Generate final answer
    print("Generating final answer...")
    response_dict = generate_answer(user_question, context_str, selected_files)

    # Format output
    answer = response_dict.get("answer", "Sorry, I couldn't generate an answer.")
    citations = "\n".join([f"- {c}" for c in response_dict.get("citations", [])])
    
    # Create an expandable section for the raw source context
    source_context_details = f"<details><summary>Click to view source content</summary>\n\n{context_str}\n\n</details>"
    
    return answer, citations, source_context_details

# --- 3. BUILD GRADIO UI ---
def create_ui():
    """
    Creates and returns the Gradio UI application.
    """
    with gr.Blocks(title="Internal Doc QA Chatbot", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 🧠 Internal Doc QA Chatbot")
        gr.Markdown("Ask questions about our internal processes and documentation. Select up to 3 files to narrow the search or let the AI choose for you.")

        with gr.Row():
            with gr.Column(scale=1):
                file_selector = gr.Dropdown(
                    label="Select Files (Optional, Max 3)",
                    choices=AVAILABLE_FILES,
                    multiselect=True,
                    max_choices=3
                )
                question_input = gr.Textbox(
                    label="Question",
                    placeholder="e.g., How do I onboard a new customer?",
                    lines=4
                )
                submit_button = gr.Button("Get Answer", variant="primary")
            
            with gr.Column(scale=2):
                gr.Markdown("### Answer")
                answer_output = gr.Markdown()
                gr.Markdown("### Citations (Sources Used)")
                citations_output = gr.Markdown()
                gr.Markdown("### Raw Source Content")
                source_context_output = gr.Markdown()

        # Connect components
        submit_button.click(
            fn=get_bot_response,
            inputs=[question_input, file_selector],
            outputs=[answer_output, citations_output, source_context_output]
        )

    return app 