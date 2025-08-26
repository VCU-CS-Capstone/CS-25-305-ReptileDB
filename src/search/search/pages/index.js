import { useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [query, setQuery] = useState(''); // For capturing user input
  const [results, setResults] = useState([]); // To store search results
  const [loading, setLoading] = useState(false); // For loading state

  // This function is called when the user types in the search input
  const handleSearch = async (event) => {
    setQuery(event.target.value); // Update query as user types

    if (event.target.value.trim().length > 0) {
      setLoading(true); // Show loading spinner

      try {
        const res = await fetch(`/api/search?query=${event.target.value}`);
        const data = await res.json();

        if (res.ok) {
          setResults(data); // Update the results state with fetched data
        } else {
          console.error('Error fetching results:', data);
        }
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false); // Hide loading spinner
      }
    } else {
      setResults([]); // Clear results if search query is empty
    }
  };

  return (
    <div>
      <h1>Search Page</h1>
      <input
        type="text"
        placeholder="Search for an item"
        value={query}
        onChange={handleSearch}
      />
      {loading && <p>Loading...</p>} {/* Show loading text when fetching */}
      <div>
        <h2>Results:</h2>
        <ul>
          {results.map((item) => (
            <li key={item.id}>
              <Link href={`/item/${item.id}`}>
                <a>{item.name}</a> {/* Show the name of the item */}
              </Link>
            </li>
          ))}
        </ul>
      </div>
      <div style={{ marginTop: '20px' }}>
        <Link href="/showcase">Dashboard
        </Link>
      </div>
    </div>

    
  );
}

