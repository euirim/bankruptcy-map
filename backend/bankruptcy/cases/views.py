from django.shortcuts import render
from django.db.models import Q
from django.views.generic import DetailView

from .models import Case
from .documents import CaseDocument

def search(request):
    query_str = request.GET.get('q')
    cases = None
    if query_str:
        query_str = query_str.lower()
        cases = CaseDocument.search().query(
            'multi_match',
            query=query_str,
            fields=['name', 'jurisdiction']
        )[:30].to_queryset()

    return render(
        request, 
        'cases/search.html', 
        {'cases': cases, 'query': query_str}
    )


class CaseDetail(DetailView):

    model = Case
    slug_field = "pk"
    slug_url_kwarg = "pk"
