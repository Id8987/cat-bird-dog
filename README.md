# 🖼️ AI Image Classifier

Une application web intelligente pour classer des images (Oiseaux/Chats/Chiens) avec des fonctionnalités avancées d'IA et de traitement d'image.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green)](https://flask.palletsprojects.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.1-orange)](https://tensorflow.org)

## ✨ Fonctionnalités

- **Classification d'images** (Oiseau/Chat/Chien) avec EfficientNet
- Interface utilisateur moderne avec **Bootstrap 5**
- Système complet d'**authentification** utilisateur
- **Bruitage paramétrable** des images (ε entre 0 et 1)
- Visualisation des probabilités de prédiction
- Prévisualisation des images avant upload
- Historique des analyses dans l'interface

## 🚀 Installation

### Prérequis
- Python 3.10+
- pip
- Git

### Étapes d'installation

1. Cloner le dépôt :
```bash
git clone https://github.com/Id8987/cat-bird-dog.git
cd votre-repo
```
2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Installer les dépendances :
```bash
pip install -r requirements.txt
```
4. Lancer l'application :
```bash
flask run
python -m flask run  # Windows
```
5. Ouvrir l'application dans votre navigateur : [http://localhost:5000](http://localhost:5000)
6. Pour arrêter l'application, appuyez sur `Ctrl+C` dans le terminal.