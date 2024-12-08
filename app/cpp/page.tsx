import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

export default function BookingPage() {
  const [flights, setFlights] = useState([]);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [bookingInfo, setBookingInfo] = useState({
    flightNumber: '',
    idNumber: '',
    name: '',
    gender: '',
    birthDate: '',
    seatNumber: '',
  });
  const router = useRouter();

  useEffect(() => {
    // Fetch available flights when the component mounts
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

  const handleFlightSelect = (flight) => {
    setSelectedFlight(flight);
    setBookingInfo({ ...bookingInfo, flightNumber: flight.flight_number });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setBookingInfo({ ...bookingInfo, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bookingInfo),
      });
      const data = await response.json();
      if (response.ok) {
        alert('Booking successful!');
        router.push('/booking-confirmation');
      } else {
        alert(`Booking failed: ${data.error}`);
      }
    } catch (error) {
      console.error('Error submitting booking:', error);
      alert('An error occurred while booking. Please try again.');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Flight Booking</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h2 className="text-xl font-semibold mb-2">Available Flights</h2>
          <ul className="space-y-2">
            {flights.map((flight) => (
              <li
                key={flight.flight_number}
                className={`p-2 border rounded cursor-pointer ${
                  selectedFlight?.flight_number === flight.flight_number ? 'bg-blue-100' : ''
                }`}
                onClick={() => handleFlightSelect(flight)}
              >
                {flight.flight_number} - {flight.departure_location} to {flight.arrival_location}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-2">Booking Information</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="name" className="block">Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={bookingInfo.name}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <div>
              <label htmlFor="idNumber" className="block">ID Number</label>
              <input
                type="text"
                id="idNumber"
                name="idNumber"
                value={bookingInfo.idNumber}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <div>
              <label htmlFor="gender" className="block">Gender</label>
              <select
                id="gender"
                name="gender"
                value={bookingInfo.gender}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              >
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label htmlFor="birthDate" className="block">Birth Date</label>
              <input
                type="date"
                id="birthDate"
                name="birthDate"
                value={bookingInfo.birthDate}
                onChange={handleInputChange}
                required
                className="w-full border rounded p-2"
              />
            </div>
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              disabled={!selectedFlight}
            >
              Book Flight
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}