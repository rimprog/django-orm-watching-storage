from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    all_passcard_visits = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []
    for passcard_visit in all_passcard_visits:
        passcard_visit_info = {
            "entered_at": passcard_visit.entered_at,
            "duration": passcard_visit.format_duration(),
            "is_strange": passcard_visit.is_visit_long()
        }

        this_passcard_visits.append(passcard_visit_info)

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
