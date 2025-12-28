"""
LangGraph-based Trip Planner Agent

This module implements a multi-agent trip planning system using LangGraph,
where different agents handle different aspects of trip planning.
"""

import os
import time
import uuid
from typing import Dict, List, Any, TypedDict, Annotated
from datetime import datetime, timedelta
import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Import Langfuse integration
try:
    from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler
    from langfuse import Langfuse
    from langfuse.decorators import observe
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    LangfuseCallbackHandler = None
    Langfuse = None
    # Create a no-op decorator when Langfuse is not available
    def observe(name=None):
        def decorator(func):
            return func
        return decorator

# Initialize the LLM lazily to avoid hanging on import
llm = None
langfuse_client = None

def get_langfuse_client():
    """Get or create the Langfuse client for workflow tracing."""
    global langfuse_client
    if langfuse_client is None and LANGFUSE_AVAILABLE and Langfuse:
        try:
            langfuse_client = Langfuse()
            print("✅ Langfuse client initialized for workflow tracing")
        except Exception as e:
            print(f"⚠️  Failed to initialize Langfuse client: {e}")
            langfuse_client = None
    return langfuse_client

def get_llm():
    """Get or create the LLM instance with OpenInference instrumentation and Langfuse tracing."""
    global llm
    if llm is None:
        # Initialize Langfuse callback handler if available
        callbacks = []
        if LANGFUSE_AVAILABLE and LangfuseCallbackHandler:
            try:
                # Langfuse callback handler gets credentials from environment variables automatically
                langfuse_handler = LangfuseCallbackHandler()
                callbacks.append(langfuse_handler)
                print("✅ Langfuse callback handler initialized")
            except Exception as e:
                print(f"⚠️  Failed to initialize Langfuse callback handler: {e}")
        
        # Initialize the LLM (OpenInference will automatically instrument it)
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
            callbacks=callbacks  # Add Langfuse callback for tracing
        )
    return llm

class TripPlanningState(TypedDict):
    """State for the trip planning workflow"""
    messages: Annotated[list, add_messages]
    destination: str
    duration: int
    budget: float
    interests: List[str]
    travel_dates: Dict[str, str]
    accommodation_preferences: Dict[str, Any]
    transportation_preferences: Dict[str, Any]
    itinerary: List[Dict[str, Any]]
    recommendations: Dict[str, Any]
    final_plan: Dict[str, Any]

class TripRequest(BaseModel):
    """Input model for trip planning requests"""
    destination: str = Field(..., description="The destination for the trip")
    duration: int = Field(..., description="Duration of the trip in days")
    budget: float = Field(..., description="Total budget for the trip")
    interests: List[str] = Field(default_factory=list, description="List of interests/activities")
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")
    accommodation_type: str = Field(default="hotel", description="Type of accommodation preferred")
    transportation_type: str = Field(default="flight", description="Preferred transportation method")

# Define tools for the agents
@tool
def research_destination(destination: str) -> str:
    """Research information about a destination including weather, culture, and attractions."""
    # In a real implementation, this would call external APIs
    research_data = {
        "paris": {
            "weather": "Mild climate, best visited in spring or fall",
            "culture": "Rich history, art, and cuisine",
            "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Champs-Élysées"],
            "currency": "Euro",
            "language": "French"
        },
        "tokyo": {
            "weather": "Four distinct seasons, cherry blossoms in spring",
            "culture": "Traditional and modern blend, excellent food scene",
            "attractions": ["Tokyo Skytree", "Senso-ji Temple", "Shibuya Crossing", "Tsukiji Market"],
            "currency": "Japanese Yen",
            "language": "Japanese"
        },
        "new york": {
            "weather": "Four seasons, can be cold in winter",
            "culture": "Diverse, fast-paced, cultural hub",
            "attractions": ["Statue of Liberty", "Central Park", "Times Square", "Broadway"],
            "currency": "US Dollar",
            "language": "English"
        }
    }
    
    dest_lower = destination.lower()
    if dest_lower in research_data:
        return json.dumps(research_data[dest_lower], indent=2)
    else:
        return f"Research data for {destination} not available. Please provide more details about your destination."

@tool
def calculate_budget_breakdown(budget: float, duration: int, destination: str) -> str:
    """Calculate a budget breakdown for the trip."""
    # Basic budget allocation
    accommodation_percent = 0.4
    food_percent = 0.3
    activities_percent = 0.2
    transportation_percent = 0.1
    
    breakdown = {
        "accommodation": budget * accommodation_percent,
        "food": budget * food_percent,
        "activities": budget * activities_percent,
        "transportation": budget * transportation_percent,
        "daily_budget": budget / duration,
        "total_budget": budget
    }
    
    return json.dumps(breakdown, indent=2)

