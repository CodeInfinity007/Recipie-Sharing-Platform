import sqlite3
import csv

# Function to create the SQLite database
def create_database():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        title TEXT,
        ingredients TEXT,
        instructions TEXT,
        author TEXT,
        category TEXT,
        prep_time INTEGER,
        cook_time INTEGER,
        total_time INTEGER,
        servings INTEGER, 
        cuisine TEXT, 
        diet TEXT,
        url TEXT
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()
    print("Database created successfully!")

def create_users_table():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        usr_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        favorite_recipes TEXT  -- Storing favorite recipes as JSON serialized string
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()
    print("Users table created successfully!")

# Function to insert a new user into the database
def insert_user(username, password, favorite_recipes=[]):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, favorite_recipes) VALUES (?, ?, ?)",
                   (username, password, json.dumps(favorite_recipes)))
    conn.commit()
    conn.close()
    print("User inserted successfully!")


# Function to import data from CSV file into database
def import_csv(filename):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for index, row in enumerate(csv_reader):
            id = index
            title = row['RecipeName']
            ingredients = row['TranslatedIngredients']
            instructions = row['TranslatedInstructions']
            cuisine = row['Cuisine']
            diet = row['Diet']
            url = row['URL']
            author = ''
            category = row['Course']
            prep_time = int(row['PrepTimeInMins']) if row['PrepTimeInMins'] else 0
            cook_time = int(row['CookTimeInMins']) if row['CookTimeInMins'] else 0
            total_time = int(row['TotalTimeInMins']) if row['TotalTimeInMins'] else 0
            servings = int(row['Servings']) if row['Servings'] else 0

            cursor.execute('INSERT INTO recipes (id, title, ingredients, instructions, author, category, prep_time, cook_time, total_time, servings, cuisine, diet, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (id, title, ingredients, instructions, author, category, prep_time, cook_time, total_time, servings, cuisine, diet, url))

    conn.commit()
    conn.close()
    print("Data imported successfully!")

if __name__ == '__main__':
    create_database()
    import_csv('data.csv')
    create_users_table()
    