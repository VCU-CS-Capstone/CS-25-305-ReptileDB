import { PrismaClient } from '@prisma/client';
import Link from 'next/link';

const prisma = new PrismaClient();

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const { query } = req.query;


    try {
      const results = await prisma.item.findMany({
        where: {
          name: {
            contains: query,
            mode: 'insensitive',
          },
        },
      });
      res.status(200).json(results);
    } catch (error) {
      res.status(500).json({ error: 'Error fetching results' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}

