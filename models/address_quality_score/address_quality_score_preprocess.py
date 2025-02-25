# preprocessing.py
import re
from nltk.stem import LancasterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import fasttext
import pandas as pd
import nltk

# Download stopwords
nltk.download("stopwords")

# Pre-processing functions


# 1. Combine features into a single text feature
def combine_features(row):
    combined = " "
    combined += row["address"] + " " if row["address"] != "" else ""
    combined += row["address_line1"] + " " if row["address_line1"] != "" else ""
    combined += row["landmark"] + " " if row["landmark"] != "" else ""
    combined += row["city"] + " " if row["city"] != "" else ""
    combined += row["state"] + " " if row["state"] != "" else ""
    return combined


# 2. Tokenizer
tokenizer = RegexpTokenizer(r"\w+")

# 3. Stopwords
stop_words = set(stopwords.words("english"))


# Function to remove stopwords from a list of tokens
def remove_stopwords(tokens):
    return [token for token in tokens if token.lower() not in stop_words]


# 4. Replace numbers with token <number>
def replace_numbers_with_token(tokens):
    return [
        (
            "<number>"
            if re.fullmatch(r"\b\d+\b|\d+[a-zA-Z]*|[a-zA-Z]+\d+", token)
            else token
        )
        for token in tokens
    ]


# 5. Stemming
lancaster_stemmer = LancasterStemmer()


def apply_lancaster_stemming(tokens):
    return [lancaster_stemmer.stem(token) for token in tokens]


# 6. Join tokens into a single string
def join_tokens(tokens):
    return " ".join(tokens)


# 7. Process and predict function
def process_and_predict(data, model_path):
    # Fill missing values
    data = data.fillna("")

    # Apply the preprocessing steps
    data["combined_features"] = data.apply(combine_features, axis=1)
    data["regexp_tokens"] = (data["combined_features"].str.lower()).apply(
        tokenizer.tokenize
    )
    data["filtered_tokens"] = data["regexp_tokens"].apply(remove_stopwords)
    data["filtered_tokens"] = data["filtered_tokens"].apply(replace_numbers_with_token)
    data["filtered_tokens"] = data["filtered_tokens"].apply(apply_lancaster_stemming)
    data["joined_tokens"] = data["filtered_tokens"].apply(join_tokens)

    # Load the trained FastText model
    model = fasttext.load_model(model_path)

    # Make predictions
    predicted_label = []
    probability = []
    for text in data["joined_tokens"]:
        label, prob = model.predict(text)
        # Clean up the label by removing "__label__" prefix
        predicted_label.append(label[0].replace("__label__", ""))
        probability.append(prob[0])

    # Add predictions to the DataFrame
    data["predicted_quality"] = predicted_label
    data["probability"] = probability

    return data
