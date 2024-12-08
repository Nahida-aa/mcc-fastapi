import React, { useState, useEffect } from 'react';

export default function AdminPage() {
  const [flights, setFlights] = useState([]);
  const [newFlight, setNewFlight] = useState({
    flight_number: '',
    max_passengers: '',
    departure_location: '',
    departure_time: '',
    arrival_location: '',
    arrival_time: '',
    price: '',
  });

  useEffect(() => {
    fetchFlights();
  }, []);

  const fetchFlights = async () => {
    try {
      const response = await fetch('/api/flights');
      const data = await response.json();
      setFlights(data);
    } catch (error) {
      console.error('Error fetching flights:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewFlight({ ...newFlight, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/flights', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newFlight),
      });
      if (response.ok) {
        alert('Flight added successfully!');
        setNewFlight({
          flight_number: '',
          max_passengers: '',
          departure_location: '',
          departure_time: '',
          arrival_location: '',
          arrival_time: '',
          price: '',
        });
        fetchFlights();
      } else {
        const data = await response.json();
        alert(`Failed to add flight: ${data.error}`);
      }
    } catch (error) {
      console.error('Error adding flight:', error);
      alert('An error occurred while adding the flight. Please try again.');
    }
  };

  const handleCancelFlight = async (flightNumber) => {
    try {
      const response = await fetch(`/api/flights/cancel/${flightNumber}`, {
        method: 'PUT',
      });
      if (response.ok) {
        alert('Flight cancelled successfully!');
        fetchFlights();
      } else {
        const data = await response.json();
        alert(`Failed to cancel flight: ${data.error}`);
      }
    } catch (error) {
      console.error('Error cancelling flight:', error);
      alert('An error occurred while cancelling the flight. Please try again.');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h2 className="text-xl font-semibold mb-2">Add New Flight</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="flight_number" className="block">Flight Number</label>
              <input
                type="text"
                id="flight_number"
                name="flight_number"
                value={newFlight.flight_number}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <div>
              <label htmlFor="max_passengers" className="block">Max Passengers</label>
              <input
                type="number"
                id="max_passengers"
                name="max_passengers"
                value={newFlight.max_passengers}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <div>
              <label htmlFor="departure_location" className="block">Departure Location</label>
              <input
                type="text"
                id="departure_location"
                name="departure_location"
                value={newFlight.departure_location}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <div>
              <label htmlFor="departure_time" className="block">Departure Time</label>
              <input
                type="datetime-local"
                id="departure_time"
                name="departure_time"
                value={newFlight.departure_time}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <div>
              <label htmlFor="arrival_location" className="block">Arrival Location</label>
              <input
                type="text"
                id="arrival_location"
                name="arrival_location"
                value={newFlight.arrival_location}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <div>
              <label htmlFor="arrival_time" className="block">Arrival Time</label>
              <input
                type="datetime-local"
                id="arrival_time"
                name="arrival_time"
                value={newFlight.arrival_time}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <div>
              <label htmlFor="price" className="block">Price</label>
              <input
                type="number"
                id="price"
                name="price"
                value={newFlight.price}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <button
              type="submit"
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              Add Flight
            </button>
          </form>
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-2">Manage Flights</h2>
          <ul className="space-y-2">
            {flights.map((flight) => (
              <li key={flight.flight_number} className="p-2 border rounded">
                <p>{flight.flight_number} - {flight.departure_location} to {flight.arrival_location}</p>
                <p>Departure: {flight.departure_time}</p>
                <p>Arrival: {flight.arrival_time}</p>
                <p>Available Seats: {flight.available_seats} / {flight.max_passengers}</p>
                <button
                  onClick={() => handleCancelFlight(flight.flight_number)}
                  className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600 mt-2"
                  disabled={flight.is_cancelled}
                >
                  {flight.is_cancelled ? 'Cancelled' : 'Cancel Flight'}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}