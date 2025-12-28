# Quick Start Guide

Get the Trip Planner Agent up and running in minutes with full observability.

## 🚀 5-Minute Setup

### 1. Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key
- Langfuse account (free)

### 2. Clone and Install
```bash
# Clone the repository
git clone <repository-url>
cd trip-planner-agent

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Get API Keys

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key

#### Langfuse Credentials
1. Sign up at [Langfuse](https://cloud.langfuse.com/) (free tier)
2. Create a new project
3. Get your API keys from the project settings

### 4. Configure Environment
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your keys
nano .env  # or use your preferred editor
```

Add your keys to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 5. Start the Application

#### Backend (Terminal 1)
```bash
# From project root
source venv/bin/activate
python backend/main.py
```

#### Frontend (Terminal 2)
```bash
# From project root
cd frontend
npm install
npm start
```

### 6. Test the Application
1. Open [http://localhost:3000](http://localhost:3000)
2. Fill out the trip planning form
3. Click "Plan My Trip"
4. View your personalized trip plan!

## ✅ Verify Everything Works

### Check Backend Health
```bash
curl http://localhost:8000/health
```
Expected: `{"status": "healthy", "service": "trip-planner-agent"}`

### Test Trip Planning
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

### Check Observability
1. Go to your [Langfuse Dashboard](https://cloud.langfuse.com/)
2. Navigate to your project
3. Look for incoming data (may take 1-10 minutes)

## 🔧 Troubleshooting

### Common Issues

**Backend won't start:**
- Check Python version: `python --version` (should be 3.8+)
- Verify virtual environment is activated
- Check all dependencies installed: `pip list`

**Frontend won't start:**
- Check Node.js version: `node --version` (should be 16+)
- Install dependencies: `cd frontend && npm install`

**No data in Langfuse:**
- Verify API keys in `.env` file
- Check Langfuse dashboard for traces
- Wait 1-10 minutes for data to appear

**API errors:**
- Check OpenAI API key is valid
- Verify Langfuse credentials are correct
- Check console logs for error messages

### Debug Commands

```bash
# Test Langfuse connection
python3 -c "from langfuse import Langfuse; print('Langfuse connection test')"

# Check environment variables
python3 -c "import os; print('LANGFUSE_SECRET_KEY:', 'Set' if os.getenv('LANGFUSE_SECRET_KEY') else 'Missing')"

# Test API endpoint
curl http://localhost:8000/docs
```

## 📊 What You'll See

### In the Application
- Beautiful trip planning form
- Real-time AI-powered trip recommendations
- Detailed itineraries with budgets
- Accommodation and activity suggestions

### In Langfuse Dashboard
- Real-time LLM call monitoring
- Token usage and cost tracking
- Workflow execution traces
- Performance metrics and alerts

## 🎯 Next Steps

1. **Explore the Dashboard**: Check out all the observability features in Langfuse
2. **Customize the Agents**: Modify the trip planning logic in `backend/trip_planner_agent.py`
3. **Add New Features**: Extend the application with additional capabilities
4. **Deploy**: Follow the deployment guide in the main README

## 📚 Learn More

- [Full Documentation](README.md)
- [Observability Guide](OBSERVABILITY.md)
- [API Documentation](http://localhost:8000/docs)

## 🆘 Need Help?

1. Check the troubleshooting section above
2. Review the full documentation
3. Check the application logs
4. Verify your API keys and credentials

Happy trip planning! 🗺️✈️




