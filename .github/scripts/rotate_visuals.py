import argparse
import datetime
from pathlib import Path
import re
import sys

# Visual 1: Git Repo Map (3 days)
GIT_REPO_MAP = '''<!-- ===================== git repo map ===================== -->

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/map-graph?username=probanjee&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F230592145%3Fu%3D2dae9ec52c1241cdcbec1fd6fce6a5f30b0a62d4%26v%3D4&mode=light" />
  <img src="https://www.gitskins.com/api/section/map-graph?username=probanjee&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F230592145%3Fu%3D2dae9ec52c1241cdcbec1fd6fce6a5f30b0a62d4%26v%3D4&mode=dark" width="100%" alt="A map of Prosun Banerjee's projects" />
</picture>

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/map-legend?username=probanjee&mode=light" />
  <img src="https://www.gitskins.com/api/section/map-legend?username=probanjee&mode=dark" width="100%" alt="Languages on the map" />
</picture>

<br/>

<h3 align="center">Up close</h3>

<p align="center">
  <a href="https://github.com/probanjee/Dynamic-API-Genarator"><picture><source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/map-card?username=probanjee&i=0&r=Dynamic-API-Genarator&mode=light" /><img src="https://www.gitskins.com/api/section/map-card?username=probanjee&i=0&r=Dynamic-API-Genarator&mode=dark" width="49%" alt="Dynamic-API-Genarator: api-builder  trpc  react19  vite  drizzle-orm  typescript  express  openapi  ai-assistant  mock-server  api-designer  security-audit" /></picture></a>
  <a href="https://github.com/probanjee/P.A.I."><picture><source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/map-card?username=probanjee&i=1&r=P.A.I.&mode=light" /><img src="https://www.gitskins.com/api/section/map-card?username=probanjee&i=1&r=P.A.I.&mode=dark" width="49%" alt="P.A.I.: Prosenjit, or P.A.I. (Practical Assistant Inside), is designed to be your desktop best friend, project manager, and personal AI assistant. Inspired by the futuristic assistants from Iron Man, this passion project focuses on creating a local-first AI companion for students, developers, and makers." /></picture></a>
</p>
<p align="center">
  <a href="https://github.com/probanjee/R.U.D.R.A"><picture><source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/map-card?username=probanjee&i=2&r=R.U.D.R.A&mode=light" /><img src="https://www.gitskins.com/api/section/map-card?username=probanjee&i=2&r=R.U.D.R.A&mode=dark" width="49%" alt="R.U.D.R.A: " /></picture></a>
  <a href="https://github.com/probanjee/probanjee"><picture><source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/map-card?username=probanjee&i=3&r=probanjee&mode=light" /><img src="https://www.gitskins.com/api/section/map-card?username=probanjee&i=3&r=probanjee&mode=dark" width="49%" alt="probanjee: " /></picture></a>
</p>

<sub>Project Map · drawn from my public repositories</sub>'''

# Visual 2: Solar System (2 days)
SOLAR_SYSTEM = '''<!-- ===================== Solar system ===================== -->

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/solar-orbits?username=probanjee&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F230592145%3Fu%3D2dae9ec52c1241cdcbec1fd6fce6a5f30b0a62d4%26v%3D4&mode=light" />
  <img src="https://www.gitskins.com/api/section/solar-orbits?username=probanjee&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F230592145%3Fu%3D2dae9ec52c1241cdcbec1fd6fce6a5f30b0a62d4%26v%3D4&mode=dark" width="100%" alt="My languages as planets around me" />
</picture>

<sub>Solar System · planets are languages, comets are recent pushes</sub>'''

# Visual 3: Repo Metro (2 days)
REPO_METRO = '''<!-- ===================== Repo Metro ===================== -->

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://www.gitskins.com/api/section/metro-map?username=probanjee&mode=light" />
  <img src="https://www.gitskins.com/api/section/metro-map?username=probanjee&mode=dark" width="100%" alt="My repositories as a metro map, one line per language" />
</picture>

<sub>Repo Metro · every line is a language, every stop a project</sub>'''

VISUALS = {
    "map": ("Git Repo Map", GIT_REPO_MAP),
    "solar": ("Solar System", SOLAR_SYSTEM),
    "metro": ("Repo Metro", REPO_METRO),
}

START_MARKER = "<!-- REPO_VISUAL_START -->"
END_MARKER = "<!-- REPO_VISUAL_END -->"

def choose_visual(weekday: int) -> tuple[str, str]:
    # 0 = Monday, 1 = Tuesday, 2 = Wednesday -> Git Repo Map (3 days)
    # 3 = Thursday, 4 = Friday             -> Solar System (2 days)
    # 5 = Saturday, 6 = Sunday             -> Repo Metro (2 days)
    if weekday in (0, 1, 2):
        return VISUALS["map"]
    elif weekday in (3, 4):
        return VISUALS["solar"]
    else:
        return VISUALS["metro"]

def update_readme(target_content: str, readme_path: Path) -> bool:
    content = readme_path.read_text(encoding="utf-8")
    
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL
    )
    
    if not pattern.search(content):
        print(f"Error: Could not find markers {START_MARKER} and {END_MARKER} in {readme_path}")
        return False
        
    replacement = f"{START_MARKER}\n\n{target_content}\n\n{END_MARKER}"
    new_content = pattern.sub(replacement, content)
    
    if new_content == content:
        print("README is already up-to-date with this visual.")
        return False
        
    readme_path.write_text(new_content, encoding="utf-8")
    return True

def main():
    parser = argparse.ArgumentParser(description="Rotate repository visual in profile README")
    parser.add_argument("--visual", choices=["map", "solar", "metro"], help="Force a specific visual")
    parser.add_argument("--day", type=int, choices=range(7), help="Simulate a day of week (0=Mon, 6=Sun)")
    parser.add_argument("--file", type=Path, default=Path(__file__).resolve().parent.parent.parent / "README.md")
    args = parser.parse_args()

    if args.visual:
        name, visual_snippet = VISUALS[args.visual]
        print(f"Using forced visual: {name}")
    else:
        weekday = args.day if args.day is not None else datetime.datetime.now(datetime.timezone.utc).weekday()
        day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][weekday]
        name, visual_snippet = choose_visual(weekday)
        print(f"Current Day: {day_name} (index {weekday}) -> Selected Visual: {name}")

    changed = update_readme(visual_snippet, args.file)
    if changed:
        print(f"Successfully updated README.md with '{name}'.")
    else:
        print("No changes written.")

if __name__ == "__main__":
    main()

