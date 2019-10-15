from django.shortcuts import render
from django.db.models import Q
from .models import Case

def search(request):
    query_str = request.GET.get('q')
    cases = None
    if query_str:
        query_str = query_str.lower()
        cases = Case.objects.filter(
            Q(name__icontains=query_str) | 
            Q(jurisdiction=query_str)
        )

    return render(
        request, 
        'cases/search.html', 
        {'cases': cases, 'query': query_str}
    )
