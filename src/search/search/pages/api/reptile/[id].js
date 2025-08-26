//This API page connects to the 'pages/reptile/[id]' page to fetch the data from the db

import db from '../../../lib/db'; // this filepath works with the current setup, might need to be adjusted later

export default function handler(req, res) {
  const { id } = req.query;

  try {
    const stmt = db.prepare('SELECT * FROM species WHERE species_id = ?');
    const reptile = stmt.get(id);
 
    if (!reptile) {
      return res.status(404).json({ error: 'Reptile not found' });
    }

    res.status(200).json(reptile);
  } catch (error) {
    res.status(500).json({ error: 'Database error', details: error.message });
  }
}
