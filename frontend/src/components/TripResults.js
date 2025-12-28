import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, MapPin, Calendar, DollarSign, Heart, Download, Share2 } from 'lucide-react';
import { useTrip } from '../context/TripContext';

const TripResults = () => {
  const navigate = useNavigate();
  const { tripData, reset } = useTrip();

  if (!tripData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 mb-4">No trip data available</p>
        <button
          onClick={() => navigate('/')}
          className="btn-primary"
        >
          Plan a New Trip
        </button>
      </div>
    );
  }

  const handleNewTrip = () => {
    reset();
    navigate('/');
  };

  const handleDownload = () => {
    const dataStr = JSON.stringify(tripData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'trip-plan.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'My Trip Plan',
          text: `Check out my trip plan for ${tripData.destination}!`,
          url: window.location.href,
        });
      } catch (error) {
        console.log('Error sharing:', error);
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      alert('Trip plan link copied to clipboard!');
    }
  };

  const handleBookAccommodation = () => {
    const searchQuery = encodeURIComponent(`${tripData.destination} ${tripData.accommodation_type || 'hotel'}`);
    window.open(`https://www.booking.com/searchresults.html?ss=${searchQuery}`, '_blank');
  };

  const handleFindFlights = () => {
    const searchQuery = encodeURIComponent(`flights to ${tripData.destination}`);
    window.open(`https://www.google.com/travel/flights?q=${searchQuery}`, '_blank');
  };

  const handleCreateItinerary = () => {
    const summary = tripData.final_plan?.summary;
    const itineraryText = typeof summary === 'string' 
      ? summary 
      : summary?.summary || 'Trip plan details';
    const blob = new Blob([itineraryText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${tripData.destination}-itinerary.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleSetReminders = () => {
    const startDate = new Date(tripData.travel_dates?.start || new Date());
    // eslint-disable-next-line no-unused-vars
    const reminderDate = new Date(startDate.getTime() - 7 * 24 * 60 * 60 * 1000); // 7 days before
    
    const reminderText = `Trip to ${tripData.destination} starts in 7 days!`;
    
    if ('Notification' in window) {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          new Notification('Trip Reminder', {
            body: reminderText,
            icon: '/favicon.ico'
          });
        } else {
          alert(`Reminder: ${reminderText}`);
        }
      });
    } else {
      alert(`Reminder: ${reminderText}`);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center space-x-4">
          <button
            onClick={handleNewTrip}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="h-5 w-5" />
            <span>Plan Another Trip</span>
          </button>
        </div>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={handleDownload}
            className="flex items-center space-x-2 btn-secondary"
          >
            <Download className="h-4 w-4" />
            <span>Download</span>
          </button>
          <button
            onClick={handleShare}
            className="flex items-center space-x-2 btn-secondary"
          >
            <Share2 className="h-4 w-4" />
            <span>Share</span>
          </button>
        </div>
      </div>

      {/* Trip Overview */}
      <div className="card mb-8">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Your Trip to {tripData.destination}
          </h1>
          <p className="text-lg text-gray-600">
            {tripData.duration} days • ${tripData.budget} budget
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg">
            <MapPin className="h-6 w-6 text-primary-600" />
            <div>
              <p className="text-sm text-gray-500">Destination</p>
              <p className="font-semibold text-gray-900">{tripData.destination}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg">
            <Calendar className="h-6 w-6 text-primary-600" />
            <div>
              <p className="text-sm text-gray-500">Duration</p>
              <p className="font-semibold text-gray-900">{tripData.duration} days</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg">
            <DollarSign className="h-6 w-6 text-primary-600" />
            <div>
              <p className="text-sm text-gray-500">Budget</p>
              <p className="font-semibold text-gray-900">${tripData.budget}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg">
            <Heart className="h-6 w-6 text-primary-600" />
            <div>
              <p className="text-sm text-gray-500">Interests</p>
              <p className="font-semibold text-gray-900">
                {tripData.interests?.length || 0} selected
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Trip Plan Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Main Content */}
        <div className="space-y-6">
          {/* Final Plan Summary */}
          {tripData.final_plan && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Trip Plan Summary
              </h2>
              <div className="prose prose-gray max-w-none">
                {tripData.final_plan.summary ? (
                  <div className="whitespace-pre-wrap text-gray-700">
                    {typeof tripData.final_plan.summary === 'string' 
                      ? tripData.final_plan.summary 
                      : tripData.final_plan.summary.summary || 'No summary available'}
                  </div>
                ) : (
                  <p className="text-gray-500">No summary available</p>
                )}
              </div>
            </div>
          )}

          {/* Messages/Conversation */}
          {tripData.messages && tripData.messages.length > 0 && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Planning Process
              </h2>
              <div className="space-y-4">
                {tripData.messages.map((message, index) => (
                  <div
                    key={index}
                    className="p-4 bg-gray-50 rounded-lg"
                  >
                    <div className="text-sm text-gray-500 mb-2">
                      Step {index + 1}
                    </div>
                    <div className="text-gray-700 whitespace-pre-wrap">
                      {message}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Quick Actions
            </h3>
            <div className="space-y-3">
              <button 
                onClick={handleBookAccommodation}
                className="w-full btn-primary"
              >
                Book Accommodation
              </button>
              <button 
                onClick={handleFindFlights}
                className="w-full btn-secondary"
              >
                Find Flights
              </button>
              <button 
                onClick={handleCreateItinerary}
                className="w-full btn-secondary"
              >
                Create Itinerary
              </button>
              <button 
                onClick={handleSetReminders}
                className="w-full btn-secondary"
              >
                Set Reminders
              </button>
            </div>
          </div>

          {/* Trip Details */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Trip Details
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Destination</span>
                <span className="font-medium">{tripData.destination}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Duration</span>
                <span className="font-medium">{tripData.duration} days</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Budget</span>
                <span className="font-medium">${tripData.budget}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Daily Budget</span>
                <span className="font-medium">
                  ${Math.round(tripData.budget / tripData.duration)}
                </span>
              </div>
            </div>
          </div>

          {/* Tips */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Travel Tips
            </h3>
            <div className="space-y-3 text-sm text-gray-600">
              <div className="flex items-start space-x-2">
                <div className="w-2 h-2 bg-primary-600 rounded-full mt-2 flex-shrink-0"></div>
                <p>Book accommodations in advance for better rates</p>
              </div>
              <div className="flex items-start space-x-2">
                <div className="w-2 h-2 bg-primary-600 rounded-full mt-2 flex-shrink-0"></div>
                <p>Check visa requirements for your destination</p>
              </div>
              <div className="flex items-start space-x-2">
                <div className="w-2 h-2 bg-primary-600 rounded-full mt-2 flex-shrink-0"></div>
                <p>Purchase travel insurance for peace of mind</p>
              </div>
              <div className="flex items-start space-x-2">
                <div className="w-2 h-2 bg-primary-600 rounded-full mt-2 flex-shrink-0"></div>
                <p>Download offline maps and translation apps</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TripResults;
