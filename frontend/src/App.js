import React, { useState } from "react";

function App() {
  const [zipcode1, setZipcode1] = useState("");
  const [zipcode2, setZipcode2] = useState("");
  const [distance, setDistance] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:8000/distance/?zipcode1=${zipcode1}&zipcode2=${zipcode2}`
      );
      const data = await response.json();

      if (response.ok) {
        setDistance(data.distance_mi.toFixed(2));
      } else {
        setError(data.detail);
      }
    } catch (err) {
      setError("An error occurred while fetching the distance.");
    }
  };

  return (
    <div className="App">
      <h1>Distance Calculator</h1>
      <form onSubmit={handleSubmit}>
        <label>
          First Zipcode:
          <input
            type="text"
            value={zipcode1}
            onChange={(e) => setZipcode1(e.target.value)}
            required
          />
        </label>
        <br />
        <label>
          Second Zipcode:
          <input
            type="text"
            value={zipcode2}
            onChange={(e) => setZipcode2(e.target.value)}
            required
          />
        </label>
        <br />
        <button type="submit">Calculate Distance</button>
      </form>

      {distance && <h2>Distance: {distance} miles</h2>}
      {error && <h2 style={{ color: "red" }}>{error}</h2>}
    </div>
  );
}

export default App;
