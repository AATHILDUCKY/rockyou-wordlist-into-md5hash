import mysql.connector
import hashlib

# Database configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'md5hash'
}

# Connect to the MySQL database
db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS wordlist (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(255) NOT NULL,
        md5_hash CHAR(32) NOT NULL
    )
''')

# Function to calculate MD5 hash
def calculate_md5(word):
    return hashlib.md5(word.encode()).hexdigest()

# Open and read the wordlist file with a different encoding
with open('rockyou_part_ct', 'r', encoding='latin-1') as file:
    words = file.read().splitlines()

# Insert words and their MD5 hashes into the database
for word in words:
    md5_hash = calculate_md5(word)
    cursor.execute('''
        INSERT INTO wordlist (word, md5_hash) VALUES (%s, %s)
    ''', (word, md5_hash))

# Commit the transaction
db_connection.commit()

# Close the cursor and connection
cursor.close()
db_connection.close()

print("Wordlist has been successfully added to the database.")
