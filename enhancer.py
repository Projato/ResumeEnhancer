from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


PROMPT_PATH = Path(__file__).parent / "prompts" / "enhancer_resume.txt"

DEFAULT_MODEL = "llama-3.3-70b-versatile"


def enhance_resume(resume_text: str, target_role: str, model: str = DEFAULT_MODEL) -> str:

    load_dotenv()  # loads GROQ_API_KEY from .env
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY. Create a .env file in the project root with GROQ_API_KEY=...")

    prompt_template = _load_prompt_template()
    prompt = prompt_template.format(target_role=target_role.strip(), resume_text=resume_text.strip())

    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    # Extract text safely
    content = completion.choices[0].message.content or ""
    return content.strip()


def _load_prompt_template() -> str:
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt file not found: {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")