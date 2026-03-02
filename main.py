from pathlib import Path
from resume_reader import read_resume
from enhancer import enhance_resume
from comparator import build_unified_diff

allowed_ext = {".txt", ".pdf"}


def main():
    base = Path(__file__).parent
    resumes_dir = base / "resumes"

    if not resumes_dir.exists():
        print("resumes/ folder not found.")
        return

    #List available files (txt/pdf only)
    files = sorted([p.name for p in resumes_dir.iterdir() if p.is_file() and p.suffix.lower() in allowed_ext])

    if not files:
        print("No files found in resumes")
        return

    print("\n Available resume files in resumes:")
    for f in files:
        print(" -", f)

    # Ask user which file to read
    filename = input("\nType the filename to read (exactly as shown): ").strip()
    if not filename:
        print("No filename entered.")
        return
    
    role = input("Enter the target role: ").strip()
    if not role:
        print("No target role entered.")
        return

    target_path = resumes_dir / filename
    if not target_path.exists():
        print(f"File not found: {filename}")
        return
    
    print("\nReading Resume")
    doc=read_resume(target_path)

    print("Calling LLM")
    enhanced = enhance_resume(doc.text, target_role=role)

    # Save enhanced output
    stem = Path(filename).stem
    enhanced_name=f"enhanced_{stem}.txt"
    enhanced_path = resumes_dir / enhanced_name
    enhanced_path.write_text(enhanced, encoding="utf-8")
    
    # Generate unified diff between original and enhanced resume
    diff_result = build_unified_diff(
        original_text=doc.text,
        enhanced_text=enhanced,
        from_name=f"{stem}_original",
        to_name=f"{stem}_enhanced",
    )
    diff_name = f"diff_{stem}.txt"
    diff_path = resumes_dir / diff_name
    diff_path.write_text(diff_result.diff_text, encoding="utf-8")

    # Save enhanced resume output
    print("\nEnhancement Complete")
    print("Saved enhanced to: ", enhanced_name)
    print("Saved diff to: ", diff_name)
    print("Diff changed lines:", diff_result.changed_lines)

    print("\n --- Enhanced preview (first 500 chars) ---")
    print(enhanced[:500])

if __name__ == "__main__":
    main()