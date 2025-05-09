import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

//Had trouble with broken icons for the observation pinpoints. This manual override fixes that so Do Not Touch
import L from 'leaflet';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x.src || markerIcon2x,
  iconUrl: markerIcon.src || markerIcon,
  shadowUrl: markerShadow.src || markerShadow,
});


export default function ReptilePage() {
  const { id } = useRouter().query;

  const [reptile, setReptile] = useState(null);
  const [images, setImages] = useState([]);
  const [taxonId, setTaxonId] = useState(null);
  const [markers, setMarkers] = useState([]);
  const [rangeData, setRangeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch reptile data from Flask API
  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetch(`http://localhost:5000/api/reptile/${id}`)
      .then(res => res.json())
      .then(data => {
        setReptile(data);
        setLoading(false);
      })
      .catch(err => {
        setError('Error fetching reptile data');
        setLoading(false);
        console.error(err);
      });
  }, [id]);

  // Fetch iNaturalist images and taxon ID
  useEffect(() => {
    if (!id) return;
    fetch(`http://localhost:5000/images?species_id=${id}`)
      .then(res => res.json())
      .then(data => {
        setImages(data.images || []);
        setTaxonId(data.taxon_id);
      })
      .catch(err => {
        console.error('Error fetching iNaturalist data', err);
      });
  }, [id]);

  // Fetch map markers
  useEffect(() => {
    if (!taxonId) return;
    async function fetchObservations() {
      const res = await fetch(`https://api.inaturalist.org/v1/observations?taxon_id=${taxonId}&per_page=50`);
      const data = await res.json();
      const points = data.results
        .filter(obs => obs.geojson && obs.geojson.coordinates)
        .map(obs => ({
          lat: obs.geojson.coordinates[1],
          lon: obs.geojson.coordinates[0],
          name: obs.species_guess,
          url: obs.uri
        }));
      setMarkers(points);
    }
    fetchObservations();
  }, [taxonId]);

  // Fetch range GeoJSON, Note that many species don't have range data so it'll log if it does and then just drop pins if there is no range
  useEffect(() => {
    if (!taxonId) return;
    fetch(`https://api.inaturalist.org/v1/taxa/${taxonId}`)
      .then(res => res.json())
      .then(data => {
        console.log('iNat taxon data:', data);
        const geojson = data.results[0].range_geojson;
        if (geojson) {
          setRangeData(geojson);
        } else {
          console.warn('No range data available for this taxon');
        }
      })
      .catch(err => console.error('Error fetching range data:', err));
  }, [taxonId]);
  
  const displayValue = (value) => {
    if (!value || value.length === 0) return 'N/A';
    if (Array.isArray(value)) return value.join(', ');
    return String(value);
  };
  

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!reptile) return <p>No reptile found.</p>;

  return (
    <div style={containerStyle}>
      <h1 style={headerStyle}>{displayValue(reptile.genus)} {displayValue(reptile.species)}</h1>

      <div style={infoStyle}><strong>Common Names:</strong> {displayValue(reptile.common_names)}</div>
      <div style={infoStyle}><strong>Higher Taxa:</strong> {displayValue(reptile.higher_taxa)}</div>
      <div style={infoStyle}><strong>Authority:</strong> {displayValue(reptile.authority)}</div>
      <div style={infoStyle}><strong>Year:</strong> {displayValue(reptile.year)}</div>
      <div style={infoStyle}><strong>Valid:</strong> {displayValue(reptile.valid)}</div>
      <div style={infoStyle}><strong>Synonyms:</strong> {displayValue(reptile.synonyms)}</div>
      <div style={infoStyle}><strong>Distribution:</strong> {displayValue(reptile.distribution_raw)}</div>
      <div style={infoStyle}><strong>Type Specimens:</strong> {displayValue(reptile.type_specimens)}</div>
      <div style={infoStyle}><strong>Media Links:</strong> {displayValue(reptile.media_links)}</div>
      <div style={infoStyle}><strong>Comments:</strong> {displayValue(reptile.notes)}</div>
      <div style={infoStyle}><strong>Etymology:</strong> {displayValue(reptile.etymology)}</div>
      <div style={infoStyle}><strong>Reproduction:</strong> {displayValue(reptile.reproduction)}</div>

      <h2>iNaturalist Photos</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {images.map((url, index) => (
          <img key={index} src={url} alt={`Observation ${index + 1}`} style={{ height: '150px', margin: '10px' }} />
        ))}
      </div>

      <h2>Observations Courtesy of iNaturalist</h2>
      <MapContainer center={[0, 0]} zoom={2} style={{ height: '600px', width: '100%' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {rangeData && (
          <GeoJSON data={rangeData} style={{ color: 'lime', weight: 2 }} />
        )}


{markers.map((marker, index) => (
  <CircleMarker
    key={index}
    center={[marker.lat, marker.lon]}
    radius={4}
    color="red"
    fillColor="red"
    fillOpacity={1}
  >
    <Popup>
      <a href={marker.url} target="_blank" rel="noopener noreferrer">{marker.name}</a>
    </Popup>
  </CircleMarker>
))}

      </MapContainer>
    </div>
  );
}

const containerStyle = {
  padding: '2rem',
  fontFamily: 'sans-serif',
  backgroundColor: 'black',
  color: 'white',
  minHeight: '100vh'
};

const headerStyle = {
  fontSize: '2rem',
  marginBottom: '1rem',
  color: 'white'
};

const infoStyle = {
  marginBottom: '0.5rem',
  fontSize: '1rem'
};
