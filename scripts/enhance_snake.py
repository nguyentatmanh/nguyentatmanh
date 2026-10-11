"""Enhance contribution snake SVGs with vivid neon glow and vibrant styling."""
from pathlib import Path
import re

def enhance_svg(file_path: Path, glow_color: str):
    if not file_path.exists():
        return
    content = file_path.read_text(encoding='utf-8')
    
    # Inject glow filter to .s class
    glow_css = f"filter:drop-shadow(0 0 3px {glow_color}) drop-shadow(0 0 6px {glow_color}88);"
    if "drop-shadow" not in content and ".s{" in content:
        content = re.sub(
            r"(\.s\{[^}]*fill:var\(--cs\);)",
            rf"\1{glow_css}",
            content
        )
    file_path.write_text(content, encoding='utf-8')
    print(f"Enhanced {file_path.name} with {glow_color} glow.")

def main():
    enhance_svg(Path("assets/github-snake.svg"), "#ff0055")
    enhance_svg(Path("assets/github-snake-dark.svg"), "#00f5d4")

if __name__ == "__main__":
    main()
