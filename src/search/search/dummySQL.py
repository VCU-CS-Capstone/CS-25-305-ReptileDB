#Creating a fake db to test endpoints with

import sqlite3

conn = sqlite3.connect('dummyreptile.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS taxonomy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        higher_taxa TEXT,
        genus TEXT,
        species TEXT,
        author TEXT,
        year INTEGER,
        parentheses TEXT,
        species_author TEXT,
        synonyms TEXT,
        subspecies TEXT,
        common_names TEXT,
        distribution TEXT,
        comments TEXT,
        types TEXT,
        links TEXT,
        reference_numbers TEXT
    );
''')


fake_reptiles = [
    ('Reptilia, Squamata, Varanidae', 'Varanus', 'komodoensis', 'Owen', 1856, '(', 'Varanus komodoensis Owen 1856', 'Komodo dragon', '', '', 'Indonesia', 'Large lizard, endangered', 'Carnivorous', 'https://en.wikipedia.org/wiki/Komodo_dragon', 'Ref-001'),
    ('Reptilia, Squamata, Varanidae', 'Varanus', 'niloticus', 'Linnaeus', 1766, '(', 'Varanus niloticus Linnaeus 1766', 'Nile monitor', '', 'Nile Monitor', 'Africa', 'Common species, aggressive', 'Omnivorous', 'https://en.wikipedia.org/wiki/Nile_monitor', 'Ref-002'),
    ('Reptilia, Testudines, Testudinidae', 'Chelonoidis', 'nigra', 'Gray', 1831, '(', 'Chelonoidis nigra Gray 1831', 'Galápagos tortoise', '', '', 'Galápagos Islands', 'Endangered species', 'Herbivorous', 'https://en.wikipedia.org/wiki/Galápagos_tortoise', 'Ref-003'),
    ('Reptilia, Crocodylia, Crocodylidae', 'Crocodylus', 'porosus', 'Schneider', 1801, '(', 'Crocodylus porosus Schneider 1801', 'Saltwater crocodile', '', '', 'Southeast Asia, Australia', 'Largest living reptile', 'Carnivorous', 'https://en.wikipedia.org/wiki/Saltwater_crocodile', 'Ref-004'),
    ('Reptilia, Squamata, Iguanidae', 'Iguana', 'iguana', 'Linnaeus', 1758, '(', 'Iguana iguana Linnaeus 1758', 'Green iguana', 'Green iguana', 'Green iguana', 'Central and South America', 'Popular pet', 'Herbivorous', 'https://en.wikipedia.org/wiki/Green_iguana', 'Ref-005')
]


cursor.executemany('''
    INSERT INTO taxonomy (
        higher_taxa, genus, species, author, year, parentheses, species_author, 
        synonyms, subspecies, common_names, distribution, comments, types, links, reference_numbers
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
''', fake_reptiles)

conn.commit()
conn.close()

print("You've Got Fake Reptiles")
