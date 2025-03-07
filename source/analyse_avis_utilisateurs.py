import os
import joblib
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Télécharger les ressources nécessaires de nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Charger le modèle et le vectoriseur
log_reg_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'logistic_regression_model.pkl')
log_reg = joblib.load(log_reg_path)

tfidf_vectorizer_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'tfidf_vectorizer.pkl')
tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)


# Initialiser le lemmatizer
lemmatizer = WordNetLemmatizer()

# Fonction de nettoyage du texte
def clean_text(text):
    # Conversion en minuscules
    text = text.lower()

    # Suppression de la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Suppression des chiffres
    text = ''.join([i for i in text if not i.isdigit()])

    # Tokenisation
    tokens = word_tokenize(text)

    # Suppression des stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatisation
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Rejoindre les tokens nettoyés en une chaîne de caractères
    cleaned_text = ' '.join(tokens)

    return cleaned_text

# Fonction de prédiction
def predict_user_reviews(uploaded_file):
    if uploaded_file is not None:
        # Lecture du fichier CSV
        print("1")
        data = pd.read_csv(uploaded_file)
        print("2")
        # Vérifier que la colonne 'user_review' existe
        if 'user_review' in data.columns:
            # Nettoyer les critiques utilisateur
            print("3")
            data['cleaned_user_review'] = data['user_review'].apply(clean_text)
            
            # Vectoriser les critiques utilisateur nettoyées
            X = tfidf_vectorizer.transform(data['cleaned_user_review'])
            
            # Faire des prédictions
            predictions = log_reg.predict(X)
            print("5")
            # Ajouter les prédictions au DataFrame
            data['predictions'] = predictions
            
            # Calculer les pourcentages de prédictions positives et négatives
            positive_percentage = (predictions == 1).mean() * 100
            negative_percentage = (predictions == 0).mean() * 100
            
            return data, positive_percentage, negative_percentage
        else:
            return None, None, None
    return None, None, None
