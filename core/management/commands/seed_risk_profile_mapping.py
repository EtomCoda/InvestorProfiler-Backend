from django.core.management.base import BaseCommand
from core.models import RiskProfile, ProfileMapping

class Command(BaseCommand):
    help = 'Load predefined risk profile mappings into the database.'

    def handle(self, *args, **kwargs):
        matrix = [
            ("Moderately Conservative", 3, 4, 19, 31),
            ("Moderately Conservative", 5, 6, 16, 24),
            ("Moderately Conservative", 7, 9, 13, 20),
            ("Moderately Conservative", 10, 12, 12, 18),
            ("Moderately Conservative", 14, 18, 11, 17),
            ("Moderately Aggressive", 5, 6, 36, 40),
            ("Moderately Aggressive", 7, 9, 29, 37),
            ("Moderately Aggressive", 10, 12, 27, 34),
            ("Moderately Aggressive", 14, 18, 25, 31),
            ("Aggressive", 7, 9, 38, 40),
            ("Aggressive", 10, 12, 35, 40),
            ("Aggressive", 14, 18, 32, 40),
            ("Moderate", 3, 4, 32, 40),
            ("Moderate", 5, 6, 25, 35),
            ("Moderate", 7, 9, 21, 28),
            ("Moderate", 10, 12, 19, 26),
            ("Moderate", 14, 18, 18, 24),
            ("Conservative", 3, 4, 0, 18),
            ("Conservative", 5, 6, 0, 15),
            ("Conservative", 7, 9, 0, 12),
            ("Conservative", 10, 12, 0, 11),
            ("Conservative", 14, 18, 0, 10),
        ]

        created = 0
        for name, t_min, t_max, r_min, r_max in matrix:
            profile = RiskProfile.objects.get(name=name)
            obj, is_created = ProfileMapping.objects.get_or_create(
                profile=profile,
                time_score_min=t_min,
                time_score_max=t_max,
                tolerance_score_min=r_min,
                tolerance_score_max=r_max,
            )
            if is_created:
                created += 1
        
        self.stdout.write(self.style.SUCCESS(f'{created} profile mappings created.'))