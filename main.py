"""def main():
    print("Hello from resume-enhancer!")


if __name__ == "__main__":
    main()
"""

"""from pathlib import Path

def main():
    base = Path(__file__).parent
    resumes_dir = base / "resumes"

    print("Resume Enhancer project scaffold is ready.")
    print(f"Resumes folder: {resumes_dir}")

    if resumes_dir.exists():
        files = sorted([p.name for p in resumes_dir.iterdir() if p.is_file()])
        print("Files in resumes/:")
        for f in files:
            print(" -", f)
    else:
        print("resumes/ folder not found (unexpected).")

if __name__ == "__main__":
    main()
"""

from pathlib import Path

from resume_reader import read_resume


"""
def main():
    base = Path(__file__).parent
    resumes_dir = base / "resumes"

    input_txt = resumes_dir / "input_resume.txt"

    doc = read_resume(input_txt)

    print("Loaded resume")
    print("Path:", doc.path)
    print("Type:", doc.ext)
    print("\n--- Preview (first 400 chars) ---")
    print(doc.text[:400])
    print("\n--- Stats ---")
    print("Chars:", len(doc.text))
    print("Lines:", doc.text.count("\n") + 1)


if __name__ == "__main__":
    main()
"""

from pathlib import Path
from resume_reader import read_resume


def main():
    base = Path(__file__).parent
    resumes_dir = base / "resumes"

    if not resumes_dir.exists():
        print("resumes/ folder not found.")
        return

    # 1) List available files (txt/pdf only)
    allowed_ext = {".txt", ".pdf"}
    files = sorted([p.name for p in resumes_dir.iterdir() if p.is_file() and p.suffix.lower() in allowed_ext])

    if not files:
        print("No .txt or .pdf files found in resumes/")
        return

    print("\nAvailable resume files in resumes/:")
    for f in files:
        print(" -", f)

    # 2) Ask user which file to read
    filename = input("\nType the filename to read (exactly as shown): ").strip()

    if not filename:
        print("No filename entered.")
        return

    target_path = resumes_dir / filename

    # 3) Read + preview
    try:
        doc = read_resume(target_path)
    except Exception as e:
        print(f"Could not read '{filename}': {e}")
        return

    print("\n Loaded resume")
    print("Path:", doc.path)
    print("Type:", doc.ext)

    print("\n --- Preview (first 500 chars) ---")
    print(doc.text[:500])

    print("\n --- Stats ---")
    print("Chars:", len(doc.text))
    print("Lines:", doc.text.count("\n") + 1)


if __name__ == "__main__":
    main()