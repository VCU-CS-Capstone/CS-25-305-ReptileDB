
//To connect to the DB

import path from 'path';
import Database from 'better-sqlite3';

// Absolute path to avoid path issues when deployed or using different working directories
const dbPath = path.join(process.cwd(), 'lib', 'reptile_database.db');

const db = new Database(dbPath);
export default db;
