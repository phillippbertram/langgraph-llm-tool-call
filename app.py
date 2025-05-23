import gradio as gr
from typing import List, Tuple
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv(override=True)

from graph import graph

def chat(message: str, history: List[Tuple[str, str]]) -> str:
    """Process the chat message using LangGraph and return a response."""
    # Convert the message to a HumanMessage
    human_message = HumanMessage(content=message)
    
    # Run the graph with the new message
    config = {"configurable": {"thread_id": "1"}} # thread_id is used to track the conversation and memory
    result = graph.invoke({"messages": [human_message]}, config=config)
    
    # Get the last message (the AI response)
    response = result["messages"][-1].content
    
    return response

# Create the Gradio interface
demo = gr.ChatInterface(
    fn=chat,
    title="LangGraph Chat",
    description="Chat with your LangGraph-powered assistant",
    # theme=gr.themes.Soft(),
    examples=["Hello!", "How can you help me?", "What can you do?"],
)

if __name__ == "__main__":
    demo.launch() 