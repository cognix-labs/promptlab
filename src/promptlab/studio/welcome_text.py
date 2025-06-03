from art import tprint
def print_welcome_text(port: int) -> None:
    """Print the welcome text and port number.
    
    Args:
        port (int): The port number to display
    """

    tprint("PromptLab")
    print(f"\n🚀 PromptLab Studio running on: http://localhost:{port} 🚀")