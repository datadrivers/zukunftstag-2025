import streamlit as st
import random
import numpy as np
import pandas as pd
import altair as alt

# Initialisierung des Session States
if 'tries_left' not in st.session_state:
    st.session_state.tries_left = 200

if 'bandit_counts' not in st.session_state:
    st.session_state.bandit_counts = {1: 0, 2: 0, 3: 0, 4: 0}

if 'bandit_rewards' not in st.session_state:
    st.session_state.bandit_rewards = {1: [], 2: [], 3: [], 4: []}

if 'history' not in st.session_state:
    st.session_state.history = []  # Speichert (Bandit, Reward) Tupel für die Historie

# Mittelwerte der Banditen (geheim für den Nutzer)
bandit_means = {1: 3, 2: 6, 3: 5, 4: 4}

# App-Titel
st.title("Multi-Armed-Bandit Simulation")
st.write("Wähle einen Banditen und sieh, welche Belohnung du bekommst!")


# Funktion zum Spielen eines Banditen
def play_bandit(bandit_id):
    if st.session_state.tries_left <= 0:
        return None

    # Mittelwert des gewählten Banditen
    mean = bandit_means[bandit_id]

    # Generiere zufällige Belohnung zwischen 1 und 10
    # mit einer diskreten Verteilung um den Mittelwert
    possible_rewards = list(range(1, 11))
    # Erstelle Wahrscheinlichkeiten, die näher am Mittelwert höher sind
    probs = [1 / (1 + abs(r - mean)) for r in possible_rewards]
    # Normalisiere Wahrscheinlichkeiten
    probs = [p / sum(probs) for p in probs]

    reward = np.random.choice(possible_rewards, p=probs)

    # Aktualisiere Session State
    st.session_state.tries_left -= 1
    st.session_state.bandit_counts[bandit_id] += 1
    st.session_state.bandit_rewards[bandit_id].append(reward)
    st.session_state.history.append((bandit_id, reward))

    return reward


# Zeige verbleibende Versuche
st.header(f"Verbleibende Versuche: {st.session_state.tries_left}")

# Buttons für die Banditen
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Bandit 1 spielen", key="bandit1", disabled=st.session_state.tries_left <= 0):
        reward = play_bandit(1)
        if reward:
            st.success(f"Belohnung: {reward}")

with col2:
    if st.button("Bandit 2 spielen", key="bandit2", disabled=st.session_state.tries_left <= 0):
        reward = play_bandit(2)
        if reward:
            st.success(f"Belohnung: {reward}")

with col3:
    if st.button("Bandit 3 spielen", key="bandit3", disabled=st.session_state.tries_left <= 0):
        reward = play_bandit(3)
        if reward:
            st.success(f"Belohnung: {reward}")

with col4:
    if st.button("Bandit 4 spielen", key="bandit4", disabled=st.session_state.tries_left <= 0):
        reward = play_bandit(4)
        if reward:
            st.success(f"Belohnung: {reward}")

# Zeige Statistiken
st.header("Bandit-Statistiken")

stats_data = []
for bandit_id in range(1, 5):
    count = st.session_state.bandit_counts[bandit_id]
    rewards = st.session_state.bandit_rewards[bandit_id]
    avg_reward = sum(rewards) / count if count > 0 else 0

    stats_data.append({
        "Bandit": f"Bandit {bandit_id}",
        "Anzahl Spiele": count,
        "Durchschnittliche Belohnung": round(avg_reward, 2)
    })

# Statistik-Tabelle
stats_df = pd.DataFrame(stats_data)
st.table(stats_df)

# Visualisierung der durchschnittlichen Belohnungen
if any(st.session_state.bandit_counts.values()):
    st.subheader("Durchschnittliche Belohnungen pro Bandit")

    # Erstelle Dataframe für das Chart
    chart_data = pd.DataFrame({
        'Bandit': [f"Bandit {i}" for i in range(1, 5)],
        'Durchschnittliche Belohnung': [sum(st.session_state.bandit_rewards[i]) / st.session_state.bandit_counts[i]
                                        if st.session_state.bandit_counts[i] > 0 else 0 for i in range(1, 5)]
    })

    # Erstelle Balkendiagramm
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Bandit:N'),
        y=alt.Y('Durchschnittliche Belohnung:Q', scale=alt.Scale(domain=[0, 10])),
        color=alt.Color('Bandit:N', scale=alt.Scale(scheme='category10')),
        tooltip=['Bandit', 'Durchschnittliche Belohnung']
    ).properties(
        title='Durchschnittliche Belohnungen pro Bandit'
    )

    st.altair_chart(chart, use_container_width=True)

    # Visualisierung der Spielanzahl
    st.subheader("Anzahl der Spiele pro Bandit")

    counts_data = pd.DataFrame({
        'Bandit': [f"Bandit {i}" for i in range(1, 5)],
        'Anzahl': [st.session_state.bandit_counts[i] for i in range(1, 5)]
    })

    counts_chart = alt.Chart(counts_data).mark_bar().encode(
        x=alt.X('Bandit:N'),
        y=alt.Y('Anzahl:Q'),
        color=alt.Color('Bandit:N', scale=alt.Scale(scheme='category10')),
        tooltip=['Bandit', 'Anzahl']
    ).properties(
        title='Anzahl der Spiele pro Bandit'
    )

    st.altair_chart(counts_chart, use_container_width=True)

    # Einfache Darstellung der erhaltenen Belohnungen als Zahlenfolge
    st.subheader("Erhaltene Belohnungen pro Bandit")

    for bandit_id in range(1, 5):
        rewards = st.session_state.bandit_rewards[bandit_id]
        if rewards:  # Nur anzeigen, wenn es Belohnungen gibt
            rewards_str = ", ".join(map(str, rewards))
            st.write(f"**Bandit {bandit_id}:** {rewards_str}")
        else:
            st.write(f"**Bandit {bandit_id}:** Noch keine Spiele")

# Gesamtergebnis (nur anzeigen wenn Spiele gespielt wurden)
if sum(st.session_state.bandit_counts.values()) > 0:
    total_reward = sum([sum(rewards) for rewards in st.session_state.bandit_rewards.values()])
    st.header(f"Gesamtbelohnung: {total_reward}")

# Reset-Button
if st.button("Simulation zurücksetzen"):
    st.session_state.tries_left = 200
    st.session_state.bandit_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    st.session_state.bandit_rewards = {1: [], 2: [], 3: [], 4: []}
    st.session_state.history = []
    st.experimental_rerun()