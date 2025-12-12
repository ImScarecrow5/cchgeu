# education_parser/parser.py
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

# Внутреннее кэширование (можно заменить на Django cache позже)
_programs = None

def _fetch_and_parse():
    global _programs
    if _programs is not None:
        return _programs

    url = "https://cchgeu.ru/education/programms/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='table')
    if not table:
        raise ValueError("Таблица не найдена")

    rows = table.find_all('tr')
    programs = []
    current_level = None

    for row in rows:
        if row.get('bgcolor') == "#f5f5f5" and row.get('align') == "center":
            cells = row.find_all('td')
            if cells:
                current_level = cells[0].get_text(strip=True)
            continue

        if row.find('th'):
            continue

        cells = row.find_all('td')
        if len(cells) < 4:
            continue

        program_name = cells[1].get_text(strip=True)
        level = cells[2].get_text(strip=True) or current_level
        faculty_cell = cells[3]
        faculty = faculty_cell.get_text(strip=True)

        programs.append({
            "program": program_name,
            "level": level,
            "faculty": faculty
        })

    _programs = programs
    return programs

def get_all_programs() -> List[Dict[str, str]]:
    return _fetch_and_parse()

def normalize_level(level: str) -> str:
    if '(' in level:
        return level.split('(', 1)[0].strip()
    return level.strip()

def get_programs_by_faculty_and_levels(faculty: str, levels: List[str]) -> List[Dict[str, str]]:
    all_programs = get_all_programs()
    normalized_levels = {normalize_level(l) for l in levels}
    result = []
    for p in all_programs:
        if p["faculty"] == faculty and normalize_level(p["level"]) in normalized_levels:
            result.append(p)
    return result

def get_all_faculties() -> List[str]:
    all_programs = get_all_programs()
    return sorted({p["faculty"] for p in all_programs})