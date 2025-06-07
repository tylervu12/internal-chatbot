import os

def load_file_contents(filenames: list, base_path: str = "docs/"):
    """
    Loads the full content of specified text files and formats them into a single string.

    This function implements Step 3 of the architecture.

    Args:
        filenames (list): A list of filenames to load (e.g., ["onboarding.txt"]).
        base_path (str): The directory where the .txt files are stored.

    Returns:
        str: A single string containing the formatted content of all files,
             or an empty string if no files could be read.
    """
    if not filenames:
        return ""

    all_content = []
    
    for filename in filenames:
        file_path = os.path.join(base_path, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                formatted_content = (
                    f"--- START OF FILE: {filename} ---\n"
                    f"{content}\n"
                    f"--- END OF FILE: {filename} ---\n"
                )
                all_content.append(formatted_content)
        except FileNotFoundError:
            print(f"Warning: File not found at '{file_path}'. Skipping.")
        except Exception as e:
            print(f"Warning: Could not read file '{file_path}'. Reason: {e}. Skipping.")
            
    return "\n".join(all_content)

if __name__ == '__main__':
    # Example usage for testing the component directly
    print("--- Testing doc_loader.py ---")
    
    # Test with valid files
    test_files_1 = ["customer_onboarding.txt", "demo_to_close.txt"]
    print(f"\nLoading files: {test_files_1}")
    loaded_content_1 = load_file_contents(test_files_1)
    print(loaded_content_1)

    # Test with a mix of valid and invalid files
    test_files_2 = ["faq_customers.txt", "non_existent_file.txt"]
    print(f"\nLoading files: {test_files_2}")
    loaded_content_2 = load_file_contents(test_files_2)
    print(loaded_content_2)

    # Test with an empty list
    test_files_3 = []
    print(f"\nLoading files: {test_files_3}")
    loaded_content_3 = load_file_contents(test_files_3)
    print(f"Result for empty list: '{loaded_content_3}'") 