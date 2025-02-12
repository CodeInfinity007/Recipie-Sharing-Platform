import os
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_db_connection():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the users table if it doesn't exist
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return 'Username already exists!'
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return 'Registration successful!'

    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'

    return render_template('login.html')

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Function to fetch recipes from the database
def get_recipes():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return [dict(recipe) for recipe in recipes]

# Route to display all recipes
@app.route('/')
def home():
    recipes = get_recipes()
    return render_template('index.html', recipes=recipes)

# Route to handle search requests
@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE title LIKE ?", ('%' + search_query + '%',))
    search_results = cursor.fetchall()
    search_results = [dict(r) for r in search_results]
    conn.close()
    return render_template('search_results.html', search_results=search_results, query=search_query)

# Route to display recipe details
@app.route('/view_recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
    recipe_row = cursor.fetchone()
    recipe = dict(recipe_row)
    conn.close()
    return render_template('recipe_details.html', recipe=recipe)



@app.route('/favorites/<int:user_id>')
def favorites(user_id):
    print(f"user_id = {user_id}")
    # Retrieve favorite recipes for the user from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM favorite_recipes WHERE user_id = ?', (user_id,))
    favorite_recipes = cursor.fetchall()
    conn.close()
    

    return render_template('favorites.html', user_id=user_id, favorite_recipes=favorite_recipes)


if __name__ == '__main__':
    create_users_table()
    app.run(debug=True)
