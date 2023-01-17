import React, { useState, useEffect, useCallback } from "react";

export function FetchData() {
  const [environment, setEnvironment] = useState([]);
  const [rows, setRows] = useState(15);

  const fetchTemperatures = useCallback(() => {
    fetch("api/Info?rows=" + rows)
      .then((response) => response.json())
      .then((data) => {
        setEnvironment([...environment, ...data]);
        console.log(data);
      });
  }, []);

  useEffect(() => {
    fetchTemperatures();
  }, [fetchTemperatures]);

  return (
    <div>
      <h1 id="tabelLabel">Temperature & Humidity</h1>
      <div>
        <table className="table table-striped" aria-labelledby="tabelLabel">
          <thead>
            <tr>
              <th>Date</th>
              <th>Temperature</th>
              <th>Humidity</th>
            </tr>
          </thead>
          <tbody>
            {environment.map((temperature) => (
              <tr key={temperature.id}>
                <td>{temperature.time}</td>
                <td>{temperature.temperature} °C</td>
                <td>{temperature.humidity}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
