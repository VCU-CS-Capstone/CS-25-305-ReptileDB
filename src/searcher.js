import { useState } from 'react';
import Link from 'next/link';

export default function Search() {
  const [searchMode, setSearchMode] = useState(''); // 'basic' or 'advanced'

  // Basic Search State
  const [basicQuery, setBasicQuery] = useState('');
  const [basicField, setBasicField] = useState('common_names');

  // Advanced Search State
  const [form, setForm] = useState({
    common_name: '',
    higher_taxa: '',
    genus: '',
    species: '',
    authority: '',
    year: '',
    valid: '',
    synonyms: '',
    distribution: '',
    notes: '',
    diagnosis: '',
    type_specimens: '',
    media_links: '',
    identifier: '',
    etymology: '',
    catalog_number: '',
    external_id: '',
    reproduction: ''
  });

  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    let url = '';
    let params = new URLSearchParams();

    if (searchMode === 'basic') {
      if (!basicQuery.trim()) return;
      url = 'http://localhost:5000/api/search_dynamic';
      params.append('query', basicQuery);
      params.append('field', basicField);
    } else {
      url = 'http://localhost:5000/api/advanced_search';
      let anyFilled = false;
      Object.entries(form).forEach(([key, value]) => {
        if (value.trim()) {
          params.append(key, value);
          anyFilled = true;
        }
      });
      if (!anyFilled) return;
    }

    try {
      const response = await fetch(`${url}?${params}`);
      const data = await response.json();
      if (!response.ok) {
        setError(data.error || 'Unknown error');
        setResults([]);
        return;
      }
      setResults(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      setResults([]);
    }
  };

  const updateField = (key, value) => {
    setForm(prev => ({ ...prev, [key]: value }));
  };

  const fieldLabels = {
    common_name: 'Common Name',
    higher_taxa: 'Higher Taxa',
    genus: 'Genus',
    species: 'Species',
    authority: 'Authority',
    year: 'Year',
    valid: 'Valid',
    synonyms: 'Synonyms',
    distribution: 'Distribution',
    notes: 'Notes',
    diagnosis: 'Diagnosis',
    type_specimens: 'Type Specimens',
    media_links: 'Media Links',
    identifier: 'Identifier',
    etymology: 'Etymology',
    catalog_number: 'Catalog Number',
    external_id: 'External ID',
    reproduction: 'Reproduction'
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>{searchMode === 'basic' ? 'Search Species' : 'Advanced Species Search'}</h1>

      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => setSearchMode('basic')} style={{ marginRight: '10px' }}>
          Basic Search
        </button>
        <button onClick={() => setSearchMode('advanced')}>Advanced Search</button>
      </div>

      {searchMode === 'basic' ? (
        <>
          <input
            type="text"
            value={basicQuery}
            onChange={(e) => setBasicQuery(e.target.value)}
            placeholder="Enter search term"
            style={{ padding: '8px', marginRight: '10px' }}
          />
          <select
            value={basicField}
            onChange={(e) => setBasicField(e.target.value)}
            style={{ padding: '8px', marginRight: '10px' }}
          >
            {Object.keys(fieldLabels).map((key) => (
              <option key={key} value={key}>
                {fieldLabels[key]}
              </option>
            ))}
          </select>
        </>
      ) : (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '10px' }}>
          {Object.entries(fieldLabels).map(([key, label]) => (
            <input
              key={key}
              type="text"
              placeholder={label}
              value={form[key]}
              onChange={(e) => updateField(key, e.target.value)}
              style={{ padding: '8px', minWidth: '200px' }}
            />
          ))}
        </div>
      )}

      <button onClick={handleSearch} style={{ padding: '8px' }}>
        Search
      </button>

      <div style={{ marginTop: '20px' }}>
        {error && <div style={{ color: 'red' }}>Error: {error}</div>}

        <h2>Results:</h2>
        <ul>
          {results.length > 0 ? (
            results.map((item, index) => (
              <li key={index} style={{ marginBottom: '10px' }}>
                <Link href={`/reptile/${item.species_id}`}>
                  <strong>{item.common_names || 'Unnamed Reptile'}</strong>
                  <br />
                  <em>{item.genus} {item.species}</em>
                </Link>
                <br />
                <span>Higher Taxa: {item.higher_taxa || 'N/A'}</span><br />
                <span>Genus: {item.genus || 'Unknown'}</span><br />
                <span>Reproduction: {item.reproduction || 'N/A'}</span><br />
                <span>Distribution: {item.distribution_raw || 'N/A'}</span>
              </li>
            ))
          ) : (
            !error && <li>No results found</li>
          )}
        </ul>
      </div>
    </div>
  );
}
