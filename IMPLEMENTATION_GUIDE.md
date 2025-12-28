# Trip Planner Agent - LLM Implementation Guide

## 🎯 Overview
This guide provides step-by-step instructions for an LLM to recreate the complete Trip Planner Agent application with observability.

## 📋 Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key
- Langfuse account (free tier)

## 🚀 Step-by-Step Implementation

### Step 1: Project Setup
```bash
mkdir trip-planner-agent
cd trip-planner-agent
python -m venv venv
source venv/bin/activate
mkdir backend frontend
```

### Step 2: Backend Dependencies
Create `requirements.txt`:
```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
langgraph==0.0.62
langchain-openai>=0.1.0
langchain-community>=0.0.10
langfuse>=3.3.0
openinference-instrumentation-openai>=1.0.0
opentelemetry-api>=1.20.0
opentelemetry-sdk>=1.20.0
opentelemetry-exporter-otlp>=1.20.0
```

### Step 3: Environment Configuration
Create `env.example`:
```env
OPENAI_API_KEY=your_openai_api_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Step 4: Backend Implementation

#### 4.1 Main FastAPI Application (`backend/main.py`)
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenInference setup (must be first)
try:
    from openinference_config import openinference_config
    if openinference_config.setup_instrumentation():
        print("✅ OpenInference instrumentation setup completed successfully")
    else:
        print("⚠️  OpenInference instrumentation setup failed")
except ImportError as e:
    print(f"⚠️  OpenInference packages not available: {e}")
except Exception as e:
    print(f"❌ Failed to setup OpenInference instrumentation: {e}")

from trip_planner_agent import plan_trip, TripRequest

app = FastAPI(title="Trip Planner Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripPlanRequest(BaseModel):
    destination: str
    duration: int
    budget: float
    interests: List[str] = []
    start_date: str
    end_date: str
    accommodation_type: str = "hotel"
    transportation_type: str = "flight"

class TripPlanResponse(BaseModel):
    success: bool
    data: Dict[str, Any] = None
    error: str = None

@app.get("/")
async def root():
    return {"message": "Trip Planner Agent API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "trip-planner-agent"}

@app.post("/plan-trip", response_model=TripPlanResponse)
async def create_trip_plan(request: TripPlanRequest):
    try:
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        trip_request = TripRequest(
            destination=request.destination,
            duration=request.duration,
            budget=request.budget,
            interests=request.interests,
            start_date=request.start_date,
            end_date=request.end_date,
            accommodation_type=request.accommodation_type,
            transportation_type=request.transportation_type
        )
        
        result = plan_trip(trip_request)
        
        return TripPlanResponse(success=True, data=result)
        
    except Exception as e:
        return TripPlanResponse(success=False, error=str(e))

@app.get("/destinations")
async def get_popular_destinations():
    destinations = [
        {"name": "Paris", "country": "France", "currency": "EUR"},
        {"name": "Tokyo", "country": "Japan", "currency": "JPY"},
        {"name": "New York", "country": "USA", "currency": "USD"},
        {"name": "London", "country": "UK", "currency": "GBP"},
        {"name": "Rome", "country": "Italy", "currency": "EUR"}
    ]
    return {"destinations": destinations}

@app.get("/interests")
async def get_common_interests():
    interests = [
        "art", "history", "food", "nature", "adventure", "culture",
        "shopping", "nightlife", "beaches", "mountains", "museums"
    ]
    return {"interests": interests}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

#### 4.2 Trip Planner Agent (`backend/trip_planner_agent.py`)
```python
import os
import time
import uuid
from typing import Dict, List, Any, TypedDict, Annotated
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from pydantic import BaseModel, Field
# Langfuse integration is handled automatically via callbacks

llm = None

def get_llm():
    global llm
    if llm is None:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    return llm

class TripPlanningState(TypedDict):
    messages: Annotated[list, add_messages]
    destination: str
    duration: int
    budget: float
    interests: List[str]
    start_date: str
    end_date: str
    accommodation_type: str
    transportation_type: str
    research_data: Dict[str, Any]
    budget_analysis: Dict[str, Any]
    itinerary: Dict[str, Any]
    accommodation: Dict[str, Any]
    final_plan: Dict[str, Any]

class TripRequest(BaseModel):
    destination: str
    duration: int
    budget: float
    interests: List[str]
    start_date: str
    end_date: str
    accommodation_type: str = "hotel"
    transportation_type: str = "flight"

