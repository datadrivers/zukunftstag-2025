import streamlit as st
import random
import pandas as pd
import altair as alt

# Initialisierung des Session States
if 'total_rolls' not in st.session_state:
    st.session_state.total_rolls = 0

if 'dice_counts' not in st.session_state:
    # Dictionary für die Anzahl jeder Augenzahl (1-6)
    st.session_state.dice_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

# App-Titel
st.title("Würfel-Simulation")
st.write("Klicke auf den Button, um den Würfel zu werfen!")


# Funktion für den Würfelwurf
def roll_dice():
    st.session_state.total_rolls += 1
    result = random.randint(1, 6)
    st.session_state.dice_counts[result] += 1
    return result


# Button zum Werfen des Würfels
if st.button("Würfel werfen"):
    result = roll_dice()
    st.success(f"Ergebnis: {result}")

    # Optional: Würfelbild anzeigen
    dice_images = {
        1: "⚀",
        2: "⚁",
        3: "⚂",
        4: "⚃",
        5: "⚄",
        6: "⚅"
    }
    st.markdown(f"<h1 style='text-align: center;'>{dice_images[result]}</h1>", unsafe_allow_html=True)

# Statistik anzeigen
st.subheader("Statistik")
st.write(f"Gesamtanzahl der Würfe: {st.session_state.total_rolls}")

# Einzelwerte anzeigen
for number in range(1, 7):
    count = st.session_state.dice_counts[number]
    percentage = (count / st.session_state.total_rolls * 100) if st.session_state.total_rolls > 0 else 0
    st.write(f"Würfelzahl {number}: {count} Mal ({percentage:.1f}%)")

# Visualisierung mit einem Balkendiagramm
if st.session_state.total_rolls > 0:
    st.subheader("Verteilung")

    # Daten vorbereiten
    chart_data = pd.DataFrame({
        'Würfelzahl': list(st.session_state.dice_counts.keys()),
        'Anzahl': list(st.session_state.dice_counts.values()),
        'Prozent': [count / st.session_state.total_rolls * 100 for count in st.session_state.dice_counts.values()]
    })

    # Balkendiagramm erstellen
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Würfelzahl:O', title='Würfelzahl'),
        y=alt.Y('Anzahl:Q', title='Häufigkeit'),
        color=alt.Color('Würfelzahl:N', scale=alt.Scale(scheme='category10')),
        tooltip=['Würfelzahl', 'Anzahl', 'Prozent']
    ).properties(
        title='Würfelergebnisse'
    )

    st.altair_chart(chart, use_container_width=True)

# Reset-Button
if st.button("Statistik zurücksetzen"):
    st.session_state.total_rolls = 0
    st.session_state.dice_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    st.experimental_rerun()