@tool
def generate_itinerary(destination: str, duration: int, interests: List[str], budget: float) -> str:
    """Generate a detailed day-by-day itinerary."""
    # Sample itinerary generation
    itinerary = []
    
    for day in range(1, duration + 1):
        day_plan = {
            "day": day,
            "morning": f"Explore {destination} - Visit local attractions",
            "afternoon": f"Enjoy {interests[0] if interests else 'local culture'}",
            "evening": "Dinner at local restaurant",
            "estimated_cost": budget / duration * 0.3
        }
        itinerary.append(day_plan)
    
    return json.dumps(itinerary, indent=2)

@tool
def find_accommodations(destination: str, budget: float, accommodation_type: str) -> str:
    """Find suitable accommodations within budget."""
    # Sample accommodation data
    accommodations = {
        "budget": [
            {"name": "Budget Hostel", "price": budget * 0.2, "rating": 3.5},
            {"name": "Guesthouse", "price": budget * 0.25, "rating": 4.0}
        ],
        "mid_range": [
            {"name": "3-Star Hotel", "price": budget * 0.3, "rating": 4.2},
            {"name": "Boutique Hotel", "price": budget * 0.35, "rating": 4.5}
        ],
        "luxury": [
            {"name": "5-Star Hotel", "price": budget * 0.5, "rating": 4.8},
            {"name": "Luxury Resort", "price": budget * 0.6, "rating": 4.9}
        ]
    }
    
    # Determine budget category
    if budget < 1000:
        category = "budget"
    elif budget < 3000:
        category = "mid_range"
    else:
        category = "luxury"
    
    return json.dumps(accommodations[category], indent=2)

# Create the tools list
tools = [research_destination, calculate_budget_breakdown, generate_itinerary, find_accommodations]
tool_node = ToolNode(tools)

# Define agent functions
@observe(name="research_agent")
def research_agent(state: TripPlanningState) -> TripPlanningState:
    """Agent responsible for researching the destination."""
    messages = state["messages"]
    destination = state.get("destination", "Unknown")
    
    system_prompt = f"""You are a travel research specialist. Your job is to gather comprehensive information about {destination}.
    Use the research_destination tool to get information about {destination}.
    Provide detailed insights about weather, culture, attractions, and practical information for {destination}.
    Focus specifically on {destination} and provide accurate, destination-specific information."""
    
    response = get_llm().invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])
    
    return {
        **state,
        "messages": [response]
    }

@observe(name="budget_agent")
def budget_agent(state: TripPlanningState) -> TripPlanningState:
    """Agent responsible for budget planning and allocation."""
    messages = state["messages"]
    
    system_prompt = """You are a budget planning specialist. Your job is to create a detailed budget breakdown for the trip.
    Use the calculate_budget_breakdown tool to allocate the budget across different categories.
    Provide recommendations for cost-saving opportunities."""
    
    response = get_llm().invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])
    
    return {
        **state,
        "messages": [response]
    }

@observe(name="itinerary_agent")
def itinerary_agent(state: TripPlanningState) -> TripPlanningState:
    """Agent responsible for creating the detailed itinerary."""
    messages = state["messages"]
    
    system_prompt = """You are an itinerary planning specialist. Your job is to create a detailed day-by-day itinerary.
    Use the generate_itinerary tool to create a comprehensive schedule.
    Consider the user's interests, budget, and duration to create an optimal plan."""
    
    response = get_llm().invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])
    
    return {
        **state,
        "messages": [response]
    }

@observe(name="accommodation_agent")
def accommodation_agent(state: TripPlanningState) -> TripPlanningState:
    """Agent responsible for finding suitable accommodations."""
    messages = state["messages"]
    
    system_prompt = """You are an accommodation specialist. Your job is to find suitable places to stay.
    Use the find_accommodations tool to get accommodation options within the budget.
    Consider location, amenities, and value for money."""
    
    response = get_llm().invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])
    
    return {
        **state,
        "messages": [response]
    }

@observe(name="coordinator_agent")
def coordinator_agent(state: TripPlanningState) -> TripPlanningState:
    """Coordinator agent that synthesizes all information into a final plan."""
    messages = state["messages"]
    
    # Get the key parameters from the state
    destination = state.get("destination", "Unknown")
    duration = state.get("duration", 0)
    budget = state.get("budget", 0)
    interests = state.get("interests", [])
    
    system_prompt = f"""You are the trip planning coordinator. Your job is to synthesize all the research and recommendations
    into a comprehensive, actionable trip plan for {destination}.
    
    Trip Details:
    - Destination: {destination}
    - Duration: {duration} days
    - Budget: ${budget}
    - Interests: {', '.join(interests) if interests else 'General travel'}
    
    Create a final summary that includes:
    1. Destination overview for {destination}
    2. Budget breakdown for ${budget}
    3. Detailed {duration}-day itinerary for {destination}
    4. Accommodation recommendations in {destination}
    5. Practical tips and reminders for {destination}
    
    Make sure the plan is realistic, within budget, and matches the user's interests. Focus specifically on {destination}."""
    
    response = get_llm().invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])
    
    return {
        **state,
        "messages": [response],
        "final_plan": {"summary": response.content}
    }