def research_agent(state: TripPlanningState) -> TripPlanningState:
    destination = state["destination"]
    interests = state["interests"]
    
    system_prompt = f"""You are a travel research expert. Research {destination} focusing on: {', '.join(interests)}.
    Provide comprehensive information about attractions, culture, best times to visit, and local insights."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Research {destination} for a {state['duration']}-day trip")
    ]
    
    llm = get_llm()
    response = llm.invoke(messages)
    
    state["research_data"] = {
        "destination": destination,
        "research": response.content,
        "timestamp": datetime.now().isoformat()
    }
    
    state["messages"].append(AIMessage(content=f"Research completed for {destination}"))
    return state

def budget_agent(state: TripPlanningState) -> TripPlanningState:
    destination = state["destination"]
    budget = state["budget"]
    duration = state["duration"]
    
    system_prompt = f"""You are a travel budget expert. Create a detailed budget breakdown for {destination} 
    with a total budget of ${budget} for {duration} days. Include accommodation, food, transportation, activities, and miscellaneous costs."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Create budget breakdown for {destination}, ${budget} for {duration} days")
    ]
    
    llm = get_llm()
    response = llm.invoke(messages)
    
    state["budget_analysis"] = {
        "total_budget": budget,
        "duration": duration,
        "breakdown": response.content,
        "timestamp": datetime.now().isoformat()
    }
    
    state["messages"].append(AIMessage(content=f"Budget analysis completed for ${budget}"))
    return state

def itinerary_agent(state: TripPlanningState) -> TripPlanningState:
    destination = state["destination"]
    duration = state["duration"]
    interests = state["interests"]
    
    system_prompt = f"""You are a travel itinerary expert. Create a detailed day-by-day itinerary for {destination} 
    for {duration} days focusing on: {', '.join(interests)}. Include specific attractions, restaurants, and activities."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Create {duration}-day itinerary for {destination}")
    ]
    
    llm = get_llm()
    response = llm.invoke(messages)
    
    state["itinerary"] = {
        "destination": destination,
        "duration": duration,
        "schedule": response.content,
        "timestamp": datetime.now().isoformat()
    }
    
    state["messages"].append(AIMessage(content=f"Itinerary created for {duration} days"))
    return state

def accommodation_agent(state: TripPlanningState) -> TripPlanningState:
    destination = state["destination"]
    accommodation_type = state["accommodation_type"]
    budget = state["budget"]
    
    system_prompt = f"""You are a travel accommodation expert. Recommend {accommodation_type} options 
    in {destination} that fit within a budget of ${budget}. Include specific recommendations with details."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Find {accommodation_type} options in {destination} for ${budget} budget")
    ]
    
    llm = get_llm()
    response = llm.invoke(messages)
    
    state["accommodation"] = {
        "destination": destination,
        "type": accommodation_type,
        "recommendations": response.content,
        "timestamp": datetime.now().isoformat()
    }
    
    state["messages"].append(AIMessage(content=f"Accommodation recommendations for {accommodation_type}"))
    return state

