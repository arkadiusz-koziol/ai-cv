# AI-CV Filter – System wspomagania rekrutacji

System informatyczny wspierający preselekcję CV przy użyciu lokalnego modelu AI.

---

## 📌 Opis projektu

Celem systemu jest wsparcie działu HR w ocenie kandydatów na stanowiska techniczne. Aplikacja pozwala zdefiniować wymagania (stanowisko + umiejętności), wgrać CV (PDF), a następnie otrzymać ocenę dopasowania kandydata wygenerowaną przez lokalnie uruchomiony model językowy.

---

## 🏢 Firma: Example Sp. z o.o.

- Branża: tworzenie aplikacji webowych B2B
- Problem: zbyt dużo CV, brak wiedzy technicznej w HR do ich selekcji
- Użytkownicy: Rekruter HR, CTO, System AI
- Rozwiązanie: lokalna aplikacja z UI + AI, bez potrzeby przesyłania danych do chmury

---

## 🧠 Technologia

- **Python 3.10+**
- **Ollama** + **Mistral** (lokalny model językowy)
- **Streamlit** – prosty interfejs webowy
- **pdfplumber** – konwersja CV PDF → tekst

---

## 🔧 Struktura projektu

```
AI-CV/
├── agent.py                  # Komunikacja z modelem AI
├── app.py                   # UI Streamlit do obsługi procesu
├── evaluate_cv.py           # Łączenie kontekstu i CV, generowanie prompta
├── parser.py                # Parsowanie plików PDF
├── recruitment_context.json # Kontekst wymagań
├── sample_cv/               # Przykładowe CV
├── requirements.txt         # Lista zależności
└── README.md                # Dokumentacja (ten plik)
```

---

## 🚀 Uruchomienie projektu

### 1. Zainstaluj model AI lokalnie

#### macOS:
```bash
brew install ollama
ollama run mistral
```

#### Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run mistral
```

#### Windows:
- Pobierz z [https://ollama.com/download](https://ollama.com/download)
- Zainstaluj i uruchom aplikację
- Otwórz CMD i uruchom: `ollama run mistral`

### 2. Zainstaluj zależności Pythona

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Uruchom aplikację webową

```bash
streamlit run app.py
```

---

## 💡 Możliwości

- Automatyczna ocena CV względem stanowiska
- Uzasadnienie dopasowania
- Szybka preselekcja kandydatów
- Działa offline – bez przesyłania danych do chmury

---

## 📌 Planowane rozszerzenia

- Eksport wyników do CSV
- Ocena punktowa kandydatów
- Obsługa wielu CV jednocześnie
- Integracja z systemami ATS

---

## 👨‍💻 Autorzy

- Arkadiusz Kozioł
- Patrycja Królikowska

Projekt realizowany w ramach przedmiotu *Systemy informatyczne zarządzania*.
