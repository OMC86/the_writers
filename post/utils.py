from .models import Competition

def activate():
    competition = Competition.objects.all()
    for comp in competition:
        comp._is_active()
