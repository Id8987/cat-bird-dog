from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
from PIL import Image
import os
import io
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.models import load_model  # Ajout important

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Chargement du modèle TensorFlow
model = load_model('model.h5')  # Chemin vers votre modèle
classes = ['Oiseau', 'Chat', 'Chien']
# Modèle Utilisateur
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
# Création des tables
with app.app_context():
    db.create_all()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Fonctions utilitaires
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def add_noise(image, epsilon):
    img_array = np.array(image)
    noise = np.random.normal(0, epsilon * 50, img_array.shape)
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img)

# Routes d'authentification
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Identifiants invalides')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Nom d\'utilisateur déjà pris')
            return redirect(url_for('register'))
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Routes principales
@app.route('/')
def index():
    return render_template('index.html')

# Ajoutez cette fonction AVANT la route @app.route('/predict')
def preprocess_image(image_path):
    # Ouvrir et convertir en RGB
    img = Image.open(image_path).convert('RGB')

    # Redimensionnement pour EfficientNet
    img = img.resize((224, 224))

    # Conversion en array et prétraitement
    img_array = np.array(img)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)

    # Ajout de la dimension batch
    img_array = np.expand_dims(img_array, axis=0)

    return img_array



@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if 'file' not in request.files:
        return render_template('index.html', error="Aucun fichier uploadé")

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="Aucun fichier sélectionné")

    if file and allowed_file(file.filename):
        # Sauvegarder l'image temporairement
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Prétraitement et prédiction
        processed_image = preprocess_image(file_path)
        predictions = model.predict(processed_image)[0]

        # Formater les résultats
        results = {classes[i]: f"{prob * 100:.2f}%" for i, prob in enumerate(predictions)}
        predicted_class = classes[np.argmax(predictions)]

        return render_template('result.html',
                               image_path=file_path,
                               results=results,
                               predicted_class=predicted_class)

    return render_template('index.html', error="Format de fichier non supporté")

# Route pour le bruitage - BIEN ALIGNÉE À GAUCHE
@app.route('/noise', methods=['GET', 'POST'])
@login_required
def add_image_noise():
    if request.method == 'POST':
        epsilon = float(request.form.get('epsilon', 0.5))
        file = request.files['file']
        if file and allowed_file(file.filename):
            img = Image.open(file.stream)
            noisy_img = add_noise(img, epsilon)

            # Sauvegarde et affichage
            img_io = io.BytesIO()
            noisy_img.save(img_io, 'PNG')
            img_io.seek(0)

            return send_file(img_io, mimetype='image/png', download_name='noisy_image.png')

    return render_template('noise.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)