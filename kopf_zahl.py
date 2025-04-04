import streamlit as st
import random

# Initialisierung des Session States, falls noch nicht vorhanden
if 'total_clicks' not in st.session_state:
    st.session_state.total_clicks = 0

if 'heads_count' not in st.session_state:
    st.session_state.heads_count = 0

if 'tails_count' not in st.session_state:
    st.session_state.tails_count = 0

# App-Titel
st.title("Kopf oder Zahl")
st.write("Klicke auf den Button, um eine Münze zu werfen!")


# Funktion für den Münzwurf
def toss_coin():
    st.session_state.total_clicks += 1
    result = random.choice(["Kopf", "Zahl"])

    if result == "Kopf":
        st.session_state.heads_count += 1
    else:
        st.session_state.tails_count += 1

    return result


# Button zum Werfen der Münze
if st.button("Münze werfen"):
    result = toss_coin()
    st.success(f"Ergebnis: {result}")

# Statistik anzeigen
st.subheader("Statistik")
st.write(f"Gesamtanzahl der Würfe: {st.session_state.total_clicks}")
st.write(f"Kopf: {st.session_state.heads_count}")
st.write(f"Zahl: {st.session_state.tails_count}")

# Verhältnis anzeigen
if st.session_state.total_clicks > 0:
    heads_percentage = (st.session_state.heads_count / st.session_state.total_clicks) * 100
    tails_percentage = (st.session_state.tails_count / st.session_state.total_clicks) * 100

    st.write(f"Verhältnis Kopf: {heads_percentage:.1f}%")
    st.write(f"Verhältnis Zahl: {tails_percentage:.1f}%")

    # Visualisierung mit einem Balkendiagramm
    st.bar_chart({
        "Kopf": heads_percentage,
        "Zahl": tails_percentage
    })