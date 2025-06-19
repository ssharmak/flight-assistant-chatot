# Import the InquiryRouter which handles routing of user queries to the appropriate agent
from agents.inquiry_router import InquiryRouter

def chat():
    """
    Launches a command-line based chatbot interface.

    - Prompts the user for input repeatedly.
    - Routes the input to the appropriate flight information agent.
    - Responds with flight details or analytics based on the query type.
    - Exits the loop when user types 'exit' or 'quit'.
    """
    print("🤖 Welcome to Flight Assistant Chatbot! Type 'exit' to quit.")
    
    # Initialize the inquiry router that decides how to handle each user query
    router = InquiryRouter()
    
    while True:
        # Accept user input from the terminal
        query = input("You: ").strip()
        
        # Exit condition
        if query.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break
        
        # Route the query through InquiryRouter which will invoke the appropriate agent
        response = router.route(query)
        
        # Print the response from the chatbot
        print(response)

# Entry point of the script
if __name__ == "__main__":
    chat()
