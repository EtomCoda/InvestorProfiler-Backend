from django.core.management.base import BaseCommand
from core.models import RiskProfile

class Command(BaseCommand):
    help = 'Seeds the database with basic risk profiles.'

    def handle(self, *args, **kwargs):
        profiles = [
            {
                "name": "Conservative",
                "description": "You prefer minimal risk and prioritize the preservation of your capital. You are willing to accept lower returns for greater stability and security."
            },
            {
                "name": "Moderately Conservative",
                "description": "You are willing to take on a small amount of risk for slightly higher returns, but still prioritize stability and capital preservation."
            },
            {
                "name": "Moderate",
                "description": "You seek a balance between risk and return. You are comfortable with some market fluctuations in exchange for moderate growth."
            },
            {
                "name": "Moderately Aggressive",
                "description": "You are willing to accept higher risk and volatility for the potential of higher long-term returns."
            },
            {
                "name": "Aggressive",
                "description": "You are comfortable with significant risk and market fluctuations in pursuit of the highest possible returns over the long term."
            },
        ]
        created = 0
        for profile in profiles:
            obj, is_created = RiskProfile.objects.get_or_create(
                name=profile["name"],
                defaults={"description": profile["description"]}
            )
            if not is_created and obj.description != profile["description"]:
                obj.description = profile["description"]
                obj.save()
            if is_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"{created} risk profiles created or updated."))