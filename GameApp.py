import streamlit as st
import pandas as pd
import re

# Function to clean text and keep only English characters
def clean_text(text):
    text = str(text)
    clean = re.sub(r'[^a-zA-Z, ]', '', text)
    return clean.strip()

#load data from a CSV file
def load_data(file_path):
    return pd.read_csv(file_path)

# get unique mechanics from the data
def get_unique_mechanics(data, mechanics_column):
    mechanics = []
    for mechanics_list in data[mechanics_column]:
        cleaned_mechanics = clean_text(mechanics_list)
        for mechanic in cleaned_mechanics.split(","):
            mechanic = mechanic.strip()
            if mechanic not in mechanics:
                mechanics.append(mechanic)
    return sorted(mechanics)

#search games by mechanic after selecting
def search_games_by_mechanic(data, mechanics_column, selected_mechanic):
    filtered_games = []
    for i in range(len(data)):
        mechanics_list = data[mechanics_column][i]
        cleaned_mechanics = clean_text(mechanics_list)
        mechanics_split = cleaned_mechanics.split(",")
        for mechanic in mechanics_split:
            if mechanic.strip() == selected_mechanic:
                game = {
                    "name": data["primary"][i],
                    "image": data["image"][i],
                    "description": data["description"][i]
                }
                filtered_games.append(game)
                break
    return filtered_games

# Starting LAYOUT
st.set_page_config(layout="wide")
st.title("Find the Game That Fits Your Play Style")

# Load the dataset
games_data = load_data("games_detailed_info.csv")
mechanics_column = "mechanics"

# Get the list of unique mechanics to dropdown
unique_mechanics = get_unique_mechanics(games_data, mechanics_column)
selected_mechanic = st.selectbox("What mechanic are YOU Looking For?:", unique_mechanics)

# Search and display games with the selected mechanic
if selected_mechanic:
    filtered_games = search_games_by_mechanic(games_data, mechanics_column, selected_mechanic)

    if len(filtered_games) > 0:
        num_columns = 5
        columns = st.columns(num_columns)

        for i in range(min(len(filtered_games), 5)):
            game = filtered_games[i]
            col = columns[i % num_columns]
            with col:
                st.write(f"**{game['name']}**")
                st.image(game["image"], use_column_width=True)
                if st.button(f"More about {game['name']}", key=f"button_{i}"):
                    st.write(game["description"])
    else:
        st.write(f"No games found with the mechanic '{selected_mechanic}'.")
