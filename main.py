# main.py
# =========================================
# MAIN ENTRY POINT
# This is the file you run! It starts the
# Multi-Agent Code Generator.
#
# How to run:
#   python main.py
# =========================================

from colorama import Fore, Style, init
from orchestrator import Orchestrator

# Initialize colored terminal output
init(autoreset=True)


def print_welcome():
    """Print a welcome banner when the app starts."""
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════════════════════╗
║        🤖 Multi-Agent Code Generator                     ║
║        Powered by Google Gemini + LangChain              ║
║                                                          ║
║  Agents: Planning → Designing → Creating → Testing       ║
╚══════════════════════════════════════════════════════════╝
""")


def print_examples():
    """Show the user some example questions they can ask."""
    print(Fore.YELLOW + "💡 Example questions you can ask:")
    examples = [
        "Create a simple calculator with add, subtract, multiply, divide",
        "Build a to-do list app that saves tasks to a file",
        "Write a web scraper that gets headlines from a news website",
        "Create a student grade management system",
        "Build a simple number guessing game",
    ]
    for i, example in enumerate(examples, 1):
        print(Fore.WHITE + f"  {i}. {example}")
    print()


def get_user_input() -> str:
    """
    Ask the user what they want to build.
    Keeps asking until they provide a non-empty request.
    
    Returns:
        The user's coding request as a string
    """
    while True:
        print(Fore.GREEN + "Enter your coding request below.")
        print(Fore.GREEN + "Type 'examples' to see examples, or 'quit' to exit.")
        print(Fore.WHITE + "-" * 50)
        
        user_input = input(Fore.CYAN + "🤖 What do you want to build? " + Style.RESET_ALL).strip()
        
        # Handle special commands
        if user_input.lower() == "quit":
            print(Fore.YELLOW + "\n👋 Goodbye! Happy coding!")
            return None
        
        if user_input.lower() == "examples":
            print_examples()
            continue
        
        # Make sure the user typed something
        if not user_input:
            print(Fore.RED + "❌ Please enter a request. Don't leave it empty!\n")
            continue
        
        # Make sure it's not too short
        if len(user_input) < 10:
            print(Fore.RED + "❌ Please be more descriptive (at least 10 characters).\n")
            continue
        
        return user_input


def ask_save_results() -> bool:
    """Ask the user if they want to save results to a file."""
    answer = input(Fore.YELLOW + "\n💾 Save results to a file? (yes/no): " + Style.RESET_ALL).strip().lower()
    return answer in ["yes", "y"]


def main():
    """
    Main function - the entry point of the application.
    This is what runs when you execute: python main.py
    """
    
    # Show welcome banner
    print_welcome()
    
    # Show example questions
    print_examples()
    
    # Create the orchestrator (this initializes all agents and connects to Gemini)
    try:
        orchestrator = Orchestrator()
    except ValueError as e:
        # API key error - show helpful message and stop
        print(Fore.RED + f"\n❌ Setup Error: {e}")
        return
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error during startup: {e}")
        return
    
    # Main interaction loop - keep running until user types 'quit'
    while True:
        print("\n")
        
        # Get what the user wants to build
        user_request = get_user_input()
        
        # If user typed 'quit', exit the loop
        if user_request is None:
            break
        
        print(Fore.CYAN + f"\n✨ Great! Running all 4 agents on your request...")
        print(Fore.CYAN + f"⏳ This may take 30-60 seconds. Please wait...\n")
        
        # Run all 4 agents through the orchestrator
        try:
            results = orchestrator.run(user_request)
            
            # Display all results in a readable format
            orchestrator.display_results(results)
            
            # Ask if user wants to save
            if ask_save_results():
                # Create a filename from the request (first 3 words)
                words = user_request.split()[:3]
                filename = "_".join(words).lower().replace("/", "").replace("\\", "")
                orchestrator.save_results(results, filename)
            
            # Ask if they want to try another request
            print()
            again = input(Fore.YELLOW + "🔄 Try another request? (yes/no): " + Style.RESET_ALL).strip().lower()
            if again not in ["yes", "y"]:
                print(Fore.GREEN + "\n👋 Thank you for using Multi-Agent Code Generator!")
                print(Fore.GREEN + "💡 Tip: Check the saved output files for your generated code.")
                break
                
        except KeyboardInterrupt:
            # User pressed Ctrl+C
            print(Fore.YELLOW + "\n\n⏹️  Stopped by user. Goodbye!")
            break
        except Exception as e:
            print(Fore.RED + f"\n❌ Error during generation: {e}")
            print(Fore.YELLOW + "💡 Common fixes:")
            print(Fore.YELLOW + "   - Check your internet connection")
            print(Fore.YELLOW + "   - Verify your API key in .env file")
            print(Fore.YELLOW + "   - Make sure your Gemini API quota isn't exceeded")
            
            # Ask if they want to try again
            retry = input(Fore.YELLOW + "\nTry again? (yes/no): " + Style.RESET_ALL).strip().lower()
            if retry not in ["yes", "y"]:
                break


# This is the standard Python way to run the main function
# It only runs when you execute this file directly (not when imported)
if __name__ == "__main__":
    main()