def coordinator_agent(state: TripPlanningState) -> TripPlanningState:
    destination = state["destination"]
    duration = state["duration"]
    budget = state["budget"]
    interests = state["interests"]
    
    system_prompt = f"""You are a travel coordinator. Synthesize all the research, budget, itinerary, and accommodation 
    information into a comprehensive trip plan for {destination}. Create a final summary that includes practical tips and reminders."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Create final trip plan for {destination}, {duration} days, ${budget} budget, interests: {', '.join(interests)}")
    ]
    
    llm = get_llm()
    response = llm.invoke(messages)
    
    state["final_plan"] = {
        "summary": response.content,
        "destination": destination,
        "duration": duration,
        "budget": budget,
        "interests": interests,
        "itinerary": state.get("itinerary", {}),
        "accommodation": state.get("accommodation", {}),
        "budget_breakdown": state.get("budget_analysis", {}),
        "recommendations": None,
        "tips": ""
    }
    
    state["messages"].append(AIMessage(content="Trip plan coordination completed"))
    return state

def create_workflow():
    workflow = StateGraph(TripPlanningState)
    
    workflow.add_node("research", research_agent)
    workflow.add_node("budget", budget_agent)
    workflow.add_node("itinerary", itinerary_agent)
    workflow.add_node("accommodation", accommodation_agent)
    workflow.add_node("coordinator", coordinator_agent)
    
    workflow.set_entry_point("research")
    workflow.add_edge("research", "budget")
    workflow.add_edge("budget", "itinerary")
    workflow.add_edge("itinerary", "accommodation")
    workflow.add_edge("accommodation", "coordinator")
    workflow.add_edge("coordinator", END)
    
    return workflow.compile()

def plan_trip(request: TripRequest) -> Dict[str, Any]:
    workflow_id = str(uuid.uuid4())
    
    try:
        # Log workflow start
        # Langfuse automatically tracks workflow execution
            workflow_id=workflow_id,
            workflow_name="trip_planning",
            status="started",
            input_data={
                "destination": request.destination,
                "duration": request.duration,
                "budget": request.budget,
                "interests": request.interests
            }
        )
        
        workflow = create_workflow()
        
        initial_state = {
            "messages": [],
            "destination": request.destination,
            "duration": request.duration,
            "budget": request.budget,
            "interests": request.interests,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "accommodation_type": request.accommodation_type,
            "transportation_type": request.transportation_type,
            "research_data": {},
            "budget_analysis": {},
            "itinerary": {},
            "accommodation": {},
            "final_plan": {}
        }
        
        result = workflow.invoke(initial_state)
        
        # Log workflow completion
        # Langfuse automatically tracks workflow execution
            workflow_id=workflow_id,
            workflow_name="trip_planning",
            status="completed",
            output_data=result["final_plan"]
        )
        
        return {
            "final_plan": result["final_plan"],
            "messages": [msg.content for msg in result["messages"] if hasattr(msg, 'content')],
            "destination": result["destination"],
            "duration": result["duration"],
            "budget": result["budget"],
            "workflow_id": workflow_id
        }
        
    except Exception as e:
        # Log workflow error
        # Langfuse automatically tracks workflow execution
            workflow_id=workflow_id,
            workflow_name="trip_planning",
            status="error",
            error_message=str(e)
        )
        raise e
```

#### 4.3 Arize Configuration (`backend/arize_config.py`)
```python
import os
import logging
from arize.api import Client
from arize.api.models import ModelTypes, Environments

logger = logging.getLogger(__name__)

class ArizeConfig:
    def __init__(self):
        self.api_key = os.getenv("ARIZE_API_KEY")
        self.space_key = os.getenv("ARIZE_SPACE_ID") or os.getenv("ARIZE_SPACE_KEY")
        self.model_id = os.getenv("ARIZE_MODEL_ID", "trip-planner-agent")
        self.model_version = os.getenv("ARIZE_MODEL_VERSION", "1.0.0")
        
        if not self.api_key or not self.space_key:
            logger.warning("Arize credentials not found. Observability disabled.")
            self.client = None
        else:
            self.client = Client(
                api_key=self.api_key,
                space_id=self.space_key
            )
            logger.info("Arize AI client initialized successfully")
    
    def log_llm_prediction(self, prediction_id: str, input_text: str, output_text: str, 
                          model_name: str, latency_ms: float, token_usage: dict):
        if not self.client:
            return
        
        try:
            future = self.client.log(
                model_id=self.model_id,
                model_version=self.model_version,
                model_type=ModelTypes.GENERATIVE_LLM,
                environment=Environments.PRODUCTION,
                prediction_id=prediction_id,
                prediction_label=output_text[:100],
                features={"input_text": input_text},
                metadata={
                    "model_name": model_name,
                    "latency_ms": latency_ms,
                    "token_usage": token_usage,
                    "output_length": len(output_text)
                }
            )
            result = future.result(timeout=10)
            logger.info(f"Successfully logged prediction {prediction_id} to Arize")
        except Exception as e:
            logger.error(f"Failed to log prediction to Arize: {e}")
    
    def log_agent_workflow(self, workflow_id: str, workflow_name: str, status: str, 
                          input_data: dict = None, output_data: dict = None, error_message: str = None):
        if not self.client:
            return
        
        try:
            metadata = {
                "workflow_name": workflow_name,
                "status": status,
                "input_data": input_data or {},
                "output_data": output_data or {},
                "error_message": error_message
            }
            
            future = self.client.log(
                model_id=self.model_id,
                model_version=self.model_version,
                model_type=ModelTypes.SCORE_CATEGORICAL,
                environment=Environments.PRODUCTION,
                prediction_id=workflow_id,
                prediction_label=status,
                features={"workflow_name": workflow_name},
                metadata=metadata
            )
            result = future.result(timeout=10)
            logger.info(f"Successfully logged workflow {workflow_id} to Arize")
        except Exception as e:
            logger.error(f"Failed to log workflow to Arize: {e}")

arize_config = ArizeConfig()
```

#### 4.4 Arize Callback (`backend/arize_callback.py`)
```python
import uuid
import time
import logging
from typing import Any, Dict, List, Optional
from langchain_core.callbacks.base import BaseCallbackHandler
# Langfuse integration is handled automatically via callbacks

logger = logging.getLogger(__name__)

class ArizeCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        self.prediction_id = str(uuid.uuid4())
        self.start_time = time.time()
        self.input_text = prompts[0] if prompts else ""
        logger.info(f"LLM started with prediction ID: {self.prediction_id}")
    
    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        if hasattr(self, 'prediction_id'):
            end_time = time.time()
            latency_ms = (end_time - self.start_time) * 1000
            
            output_text = response.generations[0][0].text if hasattr(response, 'generations') else str(response)
            
            token_usage = {
                "prompt_tokens": getattr(response.llm_output, 'token_usage', {}).get('prompt_tokens', 0),
                "completion_tokens": getattr(response.llm_output, 'token_usage', {}).get('completion_tokens', 0),
                "total_tokens": getattr(response.llm_output, 'token_usage', {}).get('total_tokens', 0)
            }
            
            arize_config.log_llm_prediction(
                prediction_id=self.prediction_id,
                input_text=self.input_text,
                output_text=output_text,
                model_name="gpt-3.5-turbo",
                latency_ms=latency_ms,
                token_usage=token_usage
            )
            
            logger.info(f"LLM completed with prediction ID: {self.prediction_id}, latency: {latency_ms:.2f}ms")
```

#### 4.5 OpenInference Configuration (`backend/openinference_config.py`)
```python
import os
import logging
from typing import Optional, Dict, Any
from opentelemetry import trace

# OpenInference instrumentation
try:
    from openinference.instrumentation.langchain import LangChainInstrumentor
    from openinference.instrumentation.openai import OpenAIInstrumentor
    OPENINFERENCE_AVAILABLE = True
except ImportError:
    OPENINFERENCE_AVAILABLE = False
    LangChainInstrumentor = None
    OpenAIInstrumentor = None

# Arize OTel
try:
    from arize.otel import register
    ARIZE_OTEL_AVAILABLE = True
except ImportError:
    ARIZE_OTEL_AVAILABLE = False

logger = logging.getLogger(__name__)

class OpenInferenceConfig:
    def __init__(self):
        self.langchain_instrumentor = None
        self.openai_instrumentor = None
        self.tracer_provider = None
        self.is_configured = False
        
    def setup_instrumentation(self) -> bool:
        try:
            arize_api_key = os.getenv("ARIZE_API_KEY")
            arize_space_id = os.getenv("ARIZE_SPACE_ID") or os.getenv("ARIZE_SPACE_KEY")
            
            if not arize_api_key or not arize_space_id:
                logger.warning("Arize credentials not found. OpenInference instrumentation disabled.")
                return False
            
            # Register Arize OTel
            if ARIZE_OTEL_AVAILABLE:
                try:
                    self.tracer_provider = register(
                        space_id=arize_space_id,
                        api_key=arize_api_key,
                        project_name="trip-planner-agent",
                    )
                    logger.info("✅ Arize OTel tracing registered successfully")
                except Exception as e:
                    logger.error(f"Failed to register Arize OTel: {e}")
                    return False
            
            # Initialize instrumentors
            if OPENINFERENCE_AVAILABLE and LangChainInstrumentor:
                self.langchain_instrumentor = LangChainInstrumentor()
                self.langchain_instrumentor.instrument()
                logger.info("✅ LangChain instrumentation enabled")
            
            if OPENINFERENCE_AVAILABLE and OpenAIInstrumentor:
                self.openai_instrumentor = OpenAIInstrumentor()
                self.openai_instrumentor.instrument()
                logger.info("✅ OpenAI instrumentation enabled")
            
            self.is_configured = True
            logger.info("✅ OpenInference instrumentation setup completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup OpenInference instrumentation: {e}")
            return False

openinference_config = OpenInferenceConfig()
```

#### 4.6 Arize Debug (`backend/arize_debug.py`)
```python
import os
import sys
from arize.api import Client
from arize.api.models import ModelTypes, Environments

class ArizeDebugger:
    def __init__(self):
        self.arize_api_key = os.getenv("ARIZE_API_KEY")
        self.arize_space_id = os.getenv("ARIZE_SPACE_ID") or os.getenv("ARIZE_SPACE_KEY")
        self.model_id = os.getenv("ARIZE_MODEL_ID", "trip-planner-agent")
        self.model_version = os.getenv("ARIZE_MODEL_VERSION", "1.0.0")
    
    def print_debug_info(self):
        print("=" * 60)
        print("🔍 ARIZE DEBUG INFORMATION")
        print("=" * 60)
        print(f"📋 CREDENTIALS STATUS:")
        print(f"   API Key: {'✅ Set' if self.arize_api_key else '❌ Missing'}")
        print(f"   Space Key: {'✅ Set' if self.arize_space_id else '❌ Missing'}")
        print(f"   Model ID: {self.model_id}")
        print(f"   Model Version: {self.model_version}")
        print(f"🔧 CONFIGURATION VALIDATION:")
        print(f"   {'✅ All required credentials are present' if self.arize_api_key and self.arize_space_id else '❌ Missing credentials'}")
        print(f"🌍 ENVIRONMENT INFO:")
        print(f"   Python Version: {sys.version}")
        print(f"   Working Directory: {os.getcwd()}")
        print(f"   Environment File: {'✅ .env exists' if os.path.exists('.env') else '❌ .env missing'}")
        print("=" * 60)
    
    def test_arize_connection(self):
        if not self.arize_api_key or not self.arize_space_id:
            print("❌ Missing Arize credentials")
            return False
        
        try:
            client = Client(space_id=self.arize_space_id, api_key=self.arize_api_key)
            future = client.log(
                model_id=self.model_id,
                model_version=self.model_version,
                model_type=ModelTypes.SCORE_CATEGORICAL,
                environment=Environments.PRODUCTION,
                prediction_id='test-connection',
                prediction_label='test',
                features={'test': 'connection'}
            )
            result = future.result(timeout=10)
            print("✅ Arize connection test successful!")
            return True
        except Exception as e:
            print(f"❌ Arize connection test failed: {e}")
            return False

arize_debugger = ArizeDebugger()
```

### Step 5: Frontend Implementation

#### 5.1 Initialize React App
```bash
cd frontend
npx create-react-app . --template typescript
npm install axios
```

#### 5.2 Create API Service (`frontend/src/services/api.js`)
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = {
  async planTrip(tripData) {
    const response = await fetch(`${API_BASE_URL}/plan-trip`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(tripData),
    });
    return response.json();
  },
  
  async getDestinations() {
    const response = await fetch(`${API_BASE_URL}/destinations`);
    return response.json();
  },
  
  async getInterests() {
    const response = await fetch(`${API_BASE_URL}/interests`);
    return response.json();
  }
};
```

#### 5.3 Create Trip Planning Form (`frontend/src/components/TripPlanningForm.js`)
```javascript
import React, { useState } from 'react';
import { api } from '../services/api';

const TripPlanningForm = ({ onTripPlanned }) => {
  const [formData, setFormData] = useState({
    destination: '',
    duration: 3,
    budget: 1000,
    interests: [],
    start_date: '',
    end_date: '',
    accommodation_type: 'hotel',
    transportation_type: 'flight'
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.planTrip(formData);
      if (result.success) {
        onTripPlanned(result.data);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to plan trip. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">Destination</label>
        <input
          type="text"
          value={formData.destination}
          onChange={(e) => setFormData({...formData, destination: e.target.value})}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          required
        />
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Duration (days)</label>
          <input
            type="number"
            value={formData.duration}
            onChange={(e) => setFormData({...formData, duration: parseInt(e.target.value)})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            min="1"
            max="30"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Budget ($)</label>
          <input
            type="number"
            value={formData.budget}
            onChange={(e) => setFormData({...formData, budget: parseFloat(e.target.value)})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            min="100"
            required
          />
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Start Date</label>
          <input
            type="date"
            value={formData.start_date}
            onChange={(e) => setFormData({...formData, start_date: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">End Date</label>
          <input
            type="date"
            value={formData.end_date}
            onChange={(e) => setFormData({...formData, end_date: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            required
          />
        </div>
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700">Interests</label>
        <input
          type="text"
          placeholder="e.g., culture, food, nature"
          value={formData.interests.join(', ')}
          onChange={(e) => setFormData({...formData, interests: e.target.value.split(',').map(s => s.trim())})}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
        />
      </div>
      
      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}
      
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Planning Your Trip...' : 'Plan My Trip'}
      </button>
    </form>
  );
};

export default TripPlanningForm;
```

#### 5.4 Create Trip Results (`frontend/src/components/TripResults.js`)
```javascript
import React from 'react';

const TripResults = ({ tripData }) => {
  if (!tripData) return null;
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Trip Plan</h2>
      
      <div className="space-y-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">Summary</h3>
          <p className="text-gray-600 whitespace-pre-wrap">
            {typeof tripData.final_plan?.summary === 'string' 
              ? tripData.final_plan.summary 
              : JSON.stringify(tripData.final_plan?.summary)}
          </p>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <h4 className="font-semibold text-gray-800">Destination</h4>
            <p className="text-gray-600">{tripData.destination}</p>
          </div>
          <div>
            <h4 className="font-semibold text-gray-800">Duration</h4>
            <p className="text-gray-600">{tripData.duration} days</p>
          </div>
          <div>
            <h4 className="font-semibold text-gray-800">Budget</h4>
            <p className="text-gray-600">${tripData.budget}</p>
          </div>
          <div>
            <h4 className="font-semibold text-gray-800">Interests</h4>
            <p className="text-gray-600">{tripData.interests?.join(', ')}</p>
          </div>
        </div>
        
        <div>
          <h3 className="text-lg font-semibold text-gray-800">Workflow Status</h3>
          <ul className="list-disc list-inside text-gray-600">
            {tripData.messages?.map((message, index) => (
              <li key={index}>{message}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TripResults;
```

#### 5.5 Create Main App (`frontend/src/App.js`)
```javascript
import React, { useState } from 'react';
import TripPlanningForm from './components/TripPlanningForm';
import TripResults from './components/TripResults';
import './App.css';

function App() {
  const [tripData, setTripData] = useState(null);
  
  const handleTripPlanned = (data) => {
    setTripData(data);
  };
  
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-gray-900 mb-8">
          Trip Planner Agent
        </h1>
        
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Plan Your Perfect Trip
            </h2>
            <TripPlanningForm onTripPlanned={handleTripPlanned} />
          </div>
          
          {tripData && <TripResults tripData={tripData} />}
        </div>
      </div>
    </div>
  );
}

export default App;
```

### Step 6: Testing and Verification

#### 6.1 Install Dependencies
```bash
# Backend
cd backend
pip install -r ../requirements.txt

# Frontend
cd ../frontend
npm install
```

#### 6.2 Configure Environment
```bash
# Copy environment template
cp env.example .env
# Edit .env with actual API keys
```

#### 6.3 Test Backend
```bash
cd backend
python main.py
```

#### 6.4 Test Frontend
```bash
cd frontend
npm start
```

#### 6.5 Verify Observability
1. Check Arize dashboard for incoming data
2. Verify logs show successful Arize integration
3. Test API endpoints for proper responses

## ✅ Success Criteria

- [ ] Backend starts without errors
- [ ] Frontend loads and displays form
- [ ] Trip planning workflow completes successfully
- [ ] Arize dashboard shows incoming data
- [ ] All API endpoints respond correctly
- [ ] Error handling works properly

## 🚨 Troubleshooting

### Common Issues
1. **Import Errors**: Check all dependencies are installed
2. **API Key Errors**: Verify environment variables are set
3. **Arize Connection**: Check credentials and network connectivity
4. **Frontend Errors**: Ensure backend is running and CORS is configured

### Debug Commands
```bash
# Test Arize connection
python -c "from backend.arize_debug import arize_debugger; arize_debugger.test_arize_connection()"

# Check environment
python -c "from backend.arize_debug import arize_debugger; arize_debugger.print_debug_info()"

# Test API
curl http://localhost:8000/health
```

This implementation guide provides everything needed to recreate the complete Trip Planner Agent application with full observability capabilities.




