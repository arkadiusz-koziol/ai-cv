from agent import ask_ollama, load_context
from parser import parse_pdf_cv


def build_cv_evaluation_prompt(context: dict, cv_text: str) -> str:
    """
    Składa pełny prompt: opis stanowiska + treść CV + polecenie.
    """
    position = context["position"]
    skills = ", ".join(context["skills"])

    return (
        f"Rekrutuję na stanowisko: {position}.\n"
        f"Poszukuję kandydatów z następującymi umiejętnościami: {skills}.\n\n"
        f"Oto treść przesłanego CV:\n"
        f"{cv_text}\n\n"
        f"📌 Oceń, czy kandydat pasuje na to stanowisko. Odpowiedz:\n"
        f"- TAK/NIE\n"
        f"- Uzasadnij w maks. 5 zdaniach\n"
        f"- Wymień mocne i słabe strony\n"
        f"- Zasugeruj pytanie na rozmowę kwalifikacyjną"
    )


if __name__ == "__main__":
    path = input("Podaj ścieżkę do pliku CV (PDF): ").strip()
    context = load_context()
    cv_text = parse_pdf_cv(path)
    prompt = build_cv_evaluation_prompt(context, cv_text)

    print("\n⏳ Analiza CV trwa...\n")
    response = ask_ollama(prompt)
    print("🧠 Odpowiedź modelu:\n")
    print(response)
