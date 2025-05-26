import subprocess
import json
from pathlib import Path

CONTEXT_PATH = Path("recruitment_context.json")


def ask_ollama(prompt: str, model: str = "mistral") -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise RuntimeError(f"Błąd modelu: {result.stderr.decode()}")

    return result.stdout.decode().strip()


def build_requirements_prompt(position: str, skills: list[str]) -> str:
    skills_formatted = ", ".join(skills)
    return (
        f"Rekrutuję na stanowisko: {position}.\n"
        f"Poszukuję kandydatów z następującymi umiejętnościami: {skills_formatted}.\n"
        f"Na podstawie tego opisu, będę Ci przesyłać CV. Twoim zadaniem będzie ocenić, czy kandydat pasuje.\n"
        f"Zadaj mi jedno pytanie, które pomogłoby Ci jeszcze lepiej zrozumieć moje potrzeby rekrutacyjne."
    )


def save_context(position: str, skills: list[str]) -> None:
    CONTEXT_PATH.write_text(json.dumps({
        "position": position,
        "skills": skills
    }, indent=2))


def load_context() -> dict:
    if CONTEXT_PATH.exists():
        return json.loads(CONTEXT_PATH.read_text())
    else:
        raise FileNotFoundError("Brak zapisanego kontekstu rekrutacji.")


if __name__ == "__main__":
    stanowisko = input("Na jakie stanowisko rekrutujesz? ")
    umiejetnosci = input("Jakie umiejętności są wymagane? (oddziel przecinkami): ")

    skills_list = [s.strip() for s in umiejetnosci.split(",")]
    prompt = build_requirements_prompt(stanowisko, skills_list)

    save_context(stanowisko, skills_list)

    odpowiedz = ask_ollama(prompt)
    print("\n🧠 Odpowiedź modelu:")
    print(odpowiedz)
