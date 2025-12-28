# VS Code Setup Guide for Trip Planner Agent

This guide will help you set up VS Code with GitHub Copilot for optimal development experience with this AI-powered trip planning application.

## 🤖 GitHub Copilot Agent Mode Migration Guide

### Step-by-Step Migration to GitHub Copilot Agent Mode

#### 1. **Open the Workspace in VS Code**
```bash
# Navigate to your project directory
cd /path/to/trip-planner-agent

# Open the workspace file
code trip-planner-agent.code-workspace
```

#### 2. **Install GitHub Copilot Agent Extension**
- Open VS Code Extensions (Ctrl+Shift+X)
- Search for "GitHub Copilot Agent"
- Install the extension
- Restart VS Code if prompted

#### 3. **Activate GitHub Copilot Agent Mode**
- Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
- Type "GitHub Copilot Agent: Start Agent Mode"
- Select and activate Agent Mode
- You'll see the Copilot Agent panel open

#### 4. **Configure Agent Context**
- In the Copilot Agent panel, click "Configure Context"
- Select "Load from Workspace" to use the `.vscode/copilot.json` configuration
- The agent will load project-specific rules and context

#### 5. **Initialize the Project**
```bash
# In the Copilot Agent chat, type:
"Initialize this trip planner project. Set up the Python virtual environment, install dependencies, and start both the backend and frontend services."
```

#### 6. **Verify Setup**
- The agent will guide you through:
  - Creating/activating Python virtual environment
  - Installing Python dependencies (`pip install -r requirements.txt`)
  - Installing Node.js dependencies (`cd frontend && npm install`)
  - Setting up environment variables (`.env` file)
  - Starting both services

#### 7. **Test the Application**
```bash
# In the Copilot Agent chat, type:
"Test the trip planner application. Make a sample API call to verify the backend is working and check if the frontend loads correctly."
```

#### 8. **Enable LangGraph Tracing**
```bash
# In the Copilot Agent chat, type:
"Help me verify that Langfuse tracing is working properly for the LangGraph workflow. Check the configuration and test a trip planning request."
```

### 🎯 **Key Commands for Copilot Agent Mode**

#### **Project Management**
- `"Show me the project structure and explain each component"`
- `"Help me understand the LangGraph workflow architecture"`
- `"Explain the multi-agent system and how agents communicate"`

#### **Development Tasks**
- `"Start the backend server and show me the logs"`
- `"Start the frontend development server"`
- `"Run the test suite and show me any failures"`
- `"Format the Python code using Black"`

#### **Debugging and Troubleshooting**
- `"Help me debug this error: [paste error message]"`
- `"Check the Langfuse integration and verify traces are being sent"`
- `"Analyze the API response and suggest improvements"`

#### **Feature Development**
- `"Add a new agent to the LangGraph workflow for [specific purpose]"`
- `"Create a new API endpoint for [specific functionality]"`
- `"Add a new React component for [specific UI element]"`
- `"Improve error handling in the [specific module]"`

#### **Code Review and Optimization**
- `"Review this code and suggest improvements for performance"`
- `"Check for security vulnerabilities in the API endpoints"`
- `"Optimize the LangGraph workflow for better performance"`
- `"Suggest best practices for the React components"`

### 🔧 **Advanced Agent Mode Features**

#### **Context-Aware Development**
- The agent understands your multi-agent AI architecture
- Recognizes LangGraph workflow patterns
- Suggests FastAPI best practices
- Provides React component patterns

#### **Intelligent Code Generation**
- Generates API endpoints with proper validation
- Creates LangGraph agents with state management
- Builds React components with modern hooks
- Suggests Pydantic models with validation

#### **Automated Problem Solving**
- Analyzes error logs and suggests fixes
- Identifies performance bottlenecks
- Recommends code refactoring
- Suggests testing strategies

### 📋 **Migration Checklist**

- [ ] VS Code workspace opened
- [ ] GitHub Copilot Agent extension installed
- [ ] Agent mode activated
- [ ] Project context loaded
- [ ] Python virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Backend service started
- [ ] Frontend service started
- [ ] API endpoints tested
- [ ] Langfuse tracing verified
- [ ] Full application tested

### 🚨 **Troubleshooting Agent Mode**

#### **If Agent Mode Doesn't Start**
- Check if GitHub Copilot is properly authenticated
- Verify the extension is enabled
- Restart VS Code
- Check internet connection

#### **If Context Loading Fails**
- Ensure `.vscode/copilot.json` exists
- Check file permissions
- Manually configure context if needed

#### **If Services Don't Start**
- Check Python/Node.js installation
- Verify environment variables
- Check port availability
- Review error logs

### 🎉 **Success Indicators**

You'll know the migration is successful when:
- ✅ Copilot Agent panel is active
- ✅ Project context is loaded
- ✅ Both services are running
- ✅ API calls work correctly
- ✅ Langfuse traces are visible
- ✅ Frontend loads without errors
- ✅ Agent can answer project-specific questions

---

## 🚀 Quick Start

1. **Open the workspace**: Open `trip-planner-agent.code-workspace` in VS Code
2. **Install recommended extensions**: VS Code will prompt you to install recommended extensions
3. **Set up environment**: Fo

4. **Start coding**: Use the provided tasks and launch configurations

