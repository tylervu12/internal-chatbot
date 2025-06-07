# 🧠 Internal Document QA Chatbot

This project is a simple, lightweight internal chatbot designed to answer questions based on a collection of text documents (`.txt` files). It uses GPT-4o to understand user queries and find relevant information within the provided documents, all served through a clean, password-protected Gradio web interface.

The key design principle is to **avoid complex retrieval pipelines** like vector databases and embeddings. Instead, it leverages the large context window of modern LLMs by dynamically loading the full content of relevant files into the prompt.

## ✨ Features

*   **Dynamic File Routing**: If no documents are selected, the chatbot uses GPT-4o to intelligently choose the most relevant files based on the user's question.
*   **Manual File Selection**: Users can manually select up to 3 documents to narrow the scope of their query.
*   **Secure Access**: The Gradio interface is protected by a username and password, configured via environment variables.
*   **Transparent & Traceable**: The UI displays the exact documents (citations) used to generate an answer and provides an expandable view of the raw source content.
*   **Simple & Maintainable**: Built with standard Python libraries and a clear, component-based structure.

## 🏗️ Architecture

The application is built with the following components:

*   **Backend**: Python
*   **UI**: Gradio
*   **LLM**: OpenAI GPT-4o
*   **File Metadata**: A `file_name_definitions.csv` file maps document filenames to user-friendly descriptions, which are used by the file router.
*   **Knowledge Base**: A `docs/` directory containing all the `.txt` source documents.

## 📂 Project Structure

```
repo/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Main entrypoint to launch the UI
│   ├── ui.py                    # Gradio UI definition and logic
│   └── components/
│       ├── __init__.py
│       ├── doc_loader.py        # Loads content from .txt files
│       ├── file_router.py       # Selects relevant files via LLM call
│       └── gpt_prompter.py      # Generates the final answer via LLM call
├── docs/
│   ├── file_name_definitions.csv # Maps filenames to descriptions
│   ├── faq_customers.txt
│   └── ... (other .txt files)
├── .env                         # Stores environment variables (API keys, credentials)
├── requirements.txt             # Python dependencies
└── README.md
```

## 🚀 Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` in the root of the project directory and add the following variables.

```
# Your secret API key from OpenAI
OPENAI_API_KEY="sk-..."

# Credentials for the Gradio UI
GRADIO_USER="your_username"
GRADIO_PASSWORD="your_password"
```

Replace the placeholder values with your actual OpenAI API key and your desired username and password for the web app.

## ▶️ How to Run the Application

Once the setup is complete, you can launch the Gradio web application with a single command:

```bash
python -m app.main
```

The terminal will output something like this:

```
Gradio authentication enabled.
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://....gradio.live
```

You can open either the local or public URL in your browser. You will be prompted to enter the username and password you configured in your `.env` file.

## 🤝 How to Use the Chatbot

1.  **Ask a Question**: Type your question into the text box.
2.  **(Optional) Select Files**: If you know which documents are relevant, you can select up to 3 from the dropdown. This will skip the AI routing step and use only the files you've chosen.
3.  **Get Answer**: Click the "Get Answer" button. The bot will display the answer, the source documents it used, and the raw content from those sources for you to review.

## ☁️ Deployment

This application is ready to be deployed on platforms like Hugging Face Spaces. The use of environment variables for credentials and API keys makes it easy to configure securely in a cloud environment. The `share=True` flag in the `launch()` method automatically generates a public link suitable for this purpose. 