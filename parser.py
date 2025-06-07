import pdfplumber
from pathlib import Path

def parse_pdf_cv(file_path: str) -> str:
    """
    Parsuje plik PDF z CV i zwraca czysty tekst.
    """
    cv_path = Path(file_path)
    if not cv_path.exists():
        raise FileNotFoundError(f"Plik {file_path} nie istnieje.")

    text = ""
    with pdfplumber.open(cv_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    return text.strip()

if __name__ == "__main__":
    path = input("Podaj ścieżkę do pliku CV (PDF): ").strip()
    content = parse_pdf_cv(path)

    print("\n📄 Treść CV:\n")
    print(content[:2000])