## 📁 Project Structure

```
trip-planner-agent/
├── .vscode/                    # VS Code configuration
│   ├── settings.json          # Workspace settings
│   ├── launch.json            # Debug configurations
│   ├── tasks.json             # Build and run tasks
│   ├── extensions.json        # Recommended extensions
│   ├── copilot.json           # GitHub Copilot rules
│   └── snippets/              # Code snippets
├── backend/                   # FastAPI + LangGraph backend
├── frontend/                  # React frontend
└── venv/                     # Python virtual environment
```

## 🔧 Environment Setup

### 1. Python Environment
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Node.js Environment
```bash
# Install frontend dependencies
cd frontend
npm install
```

### 3. Environment Variables
```bash
# Copy environment template
cp env.example .env

# Edit .env with your API keys
# Required: OPENAI_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY
```

## 🎯 VS Code Features

### Launch Configurations
- **Start Backend Server**: Debug the FastAPI backend
- **Debug Trip Planning**: Debug the LangGraph workflow
- **Start Frontend**: Launch React development server
- **Start Full Stack**: Launch both backend and frontend

### Tasks
- **Install Python Dependencies**: Install backend requirements
- **Install Frontend Dependencies**: Install frontend packages
- **Start Backend**: Run the FastAPI server
- **Start Frontend**: Run the React development server
- **Run Tests**: Execute pytest tests
- **Format Python Code**: Format with Black
- **Lint Python Code**: Lint with Flake8

### Code Snippets
- **FastAPI Route**: Template for API endpoints
- **LangGraph Agent**: Template for AI agents
- **Pydantic Model**: Template for data models
- **LangChain Tool**: Template for LangChain tools
- **React Component**: Template for React components
- **API Call Hook**: Template for API integration
- **Form Component**: Template for forms

## 🤖 GitHub Copilot Integration

### Copilot Rules
The `.vscode/copilot.json` file contains specific rules for:
- Python best practices and PEP 8
- React best practices and modern hooks
- FastAPI best practices
- LangGraph and LangChain patterns
- Error handling and logging
- TypeScript/JavaScript best practices

### Context Awareness
Copilot is configured to understand:
- Multi-agent AI system architecture
- LangGraph workflow patterns
- FastAPI + React full-stack setup
- Langfuse observability integration

## 🛠️ Development Workflow

### 1. Start Development
```bash
# Option 1: Use VS Code tasks
Ctrl+Shift+P → "Tasks: Run Task" → "Start Full Stack"

# Option 2: Use launch configuration
F5 → "Start Full Stack"
```

### 2. Debug Backend
- Set breakpoints in Python files
- Use "Start Backend Server" launch configuration
- Debug LangGraph workflows with "Debug Trip Planning"

### 3. Debug Frontend
- Set breakpoints in React components
- Use "Start Frontend" launch configuration
- Use React Developer Tools

### 4. Code Quality
```bash
# Format Python code
Ctrl+Shift+P → "Tasks: Run Task" → "Format Python Code"

# Lint Python code
Ctrl+Shift+P → "Tasks: Run Task" → "Lint Python Code"

# Run tests
Ctrl+Shift+P → "Tasks: Run Task" → "Run Tests"
```

## 📚 Key Technologies

### Backend
- **FastAPI**: Web framework
- **LangGraph**: Multi-agent workflow
- **LangChain**: LLM integration
- **OpenAI**: Language models
- **Langfuse**: Observability and tracing
- **Pydantic**: Data validation

### Frontend
- **React**: UI framework
- **Tailwind CSS**: Styling
- **JavaScript**: Programming language
- **Node.js**: Runtime environment

## 🔍 Debugging Tips

### Backend Debugging
1. Set breakpoints in agent functions
2. Use the "Debug Trip Planning" configuration
3. Monitor Langfuse traces in the dashboard
4. Check console logs for LangGraph execution

### Frontend Debugging
1. Use React Developer Tools
2. Set breakpoints in component functions
3. Monitor network requests in DevTools
4. Check console for JavaScript errors

### Full-Stack Debugging
1. Use "Start Full Stack" configuration
2. Debug both backend and frontend simultaneously
3. Monitor API calls between frontend and backend
4. Check Langfuse for complete workflow traces

## 🚀 Deployment

### Backend Deployment
- Deploy to cloud platforms (Heroku, AWS, Google Cloud)
- Set environment variables in deployment platform
- Ensure OpenAI and Langfuse credentials are configured

### Frontend Deployment
- Build production version: `npm run build`
- Deploy to platforms (Netlify, Vercel, AWS S3)
- Update API URL in environment variables

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [React Documentation](https://react.dev/)
- [Langfuse Documentation](https://langfuse.com/docs)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

## 🆘 Troubleshooting

### Common Issues
1. **Python interpreter not found**: Set correct path in settings
2. **Dependencies not installed**: Run install tasks
3. **Environment variables missing**: Check .env file
4. **Port conflicts**: Change ports in launch configurations
5. **Copilot not working**: Check extension installation

### Getting Help
1. Check the troubleshooting sections in each guide
2. Review the comprehensive documentation
3. Use GitHub Copilot Chat for code assistance
4. Check the application logs for error messages

This setup provides a complete development environment optimized for AI application development with GitHub Copilot integration!
