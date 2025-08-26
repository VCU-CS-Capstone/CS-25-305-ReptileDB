import Image from 'next/image';
import { useEffect, useState } from 'react';

export default function LizardPage() {
  const [lizardData, setLizardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {
    async function fetchLizardData() {
      try {
        const response = await fetch('http://192.168.1.109:5000/showcase/common_name/Nile Monitor');
        if (!response.ok) {
          throw new Error('Reptile not found' +response.status);
        }
        const data = await response.json();
        setLizardData(data[0]);  
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    }

    fetchLizardData();
  }, []);  // Empty dependency array

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px' }}>
      <h1>Displaying data for {lizardData.common_names || 'Unknown'}</h1>
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <div>
          <h2>Common Names: {lizardData.common_names || 'Unknown'}</h2>
          <p><strong>Scientific Name:</strong> <em>{lizardData.genus} {lizardData.species}</em></p>
          <p><strong>Higher Taxa:</strong> <em>Varanidae, Platynota, Varanoidea, Anguimorpha, Sauria, Squamata (lizards)</em></p>
          
          <p><strong>Distribution:</strong> {'Republic of South Africa (Eastern Cape etc.), Swaziland, Namibia, Botswana, Tanzania, Mozambique, Zimbabwe, Zambia, Angola, Malawi, Tanzania, Gabon, W/N/S Democratic Republic of the Congo (Zaire), Kenya, Uganda, Cameroon, Central African Republic, Ethiopia, Eritrea, Somalia, Sudan (Jumhūriyyat), Republic of South Sudan (RSS), Chad, Egypt, Liberia, Ivory Coast, Ghana, Togo, Benin, Burkina Faso, Niger, Nigeria, Mali, Mauritania, Senegal, Gambia (HÅKANSSON 1981), Guinea (Conakry), Equatorial Guinea'}</p>
          <p><strong>Diagnosis:</strong> {'Diagnosis: (1) Large lizard up to approximately 80 cm SVL and about 200 cm total length. (2) Tail laterally compressed with a low dorsal crest. (3)'}</p>
          <p> {'A total of 136 to 183 scales around the midbody. (4) Basic dorsal color of adults gray brown to olive-brown with light yellow ocelli and bands on head, back, limbs, and tail. Belly and throat are paler, with black bars. (5) V. niloticus is characterized by six to nine crossbands or rows of yellow ocelli on the back between foreand hind limbs, whereas V. ornatus normally has only five bands.'}</p>
          <p><strong>Comments:</strong> {'Synonymy: The status of V. ornatus remains somewhat contentious. Böhme and Ziegler (1997) elevated V. ornatus to full species level based on differing pigmentation patterns, tongue coloration, genital morphology, and slight differences in scale counts. However, Dowell et al. (2015) synonymized V. ornatus with V. niloticus as both are genetically indistinguishable and because morphological characters largely overlap. However, Dowell et al. found distinct clades within V. niloticus across its huge range. SCHMIDT’s Varanus niloticus might represent both V. niloticus (specimens from savanna localities) and V. ornatus (specimens from rain forest localities). ICZN opinion 540 rejected Lacerta monitor LINNAEUS 1758'}</p>
          <p><strong>Diet:</strong> {lizardData.types || 'Unknown'}</p>
          <p><strong>More Info:</strong> <a href={lizardData.links} target="_blank" rel="noopener noreferrer">Click here</a></p>
        </div>
      </div>
    </div>
  );
}

//<p><strong>Distribution:</strong> {lizardData.distribution || 'Unknown'}</p>
//<p><strong>Comments:</strong> {lizardData.comments || 'No comments available'}</p>

