# chatbot.py
from agents.inquiry_router import InquiryRouter

def chat():
    print("🤖 Welcome to Flight Assistant Chatbot! Type 'exit' to quit.")
    router = InquiryRouter()
    while True:
        query = input("You: ").strip()
        if query.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break
        response = router.route(query)
        print(response)

if __name__ == "__main__":
    chat()
