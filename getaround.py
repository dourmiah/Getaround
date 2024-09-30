import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


dataset = pd.read_excel("get_around_delay_analysis.xlsx")

st.title("GetAround Dashboard")
st.write('Données : ')
st.dataframe(dataset)

##########################################################################
#
#  Visualisation du pourcentage de retards de restituion 
#
##########################################################################

# Filtrage des lignes non-nulles pour delay_at_checkout_in_minutes
dataset_notnull = dataset.dropna(subset=['delay_at_checkout_in_minutes'])

# Calculs pour les retards
nb_total_lines = dataset_notnull['delay_at_checkout_in_minutes'].shape[0]
nb_late_checkout = dataset_notnull[dataset_notnull["delay_at_checkout_in_minutes"] > 0].shape[0]
nb_ontime_checkout = nb_total_lines - nb_late_checkout
percentage_late_checkout = (nb_late_checkout / nb_total_lines) * 100

# Affichage du pourcentage dans l'application Streamlit
st.title("Retours véhicules en retard")
st.write(f"Pourcentage des restitutions en retard : {round(percentage_late_checkout)} %")

# Données pour le graphique
labels = ["Retour véhicule en retard", "Retour véhicule à l'heure"]
sizes = [nb_late_checkout, nb_ontime_checkout]

# Graphique de type camembert
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF7043'])
ax.axis('equal')  # Assure que le graphique est bien circulaire
plt.title("Répartition des retours véhicules en retard / à l'heure")


st.pyplot(fig)

##########################################################################
#
#  Visualisation des retards de restituion en heures
#
##########################################################################

dataset_notnull['delay_at_checkout_in_hours'] = round(dataset_notnull['delay_at_checkout_in_minutes'] / 60, 2)

# Filtrer les retards compris entre 0 et moins de 12 heures
dataset_late_hour = dataset_notnull[(dataset_notnull['delay_at_checkout_in_hours'] >= 0) &
                                    (dataset_notnull['delay_at_checkout_in_hours'] < 12)]


st.title("Histogramme des retards de restitution (en heures)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(dataset_late_hour['delay_at_checkout_in_hours'], bins=30, edgecolor='black')


ax.set_xlabel('Retard à la restitution (en heures)')
ax.set_ylabel('Nombre de locations')
ax.set_title('Distribution des retards de restitution par heure')


ax.set_xticks(np.arange(0, dataset_late_hour['delay_at_checkout_in_hours'].max() + 1, 1))


st.pyplot(fig)

st.write()
st.write("La majorité des retards sont inférieurs à 2 heures")


dataset_late_hour['time_delta_with_previous_rental_in_hours'] = round(dataset_late_hour['time_delta_with_previous_rental_in_minutes'] / 60, 2)
dataset_late_hour = dataset_late_hour[dataset_late_hour['time_delta_with_previous_rental_in_hours'] > 0]
dataset_late_hour['Percentage_late_checkout_vs_time_delta'] = dataset_late_hour.apply(lambda row: round((dataset_late_hour['delay_at_checkout_in_hours'] > row['time_delta_with_previous_rental_in_hours']).mean() * 100, 2), axis=1)

plt.figure(figsize=(10, 6))

# Création du bar plot avec seaborn
sns.pointplot(x='time_delta_with_previous_rental_in_hours', y='Percentage_late_checkout_vs_time_delta', data=dataset_late_hour)

# Ajouter un titre et des labels aux axes
plt.title('Impact variation delta temps sur les retours en retard')
plt.xlabel('Delta temps avec location précédente (heures)')
plt.ylabel('Pourcentage retours en retard (%)')

# Rotation des labels sur l'axe x si nécessaire (par exemple, pour éviter le chevauchement)
plt.xticks(rotation=45)

# Affichage du graphique
plt.show()

##########################################################################
#
#  Visualisation de l'impact du delta temps sur les retours en retard
#
##########################################################################

dataset_late_hour['time_delta_with_previous_rental_in_hours'] = round(dataset_late_hour['time_delta_with_previous_rental_in_minutes'] / 60, 2)
dataset_late_hour = dataset_late_hour[dataset_late_hour['time_delta_with_previous_rental_in_hours'] > 0]

# Calcul du pourcentage des retours en retard vs le delta de temps avec la location précédente
dataset_late_hour['Percentage_late_checkout_vs_time_delta'] = dataset_late_hour.apply(
    lambda row: round((dataset_late_hour['delay_at_checkout_in_hours'] > row['time_delta_with_previous_rental_in_hours']).mean() * 100, 2),
    axis=1
)

# Création du graphique avec seaborn
st.title("Impact du delta temps sur les retours en retard")
fig, ax = plt.subplots(figsize=(10, 6))
sns.pointplot(x='time_delta_with_previous_rental_in_hours', y='Percentage_late_checkout_vs_time_delta', data=dataset_late_hour, ax=ax)

# Ajouter un titre et des labels
ax.set_title('Impact variation delta temps sur les retours en retard')
ax.set_xlabel('Delta temps avec location précédente (heures)')
ax.set_ylabel('Pourcentage retours en retard (%)')

# Rotation des labels sur l'axe x si nécessaire
plt.xticks(rotation=45)

# Afficher le graphique dans Streamlit
st.pyplot(fig)

st.write()
st.write("On pourrait par exemple envisager un delta de 3 heures. Ce qui amènerait le taux de restitution de véhibule en retard à 10 % ")