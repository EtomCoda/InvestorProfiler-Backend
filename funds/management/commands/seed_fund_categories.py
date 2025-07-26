from django.core.management.base import BaseCommand
from django.db import IntegrityError
from decimal import Decimal
from funds.models import FundCategory  
from core.models import RiskProfile

class Command(BaseCommand):
    help = 'Seed the FundCategory database with predefined categories and percentages'

    def handle(self, *args, **options):
        # Define the fund category data INCLUDING Cash/Money Market Funds
        category_data = [
            {
                'risk_profile': 'Conservative',
                'categories': [
                    {'name': 'Cash/Money Market Funds', 'percent': 30.00},
                    {'name': 'Fixed Income Funds', 'percent': 50.00},
                    {'name': 'Large Cap Equity Funds', 'percent': 20.00},
                ]
            },
            {
                'risk_profile': 'Moderately Conservative',
                'categories': [
                    {'name': 'Cash/Money Market Funds', 'percent': 10.00},
                    {'name': 'Fixed Income Funds', 'percent': 50.00},
                    {'name': 'Large Cap Equity Funds', 'percent': 35.00},
                    {'name': 'Small Cap Equity Funds', 'percent': 5.00},
                ]
            },
            {
                'risk_profile': 'Moderate',
                'categories': [
                    {'name': 'Cash/Money Market Funds', 'percent': 5.00},
                    {'name': 'Fixed Income Funds', 'percent': 35.00},
                    {'name': 'Large Cap Equity Funds', 'percent': 50.00},
                    {'name': 'Small Cap Equity Funds', 'percent': 10.00},
                ]
            },
            {
                'risk_profile': 'Moderately Aggressive',
                'categories': [
                    {'name': 'Cash/Money Market Funds', 'percent': 5.00},
                    {'name': 'Fixed Income Funds', 'percent': 15.00},
                    {'name': 'Large Cap Equity Funds', 'percent': 65.00},
                    {'name': 'Small Cap Equity Funds', 'percent': 15.00},
                ]
            },
            {
                'risk_profile': 'Aggressive',
                'categories': [
                    {'name': 'Cash/Money Market Funds', 'percent': 5.00},
                    {'name': 'Fixed Income Funds', 'percent': 0.00},
                    {'name': 'Large Cap Equity Funds', 'percent': 70.00},
                    {'name': 'Small Cap Equity Funds', 'percent': 20.00},
                    {'name': 'REITs and/or Infrastructure Funds', 'percent': 5.00},
                ]
            },
        ]

        try:
            for risk_data in category_data:
                risk_name = risk_data['risk_profile']
                
                risk_profile, created = RiskProfile.objects.get_or_create(name=risk_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created risk profile: {risk_name}"))

                for cat in risk_data['categories']:
                    category_name = cat['name']
                    try:
                        percent = Decimal(str(cat['percent'])).quantize(Decimal('0.01'))
                    except (ValueError, TypeError):
                        self.stdout.write(self.style.WARNING(f"Invalid percent for {category_name} in {risk_name}. Skipping."))
                        continue

                    try:
                        category, created = FundCategory.objects.update_or_create(
                            name=category_name,
                            risk_profile=risk_profile,
                            defaults={'percent': percent}
                        )
                        action = "Created" if created else "Updated"
                        self.stdout.write(self.style.SUCCESS(f"{action}: {category_name} ({percent}%) for {risk_name}"))
                    
                    except IntegrityError as e:
                        self.stdout.write(self.style.ERROR(f"Error saving {category_name} for {risk_name}: {e}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Unexpected error for {category_name}: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Seeding complete. Processed {len(category_data)} risk profiles."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during seeding: {e}"))
