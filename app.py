import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv  

# Carrega as variáveis do .env
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para o Fórum
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        new_post = Post(content=request.form['content'])
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('forum'))
    
    posts = Post.query.all()
    return render_template('forum.html', posts=posts)

@app.route('/encouragement')
def encouragement():
    return render_template('encouragement.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['userInput']  
    response_text = get_advice()  
    return response_text  

def get_advice():
    url = "https://api.adviceslip.com/advice"  # URL da API para obter um conselho
    response = requests.get(url)
    
    if response.status_code == 200:
        advice_data = response.json()
        return advice_data['slip']['advice']  # Retorna o texto do conselho
    else:
        return "Desculpe, não consegui obter um conselho."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria o banco de dados se não existir
    app.run(debug=True)