def should_continue(state: TripPlanningState) -> str:
    """Determine the next step in the workflow."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Simple routing logic - in a real implementation, this would be more sophisticated
    if "research" in last_message.content.lower():
        return "research"
    elif "budget" in last_message.content.lower():
        return "budget"
    elif "itinerary" in last_message.content.lower():
        return "itinerary"
    elif "accommodation" in last_message.content.lower():
        return "accommodation"
    else:
        return "coordinator"

# Create the workflow graph
def create_trip_planner_graph():
    """Create the LangGraph workflow for trip planning."""
    
    workflow = StateGraph(TripPlanningState)
    
    # Add nodes
    workflow.add_node("research_agent", research_agent)
    workflow.add_node("budget_agent", budget_agent)
    workflow.add_node("itinerary_agent", itinerary_agent)
    workflow.add_node("accommodation_agent", accommodation_agent)
    workflow.add_node("coordinator_agent", coordinator_agent)
    
    # Add edges - create a sequential flow
    workflow.add_edge("research_agent", "budget_agent")
    workflow.add_edge("budget_agent", "itinerary_agent")
    workflow.add_edge("itinerary_agent", "accommodation_agent")
    workflow.add_edge("accommodation_agent", "coordinator_agent")
    workflow.add_edge("coordinator_agent", END)
    
    # Set entry point
    workflow.set_entry_point("research_agent")
    
    return workflow.compile()

# Initialize the graph lazily to avoid hanging on import
trip_planner_graph = None

def get_trip_planner_graph():
    global trip_planner_graph
    if trip_planner_graph is None:
        trip_planner_graph = create_trip_planner_graph()
    return trip_planner_graph

@observe(name="plan_trip")
def plan_trip(trip_request: TripRequest) -> Dict[str, Any]:
    """Main function to plan a trip using the LangGraph workflow."""
    
    # Start timing for performance tracking
    start_time = time.time()
    workflow_id = str(uuid.uuid4())
    
    try:
        # Use the actual LangGraph workflow with OpenAI API calls
        graph = get_trip_planner_graph()
        
        # Create initial state for the workflow
        initial_state = {
            "messages": [],
            "destination": trip_request.destination,
            "duration": trip_request.duration,
            "budget": trip_request.budget,
            "interests": trip_request.interests,
            "start_date": trip_request.start_date,
            "end_date": trip_request.end_date,
            "accommodation_type": trip_request.accommodation_type,
            "transportation_type": trip_request.transportation_type,
        }
        
        # Execute the workflow
        final_state = graph.invoke(initial_state)
        
        # Extract the result from the final state
        final_plan_data = final_state.get("final_plan", {})
        result = {
            "final_plan": {
                "summary": final_plan_data.get("summary", "Trip plan generated successfully") if isinstance(final_plan_data, dict) else str(final_plan_data),
                "destination": final_state.get("destination", trip_request.destination),
                "duration": final_state.get("duration", trip_request.duration),
                "budget": final_state.get("budget", trip_request.budget),
                "interests": final_state.get("interests", trip_request.interests),
                "itinerary": final_state.get("itinerary", []),
                "accommodation": final_state.get("accommodation", {}),
                "transportation": final_state.get("transportation", {}),
                "budget_breakdown": final_state.get("budget_breakdown", {}),
                "recommendations": final_state.get("recommendations", []),
                "tips": final_state.get("tips", "")
            },
            "messages": [
                f"Research completed for {trip_request.destination}",
                f"Budget analysis completed for ${trip_request.budget}",
                f"Itinerary created for {trip_request.duration} days",
                f"Accommodation recommendations for {trip_request.accommodation_type}",
                "Trip plan coordination completed"
            ],
            "destination": trip_request.destination,
            "duration": trip_request.duration,
            "budget": trip_request.budget,
            "interests": trip_request.interests,
            "workflow_id": workflow_id
        }
        
        # Calculate execution time
        execution_time_ms = (time.time() - start_time) * 1000
        print(f"✅ Trip planning completed in {execution_time_ms:.2f}ms")
        
        return result
        
    except Exception as e:
        # Calculate execution time for error case
        execution_time_ms = (time.time() - start_time) * 1000
        print(f"❌ Trip planning failed after {execution_time_ms:.2f}ms: {str(e)}")
        
        # Re-raise the exception
        raise e

if __name__ == "__main__":
    # Example usage
    sample_request = TripRequest(
        destination="Paris",
        duration=5,
        budget=2000.0,
        interests=["art", "food", "history"],
        start_date="2024-06-01",
        end_date="2024-06-05",
        accommodation_type="hotel",
        transportation_type="flight"
    )
    
    result = plan_trip(sample_request)
    print(json.dumps(result, indent=2))
