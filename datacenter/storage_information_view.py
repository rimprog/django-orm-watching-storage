from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone


def storage_information_view(request):
    not_leaved_visits = Visit.objects.filter(leaved_at=None)

    non_closed_visits = []
    for not_leaved_visit in not_leaved_visits:
        visit_entered_at_local_time = timezone.localtime(not_leaved_visit.entered_at)

        non_closed_visit = {
            "who_entered": not_leaved_visit.passcard.owner_name,
            "entered_at": visit_entered_at_local_time,
            "duration": not_leaved_visit.format_duration(),
            "is_strange": not_leaved_visit.is_visit_long(minutes=60)
        }

        non_closed_visits.append(non_closed_visit)

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }

    return render(request, 'storage_information.html', context)
