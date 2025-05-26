import streamlit as st
from agent import ask_ollama, save_context, load_context
from parser import parse_pdf_cv
from evaluate_cv import build_cv_evaluation_prompt
import tempfile


st.set_page_config(page_title="AI Rekruter", layout="centered")
st.title("🤖 AI Rekruter – analiza CV")


# Sekcja 1: Wymagania rekrutacyjne
with st.expander("📋 Ustaw wymagania"):
    position = st.text_input("Stanowisko", value="Backend Developer")
    skills = st.text_input("Umiejętności (oddziel przecinkami)", value="PHP, Laravel, PostgreSQL, Docker")

    if st.button("Zapisz wymagania"):
        skill_list = [s.strip() for s in skills.split(",")]
        save_context(position, skill_list)
        st.success("✅ Zapisano wymagania!")

# Sekcja 2: Wysyłanie CV
st.subheader("📄 Prześlij CV (PDF)")
uploaded_file = st.file_uploader("Wybierz plik PDF", type="pdf")

if uploaded_file:
    # Zapisujemy plik tymczasowo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Parsowanie CV
    try:
        cv_text = parse_pdf_cv(tmp_path)
        st.text_area("📝 Treść CV (podgląd)", cv_text, height=200)

        # Załaduj kontekst i zbuduj prompt
        context = load_context()
        prompt = build_cv_evaluation_prompt(context, cv_text)

        # Przycisk analizy
        if st.button("🧠 Oceń CV"):
            with st.spinner("Analiza trwa..."):
                response = ask_ollama(prompt)
            st.success("✅ Analiza ukończona!")
            st.text_area("🧠 Odpowiedź modelu", response, height=250)

    except Exception as e:
        st.error(f"Błąd: {e}")
