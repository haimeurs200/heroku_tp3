import streamlit as st
import pandas as pd

# import matplotlib.pyplot as plt
import plotly.express as px
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data, moyenne_consommation_par_heure
import logging
import os
import glob


logging.basicConfig(level=logging.INFO)


LAG_N_DAYS: int = 7

# * INIT REPO FOR DATA
os.makedirs("data/raw/", exist_ok=True)
os.makedirs("data/interim/", exist_ok=True)

# * remove outdated json files
for file_path in glob.glob("data/raw/*json"):
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        logging.warning(e)

# plt.switch_backend("TkAgg")

# Title for your app
st.title("Data Visualization App")


# Load data from CSV
@st.cache_data(
    ttl=15 * 60
)  # This decorator caches the data to prevent reloading on every interaction.
def load_data(lag_days: int):
    load_data_from_lag_to_today(lag_days)
    main_process()
    data = pd.read_csv(
        fic_export_data, parse_dates=[col_date]
    )  # Adjust 'DateColumn' to your date column name*
    return data


# Assuming your CSV is named 'data.csv' and is in the same directory as your app.py
df = load_data(LAG_N_DAYS)

# Creating a line chart
st.subheader("Line Chart of Numerical Data Over Time")

# Select the numerical column to plot
# This lets the user select a column if there are multiple numerical columns available
# numerical_column = st.selectbox('Select the column to visualize:', df.select_dtypes(include=['float', 'int']).columns)
numerical_column = col_donnees

# ! Matplotlib - Create the plot
# fig, ax = plt.subplots()
# ax.plot(df[col_date], df[numerical_column])  # Adjust 'DateColumn' to your date column name
# ax.set_xlabel('Time')
# ax.set_ylabel(numerical_column)
# ax.set_title(f'Time Series Plot of {numerical_column}')
# # Display the plot
# st.pyplot(fig)

# ! Plotly
# Create interactive line chart using Plotly
fig = px.line(df, x=col_date, y=col_donnees, title="Consommation en fonction du temps")
st.plotly_chart(fig)




df = pd.DataFrame({
    'heure': range(24),
    'consommation': [10, 20, 15, 30, 25, 20, 35, 40, 45, 30, 25, 20,
                     20, 25, 30, 35, 40, 45, 40, 35, 30, 25, 20, 15]
})

# Calculer la moyenne de la consommation par heure
moyennes_par_heure = moyenne_consommation_par_heure(df['consommation'])

# Vérifier la longueur de la liste des moyennes par heure
if len(moyennes_par_heure) != 24:
    raise ValueError("La liste des moyennes par heure ne contient pas 24 éléments. Assurez-vous que la fonction moyenne_consommation_par_heure calcule correctement la moyenne pour chaque heure de la journée.")

# Créer un DataFrame pour les moyennes par heure
df_moyennes = pd.DataFrame({'heure': range(24), 'moyenne_consommation': moyennes_par_heure})

# Tracer le graphique
fig = px.bar(df_moyennes, x='heure', y='moyenne_consommation', title="Moyenne de la consommation par heure")
st.plotly_chart(fig)