# Trip Planner Frontend

A modern React frontend for the AI-powered Trip Planner Agent.

## Features

- **Modern UI**: Built with React and Tailwind CSS for a beautiful, responsive design
- **Trip Planning Form**: Comprehensive form to capture all trip preferences
- **Real-time Results**: Display AI-generated trip plans with detailed recommendations
- **Interactive Components**: Dynamic interest selection and preference customization
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## Tech Stack

- **React 18**: Modern React with hooks and functional components
- **React Router**: Client-side routing for navigation
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Lucide React**: Beautiful, customizable icons
- **Axios**: HTTP client for API communication
- **Context API**: State management for trip data

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running on port 8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── components/          # React components
│   ├── Header.js       # Navigation header
│   ├── TripPlanner.js  # Main trip planning form
│   ├── TripResults.js  # Results display
│   └── LoadingSpinner.js # Loading component
├── context/            # React Context for state management
│   └── TripContext.js  # Trip state management
├── services/           # API services
│   └── api.js         # API client
├── App.js             # Main app component
├── index.js           # App entry point
└── index.css          # Global styles
```

## Available Scripts

- `npm start`: Runs the app in development mode
- `npm build`: Builds the app for production
- `npm test`: Launches the test runner
- `npm eject`: Ejects from Create React App (one-way operation)

## API Integration

The frontend communicates with the backend API through the following endpoints:

- `POST /plan-trip`: Submit trip planning request
- `GET /destinations`: Get popular destinations
- `GET /interests`: Get common travel interests
- `GET /health`: Health check

## Features Overview

### Trip Planning Form
- Destination selection with popular options
- Duration and budget configuration
- Travel date selection
- Interest/activity selection
- Accommodation and transportation preferences

### Results Display
- Comprehensive trip plan summary
- Planning process visualization
- Quick action buttons
- Trip details sidebar
- Download and share functionality

### Responsive Design
- Mobile-first approach
- Adaptive layouts for all screen sizes
- Touch-friendly interface
- Optimized for performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Trip Planner Agent system.
