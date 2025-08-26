import { useState } from 'react';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);

  // Function to handle search when user types
  const search = async () => {
    if (searchQuery.trim() === '') return; // Avoid empty searches
    
    const response = await fetch(`http://localhost:5000/api/search?query=${encodeURIComponent(searchQuery)}`);
    if (!response.ok) {
      throw new Error('Reptile not found: ' + response.status);
    }
    const data = await response.json();
    setResults(data); // Directly set the entire result array
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Search</h1>
      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Enter search term"
        style={{ padding: '8px', marginRight: '10px' }}
      />
      <button onClick={search} style={{ padding: '8px' }}>Search</button>

      <div style={{ marginTop: '20px' }}>
        <h2>Results:</h2>
        <ul>
          {results.length > 0 ? (
            results.map((item, index) => (
              <li key={index}>
                <strong>{item.common_names}</strong>
                <br />
                <span>Scientific Name: {item.species}</span>
                <br />
                <span>Genus: {item.genus}</span>
                <br />
                <span>common names: {item.common_names}</span>
                <br />
                <span>Scientific Name: {item.species}</span>
                <br />
                <span>Reproduction: {item.reproduction || "Test build"}</span>
                <span>Distribution: {item.distribution || 'Unknown'}</span>
              </li>
            ))
          ) : (
            <li>No results found</li>
          )}
        </ul>
      </div>
    </div>
  );
}