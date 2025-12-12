from django.shortcuts import render
from .parser_fa import get_programs_by_faculty_and_levels, get_all_faculties
from django.http import HttpResponse, JsonResponse

def index(request):
    faculty = request.GET.get('faculty', '')
    levels = request.GET.get('levels', '').split(',') if request.GET.get('levels') else []
    programs = get_programs_by_faculty_and_levels(faculty, levels)
    return JsonResponse(programs, safe=False)
