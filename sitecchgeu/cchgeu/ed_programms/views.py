# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .parser_fa import get_all_faculties, get_programs_by_faculty
import re

def vizit(request):
    faculties = get_all_faculties()
    context = {
        'faculties': faculties,
    }
    return render(request, "vizitka.html", context)

def index(request):
    faculties = get_all_faculties()
    selected_faculty = None
    programs = []

    if request.method == 'POST':
        selected_faculty = request.POST.get('selected_faculty')
        print(f"Выбран факультет: {selected_faculty}")

        if selected_faculty and selected_faculty != "Выберите факультет":
            programs = get_programs_by_faculty(selected_faculty)
            print(f"Найдено {len(programs)} программ для факультета '{selected_faculty}'")

    context = {
        'faculties': faculties,
        'selected_faculty': selected_faculty,
        'programs': programs,
    }
    return render(request, "index.html", context)


def get_faculty_programs(request):
    if request.method == 'GET':
        faculty = request.GET.get('faculty')
        levels = request.GET.getlist('levels')  # Получаем список уровней

        print(f"=== AJAX запрос получен ===")
        print(f"Факультет: {faculty}")
        print(f"Уровни фильтрации: {levels}")
        print(f"Полные GET параметры: {dict(request.GET)}")

        if not faculty:
            print("Ошибка: Факультет не указан")
            return JsonResponse({
                'success': False,
                'error': 'Факультет не указан'
            }, status=400)

        try:
            # Получаем все программы для факультета
            print(f"Запрашиваем программы для факультета: {faculty}")
            all_programs = get_programs_by_faculty(faculty)
            print(f"Получено {len(all_programs)} программ")

            # Фильтруем по уровням, если они указаны
            filtered_programs = all_programs
            if levels:
                print(f"Применяем фильтрацию по уровням: {levels}")
                # Более гибкая фильтрация - ищем частичное совпадение
                filtered_programs = []
                for program in all_programs:
                    program_level = program.get('level', '')
                    if program_level:
                        # Проверяем, содержит ли уровень программы любой из выбранных уровней
                        if any(selected_level.lower() in program_level.lower()
                               for selected_level in levels if selected_level):
                            filtered_programs.append(program)
                    else:
                        # Если у программы нет уровня, пропускаем её при фильтрации
                        if not levels or len(levels) == 0:
                            filtered_programs.append(program)

                print(f"После фильтрации осталось {len(filtered_programs)} программ")

            # Форматируем данные для ответа
            programs_data = []
            for program in filtered_programs:
                full_name = program.get('program', '')
                program_level = program.get('level', '')

                # Извлекаем код и название
                code = ''
                name = full_name

                if full_name:
                    parts = re.match(r'^(\d{2}\.\d{2}\.\d{2})\s+(.*)$', full_name)
                    if parts:
                        code = parts.group(1)
                        name = parts.group(2).strip()

                programs_data.append({
                    'code': code,
                    'name': name,
                    'level': program_level,
                    'original_name': full_name  # Для отладки
                })

            print(f"Подготовлено {len(programs_data)} программ для отправки")

            return JsonResponse({
                'success': True,
                'faculty': faculty,
                'programs': programs_data,
                'count': len(programs_data)
            })

        except Exception as e:
            print(f"Ошибка в get_faculty_programs: {str(e)}")
            import traceback
            traceback.print_exc()

            return JsonResponse({
                'success': False,
                'error': f'Внутренняя ошибка сервера: {str(e)}'
            }, status=500)

    print(f"Неверный метод запроса: {request.method}")
    return JsonResponse({
        'success': False,
        'error': 'Метод не поддерживается'
    }, status=405)