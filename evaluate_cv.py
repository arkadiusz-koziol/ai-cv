from agent import ask_ollama, load_context
from parser import parse_pdf_cv

def validate_required_skills(cv_text: str, skills: list[str]) -> list[str]:
    """
    Sprawdza, które wymagane umiejętności (oznaczone jako ' (wymagana)') nie występują dosłownie w CV.
    """
    lower_cv = cv_text.lower()
    missing = []

    for skill in skills:
        if "(wymagana)" not in skill:
            continue
        skill_name = skill.replace(" (wymagana)", "").strip().lower()
        if skill_name not in lower_cv:
            missing.append(skill_name)

    return missing

def build_cv_evaluation_prompt(context: dict, cv_text: str) -> str:
    position = context["position"]
    required_skills = [s for s in context["skills"] if "(wymagana)" in s]
    optional_skills = [s for s in context["skills"] if "(mile widziana)" in s]

    required = ", ".join(required_skills).replace(" (wymagana)", "")
    optional = ", ".join(optional_skills).replace(" (mile widziana)", "")

    return (
        f"🔎 Rekrutuję na stanowisko: {position}.\n"
        f"🔐 Wymagane umiejętności (muszą być obecne w CV dosłownie lub jednoznacznie): {required}\n"
        f"🌿 Mile widziane (nieobowiązkowe): {optional if optional else 'brak'}\n\n"
        f"📄 Treść CV:\n"
        f"{cv_text}\n\n"
        f"🧠 Zasady oceny:\n"
        f"1. Jeśli chociaż **jedna z wymaganych umiejętności** nie występuje **dosłownie** lub **jednoznacznie** w CV, odpowiedź musi brzmieć ❌ NIE.\n"
        f"2. Nie zgaduj, nie interpretuj. *Brak = brak*. Jeśli w CV nie pojawia się konkretne słowo (np. „biznes”, „Excel”, „analiza statyczna”) lub jego oczywisty odpowiednik, uznaj, że tej kompetencji nie ma.\n"
        f"3. Nie oceniaj po stanowisku – tylko po treści i słowach z CV.\n\n"
        f"📋 Odpowiedz w tym formacie:\n"
        f"1. ✅ TAK / ❌ NIE\n"
        f"2. Uzasadnij w maksymalnie 5 zdaniach\n"
        f"3. Wypisz wykryte wymagane umiejętności (z listy)\n"
        f"4. Wypisz brakujące wymagane umiejętności (z listy)\n"
        f"5. Wymień mocne strony (jeśli są)\n"
        f"6. Wymień słabe strony (jeśli są)\n"
        f"7. Zaproponuj pytanie na rozmowę kwalifikacyjną"
    )

if __name__ == "__main__":
    path = input("Podaj ścieżkę do pliku CV (PDF): ").strip()
    context = load_context()
    cv_text = parse_pdf_cv(path)

    missing_required = validate_required_skills(cv_text, context["skills"])
    if missing_required:
        prompt = (
            f"🛑 Uwaga: Wykryto brakujące wymagane umiejętności: {', '.join(missing_required)}.\n"
            f"Twoja odpowiedź musi brzmieć ❌ NIE. Nie masz prawa interpretować braków jako obecnych.\n\n"
        ) + build_cv_evaluation_prompt(context, cv_text)
    else:
        prompt = build_cv_evaluation_prompt(context, cv_text)

    print("\n⏳ Analiza CV trwa...\n")
    response = ask_ollama(prompt)
    print("🧠 Odpowiedź modelu:\n")
    print(response)