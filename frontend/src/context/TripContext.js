import React, { createContext, useContext, useState } from 'react';

const TripContext = createContext();

export const TripProvider = ({ children }) => {
  const [tripData, setTripData] = useState(null);

  const reset = () => {
    setTripData(null);
  };

  return (
    <TripContext.Provider value={{ tripData, setTripData, reset }}>
      {children}
    </TripContext.Provider>
  );
};

export const useTrip = () => {
  const context = useContext(TripContext);
  if (!context) {
    throw new Error('useTrip must be used within a TripProvider');
  }
  return context;
};
