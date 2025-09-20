import os
import uuid
from typing import Literal, Annotated, List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

# Import our tools
from tools import AVAILABLE_TOOLS

# Load environment variables
load_dotenv()

# Ensure we have the OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Please set the OPENAI_API_KEY environment variable in .env file")


# Define the state
class State(BaseModel):
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)
    user_input: str = ""


# Initialize the LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.3)
llm_with_tools = llm.bind_tools(AVAILABLE_TOOLS)

# System message for the agent
SYSTEM_MSG = """You are an energy usage saver assistant that can analyze bill usage and kwh cost based on the dates the user provides.
Always try to call a tool if the question requires data retrieval.

If a tool is relevant, return a tool call with its parameters.
If no tool fits, answer normally in one paragraph (max 500 words).
"""


def chatbot(state: State) -> dict:
    """Process the user input and generate a response."""
    messages = state.messages
    system_message = SystemMessage(content=SYSTEM_MSG)

    # Prepare the conversation history
    chat_history = [system_message] + messages

    # Get the response from the model
    response = llm_with_tools.invoke(chat_history)

    return {"messages": [response]}


def should_continue(state: State) -> Literal["__end__", "continue"]:
    """Determine if we should continue processing or end the conversation."""
    messages = state.messages
    if not messages:
        return "__end__"

    last_message = messages[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "continue"
    return "__end__"


# Create the graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=AVAILABLE_TOOLS))

# Define the edges
graph_builder.add_conditional_edges(
    "chatbot",
    should_continue,
    {"continue": "tools", "__end__": "__end__"}
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

# Compile the graph
graph = graph_builder.compile()


def process_query(user_input: str, thread_id: str = None) -> str:
    """Process a user query and return the response."""
    if not thread_id:
        thread_id = str(uuid.uuid4())

    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "user_input": user_input
    }

    # Process the query through the graph
    response = graph.invoke(initial_state)

    # Extract the final response
    if response and 'messages' in response and response['messages']:
        last_message = response['messages'][-1]
        if hasattr(last_message, 'content'):
            return last_message.content
        return str(last_message)
    return "I couldn't generate a response. Please try again."


if __name__ == "__main__":
    print("Energy Usage Analysis Agent")
    print("Type 'quit' to exit")
    print("-" * 30)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break

        response = process_query(user_input)
        print(f"\nAssistant: {response}")
