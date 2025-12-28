import axios from 'axios';
import { Calendar, DollarSign, Heart, Home, MapPin, Plane } from 'lucide-react';
import { useState } from 'react';
import { Route, BrowserRouter as Router, Routes, useNavigate } from 'react-router-dom';
import TripResults from './components/TripResults';
import { TripProvider, useTrip } from './context/TripContext';
import './index.css';

const TripPlannerForm = () => {
  const navigate = useNavigate();
  const { setTripData } = useTrip();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    destination: '',
    duration: 3,
    budget: 1000,
    interests: '',
    start_date: new Date().toISOString().split('T')[0],
    end_date: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    accommodation_type: 'hotel',
    transportation_type: 'flight'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Convert interests string to array
      const payload = {
        ...formData,
        interests: formData.interests.split(',').map(i => i.trim()).filter(i => i),
        budget: Number(formData.budget),
        duration: Number(formData.duration)
      };

      const response = await axios.post('/plan-trip', payload);
      
      if (response.data.success) {
        setTripData(response.data.data);
        navigate('/results');
      } else {
        alert('Failed to plan trip: ' + response.data.error);
      }
    } catch (error) {
      console.error('Error planning trip:', error);
      alert('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI Trip Planner
        </h1>
        <p className="text-lg text-gray-600">
          Tell us your preferences, and we'll craft the perfect itinerary for you.
        </p>
      </div>

      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="flex items-center text-sm font-medium text-gray-700">
                <MapPin className="w-4 h-4 mr-2" />
                Destination
              </label>
              <input
                type="text"
                name="destination"
                required
                className="input-field"
                placeholder="e.g., Paris, Tokyo"
                value={formData.destination}
                onChange={handleChange}
              />
            </div>

            <div className="space-y-2">
              <label className="flex items-center text-sm font-medium text-gray-700">
                <Calendar className="w-4 h-4 mr-2" />
                Dates
              </label>
              <div className="flex space-x-2">
                <input
                  type="date"
                  name="start_date"
                  required
                  className="input-field"
                  value={formData.start_date}
                  onChange={handleChange}
                />
                <input
                  type="date"
                  name="end_date"
                  required
                  className="input-field"
                  value={formData.end_date}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="flex items-center text-sm font-medium text-gray-700">
                <DollarSign className="w-4 h-4 mr-2" />
                Budget (USD)
              </label>
              <input
                type="number"
                name="budget"
                required
                min="0"
                className="input-field"
                value={formData.budget}
                onChange={handleChange}
              />
            </div>

            <div className="space-y-2">
              <label className="flex items-center text-sm font-medium text-gray-700">
                <Calendar className="w-4 h-4 mr-2" />
                Duration (Days)
              </label>
              <input
                type="number"
                name="duration"
                required
                min="1"
                className="input-field"
                value={formData.duration}
                onChange={handleChange}
              />
            </div>

            <div className="space-y-2">
              <label className="flex items-center text-sm font-medium text-gray-700">
                <Home className="w-4 h-4 mr-2" />
                Accommodation
              </label>
              <select
                name="accommodation_type"
                className="input-field"
                value={formData.accommodation_type}
                onChange={handleChange}
              >
                <option value="hotel">Hotel</option>
                <option value="airbnb">Airbnb</option>
                <option value="hostel">Hostel</option>
                <option value="resort">Resort</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="flex items-center text-sm font-medium text-gray-700">
                <Plane className="w-4 h-4 mr-2" />
                Transportation
              </label>
              <select
                name="transportation_type"
                className="input-field"
                value={formData.transportation_type}
                onChange={handleChange}
              >
                <option value="flight">Flight</option>
                <option value="train">Train</option>
                <option value="car">Car Rental</option>
                <option value="bus">Bus</option>
              </select>
            </div>
          </div>

          <div className="space-y-2">
            <label className="flex items-center text-sm font-medium text-gray-700">
              <Heart className="w-4 h-4 mr-2" />
              Interests (comma separated)
            </label>
            <input
              type="text"
              name="interests"
              className="input-field"
              placeholder="e.g., museums, food, hiking, shopping"
              value={formData.interests}
              onChange={handleChange}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary flex justify-center items-center h-12 text-lg"
          >
            {loading ? (
              <span className="animate-pulse">Generating Trip Plan...</span>
            ) : (
              'Plan My Trip'
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

const App = () => {
  return (
    <TripProvider>
      <Router>
        <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<TripPlannerForm />} />
            <Route path="/results" element={<TripResults />} />
          </Routes>
        </div>
      </Router>
    </TripProvider>
  );
};

export default App;
