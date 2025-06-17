from agents.inquiry_router import InquiryRouter

def chat():
    router = InquiryRouter()
    while True:
        query = input("You: ").strip()
        if query.lower() in ("exit", "quit"):
            print("Goodbye! 👋")
            break
        print(router.route(query))

if __name__ == "__main__":
    chat()
