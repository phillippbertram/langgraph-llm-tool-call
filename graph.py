from typing import Annotated, TypedDict, Sequence
from langgraph.graph import Graph, StateGraph
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
#from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3

# Load environment variables
load_dotenv()

# Define the state that will be passed between nodes
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Create the LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
)

# Create the memory saver
#memory = MemorySaver()
memory = SqliteSaver(sqlite3.connect("memory.db", check_same_thread=False))

# Initialize Google Serper
search = GoogleSerperAPIWrapper()

# Define the search tool
#@tool
def search_web(query: str) -> str:
    """Search the web for current information about a topic."""
    return search.run(query)

# Create tools list
search_tool = Tool(name="search_web", func=search_web, description="Search the web for current information about a topic.")
tools = [search_tool]

# print("==="*10)
# print(search_tool.invoke("What is the current time in Tokyo?"))
# print("==="*10)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant with access to web search capabilities.
    When you need current information or facts, use the search_web tool to find accurate and up-to-date information.
    Always provide clear and concise responses, and cite your sources when using information from the web."""),
    MessagesPlaceholder(variable_name="messages"),
])




# Agent node that uses the LLM
def agent_node(state: AgentState) -> AgentState:
    """Process messages using the LLM with web search capabilities."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Create the graph
def create_graph() -> Graph:

    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add the agent node
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools=tools))
    
    # Set the entry point
    workflow.set_entry_point("agent")
    
    # Set the exit point
    workflow.set_finish_point("agent")

    workflow.add_conditional_edges("agent", tools_condition, "tools")
    workflow.add_edge("tools", "agent")
    
    # Compile the graph
    graph = workflow.compile(checkpointer=memory)
    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
    return graph

# Initialize the graph
graph = create_graph() 