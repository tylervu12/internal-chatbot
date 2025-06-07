import os
from dotenv import load_dotenv
from .ui import create_ui

load_dotenv()

def main():
    """
    Main entry point to create and launch the Gradio UI.
    Handles authentication setup.
    """
    app = create_ui()

    # Get authentication credentials from environment variables
    auth_user = os.getenv("GRADIO_USER")
    auth_password = os.getenv("GRADIO_PASSWORD")

    auth_tuple = None
    if auth_user and auth_password:
        print("Gradio authentication enabled.")
        auth_tuple = (auth_user, auth_password)

    # Launch the app with or without authentication
    app.launch(auth=auth_tuple, share=True)

if __name__ == "__main__":
    main() 