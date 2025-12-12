# education_parser/parser.py
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

# Внутреннее кэширование
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

    for row in rows:
        # Пропускаем заголовки таблицы и разделители
        if row.get('bgcolor') == "#f5f5f5" and row.get('align') == "center":
            continue

        if row.find('th'):
            continue

        cells = row.find_all('td')
        if len(cells) < 4:
            continue

        # Получаем номер и название программы
        program_cell = cells[1].find('a')
        if program_cell:
            program_name = program_cell.text.strip()
        else:
            program_name = cells[1].get_text(strip=True)

        # Получаем уровень образования
        level = cells[2].get_text(strip=True)

        # Получаем факультет
        faculty_cell = cells[3].find('a')
        if faculty_cell:
            faculty = faculty_cell.text.strip()
        else:
            faculty = cells[3].get_text(strip=True)

        # Извлекаем код программы из названия (например, "07.03.01")
        code = ""
        import re
        match = re.search(r'(\d{2}\.\d{2}\.\d{2})', program_name)
        if match:
            code = match.group(1)

        programs.append({
            "code": code,
            "program": program_name,
            "level": level,
            "faculty": faculty
        })

    _programs = programs
    return programs


def get_all_programs() -> List[Dict[str, str]]:
    return _fetch_and_parse()


def get_programs_by_faculty(faculty: str) -> List[Dict[str, str]]:
    all_programs = get_all_programs()
    result = []
    for p in all_programs:
        if p["faculty"] and p["faculty"].strip() and p["faculty"].strip() == faculty:
            result.append(p)
    return result


def get_all_faculties() -> List[str]:
    all_programs = get_all_programs()
    # Фильтруем пустые строки и сортируем уникальные факультеты
    faculties_set = set()
    for p in all_programs:
        if p["faculty"] and p["faculty"].strip():
            faculties_set.add(p["faculty"].strip())
    return sorted(faculties_set)


print("=" * 80)
print("ТЕСТ ПАРСЕРА")
print("=" * 80)

# Получаем все факультеты
faculties = get_all_faculties()
print(f"Всего факультетов: {len(faculties)}")
print("Первые 10 факультетов:")
for i, f in enumerate(faculties[:10], 1):
    print(f"{i}. {f}")

# Тестируем один факультет
if faculties:
    test_faculty = faculties[0]
    print(f"\nТестируем факультет: {test_faculty}")

    programs = get_programs_by_faculty(test_faculty)
    print(f"Найдено программ: {len(programs)}")

    if programs:
        print("Первые 3 программы:")
        for i, p in enumerate(programs[:3], 1):
            print(f"{i}. Код: {p['code']}")
            print(f"   Название: {p['program'][:80]}...")
            print(f"   Уровень: {p['level']}")
            print(f"   Факультет: {p['faculty']}")
            print()

# Получаем все программы
all_programs = get_all_programs()
print(f"Всего программ на сайте: {len(all_programs)}")