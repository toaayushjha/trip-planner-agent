# API Documentation

Complete API reference for the Trip Planner Agent backend.

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required for the current implementation.

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running and healthy.

#### Response
```json
{
  "status": "healthy",
  "service": "trip-planner-agent"
}
```

#### Example
```bash
curl http://localhost:8000/health
```

---

### 2. Root Endpoint

**GET** `/`

Get basic API information.

#### Response
```json
{
  "message": "Trip Planner Agent API is running!"
}
```

---

### 3. Plan Trip

**POST** `/plan-trip`

Create a comprehensive trip plan using AI agents.

#### Request Body
```json
{
  "destination": "string",
  "duration": "integer",
  "budget": "number",
  "interests": ["string"],
  "start_date": "string",
  "end_date": "string",
  "accommodation_type": "string",
  "transportation_type": "string"
}
```

#### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `destination` | string | Yes | Destination city or country |
| `duration` | integer | Yes | Trip duration in days |
| `budget` | number | Yes | Total budget in USD |
| `interests` | array | No | List of interests (e.g., ["culture", "food"]) |
| `start_date` | string | Yes | Start date in YYYY-MM-DD format |
| `end_date` | string | Yes | End date in YYYY-MM-DD format |
| `accommodation_type` | string | No | Type of accommodation (default: "hotel") |
| `transportation_type` | string | No | Transportation method (default: "flight") |

#### Response
```json
{
  "success": true,
  "data": {
    "final_plan": {
      "summary": "string",
      "destination": "string",
      "duration": "integer",
      "budget": "number",
      "interests": ["string"],
      "itinerary": "object",
      "accommodation": "object",
      "transportation": "object",
      "budget_breakdown": "object",
      "recommendations": "object",
      "tips": "string"
    },
    "messages": ["string"],
    "destination": "string",
    "duration": "integer",
    "budget": "number",
    "workflow_id": "string"
  },
  "error": null
}
```

#### Example Request
```bash
curl -X POST "http://localhost:8000/plan-trip" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "duration": 3,
    "budget": 1500,
    "interests": ["culture", "food"],
    "start_date": "2024-02-01",
    "end_date": "2024-02-04"
  }'
```

#### Example Response
```json
{
  "success": true,
  "data": {
    "final_plan": {
      "summary": "Here are some practical tips and reminders for your trip to Paris...",
      "destination": "Paris",
      "duration": 3,
      "budget": 1500.0,
      "interests": ["culture", "food"],
      "itinerary": null,
      "accommodation": {},
      "transportation": {},
      "budget_breakdown": {},
      "recommendations": null,
      "tips": ""
    },
    "messages": [
      "Research completed for Paris",
      "Budget analysis completed for $1500.0",
      "Itinerary created for 3 days",
      "Accommodation recommendations for hotel",
      "Trip plan coordination completed"
    ],
    "destination": "Paris",
    "duration": 3,
    "budget": 1500.0,
    "workflow_id": "2e4668e9-7b20-449e-b6be-644ca08e290d"
  },
  "error": null
}
```

---

### 4. Get Destinations

**GET** `/destinations`

Get a list of popular travel destinations.

#### Response
```json
{
  "destinations": [
    {
      "name": "string",
      "country": "string",
      "currency": "string"
    }
  ]
}
```

#### Example
```bash
curl http://localhost:8000/destinations
```

#### Example Response
```json
{
  "destinations": [
    {
      "name": "Paris",
      "country": "France",
      "currency": "EUR"
    },
    {
      "name": "Tokyo",
      "country": "Japan",
      "currency": "JPY"
    }
  ]
}
```

---

### 5. Get Interests

**GET** `/interests`

Get a list of common travel interests.

#### Response
```json
{
  "interests": ["string"]
}
```

#### Example
```bash
curl http://localhost:8000/interests
```

#### Example Response
```json
{
  "interests": [
    "art",
    "history",
    "food",
    "nature",
    "adventure",
    "culture",
    "shopping",
    "nightlife",
    "beaches",
    "mountains"
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "data": null,
  "error": "Invalid request parameters"
}
```

### 422 Unprocessable Entity
```json
{
  "success": false,
  "data": null,
  "error": "Validation error: Field 'destination' is required"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "data": null,
  "error": "OpenAI API key not configured"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. Consider implementing rate limiting for production deployments.

## CORS

The API includes CORS middleware allowing requests from any origin. For production, configure specific allowed origins.

## Observability

All API calls are automatically monitored and traced using:
- **Langfuse**: LLM call monitoring and workflow tracking
- **Prompt Management**: Version control and optimization
- **OpenInference**: AI-specific instrumentation

## Interactive Documentation

When the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## SDK Examples

### Python
```python
import requests

# Plan a trip
response = requests.post(
    "http://localhost:8000/plan-trip",
    json={
        "destination": "Paris",
        "duration": 3,
        "budget": 1500,
        "interests": ["culture", "food"],
        "start_date": "2024-02-01",
        "end_date": "2024-02-04"
    }
)

trip_plan = response.json()
print(trip_plan["data"]["final_plan"]["summary"])
```

### JavaScript
```javascript
// Plan a trip
const response = await fetch('http://localhost:8000/plan-trip', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    destination: 'Paris',
    duration: 3,
    budget: 1500,
    interests: ['culture', 'food'],
    start_date: '2024-02-01',
    end_date: '2024-02-04'
  })
});

const tripPlan = await response.json();
console.log(tripPlan.data.final_plan.summary);
```

### cURL
```bash
# Plan a trip
curl -X POST "http://localhost:8000/plan-trip" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "duration": 3,
    "budget": 1500,
    "interests": ["culture", "food"],
    "start_date": "2024-02-01",
    "end_date": "2024-02-04"
  }'

# Get destinations
curl http://localhost:8000/destinations

# Get interests
curl http://localhost:8000/interests

# Health check
curl http://localhost:8000/health
```

## Testing

### Manual Testing
Use the interactive documentation at `http://localhost:8000/docs` to test all endpoints.

### Automated Testing
```bash
# Run backend tests
cd backend
python -m pytest

# Test specific endpoint
curl -X POST "http://localhost:8000/plan-trip" \
  -H "Content-Type: application/json" \
  -d '{"destination": "Tokyo", "duration": 5, "budget": 2000, "interests": ["culture"], "start_date": "2024-03-01", "end_date": "2024-03-06"}'
```

## Production Considerations

1. **Authentication**: Implement proper authentication and authorization
2. **Rate Limiting**: Add rate limiting to prevent abuse
3. **Input Validation**: Enhanced input validation and sanitization
4. **Error Handling**: Comprehensive error handling and logging
5. **Monitoring**: Set up alerts and monitoring for production
6. **Caching**: Implement caching for frequently requested data
7. **Load Balancing**: Use load balancers for high availability
8. **Security**: Implement security headers and HTTPS




