import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function ReptilePage() {
  const { id } = useRouter().query; // Get dynamic ID from URL
  const [reptile, setReptile] = useState(null);
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState(null); 

  useEffect(() => {
    if (id) {
      setLoading(true); 
      fetch(`/api/reptile/${id}`)
        .then((res) => res.json())
        .then((data) => {
          setReptile(data);
          setLoading(false); 
        })
        .catch((err) => {
          setError('Error fetching data');
          setLoading(false); 
          console.error('Fetch error:', err);
        });
    }
  }, [id]);

  if (loading) return <p>Loading...</p>; 
  if (error) return <p>{error}</p>; 
  if (!reptile) return <p>No reptile found.</p>; 

  const {
    higher_taxa,
    genus,
    species,
    authority,
    year,
    common_names,
    distribution_raw,
    synonyms,
    valid,
    notes,
    diagnosis_raw,
    type_specimens,
    media_links,
    identifier,
    etymology,
    catalog_number,
    external_id,
    reproduction
  } = reptile;

  // Default to "N/A" for empty fields
  const displayValue = (value) => (value ? value : 'N/A');

  return (
    <div style={containerStyle}>
      <h1 style={headerStyle}>{higher_taxa}</h1>

      <div style={infoStyle}>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <div style={infoStyle}>
          <strong>Higher_taxa:</strong> {displayValue(higher_taxa)}
        </div>
        <div style={infoStyle}>
          <strong>Genus:</strong> {displayValue(genus)}
        </div>
        <div style={infoStyle}>
          <strong>Common Names:</strong> {displayValue(common_names)}
        </div>
        <div style={infoStyle}>
          <strong>Distribution:</strong> {displayValue(distribution_raw)}
        </div>
        <div style={infoStyle}>
          <strong>Species:</strong> {displayValue(species)}
        </div>
        <div style={infoStyle}>
          <strong>Authority:</strong> {displayValue(authority)}
        </div>
        <div style={infoStyle}>
          <strong>Synonyms:</strong> {displayValue(synonyms)}
        </div>  
        <div style={infoStyle}>
          <strong>Year:</strong> {displayValue(year)}
        </div>
        <div style={infoStyle}>
          <strong>Valid:</strong> {displayValue(valid)}
        </div>
        <div style={infoStyle}>
          <strong>Notes:</strong> {displayValue(notes)}
        </div>
        <div style={infoStyle}>
          <strong>Diagnosis:</strong> {displayValue(diagnosis_raw)}
        </div>
        <div style={infoStyle}>
          <strong>Type Specimens:</strong> {displayValue(type_specimens)}
        </div>
        <div style={infoStyle}>
          <strong>Media Links:</strong> {displayValue(media_links)}
        </div>
        <div style={infoStyle}>
          <strong>Identifier:</strong> {displayValue(identifier)}
        </div>
        <div style={infoStyle}>
          <strong>Etymology:</strong> {displayValue(etymology)}
        </div>
        <div style={infoStyle}>
          <strong>Catalog Number:</strong> {displayValue(catalog_number)}
        </div>
        <div style={infoStyle}>
          <strong>External ID:</strong> {displayValue(external_id)}
        </div>
        <div style={infoStyle}>
          <strong>Reproduction:</strong> {displayValue(reproduction)}
        </div>
      </div>
    </div>
  );
}

const containerStyle = {
  padding: '2rem',
  fontFamily: 'sans-serif',
  backgroundColor: 'black',
  color: 'white',
  minHeight: '100vh', 
};

const headerStyle = {
  fontSize: '2rem',
  marginBottom: '0.5rem',
  color: 'white',
};

const infoStyle = {
  marginBottom: '1rem',
  fontSize: '1rem',
  color: 'white', 
};
