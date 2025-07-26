import pandas as pd
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from decimal import Decimal
from funds.models import Fund, FundCategory

class Command(BaseCommand):
    help = 'Seed the Fund database with rankings from cleaned_fund_rankings.csv, linking to all Fund categories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            default='funds/management/csv_data/cleaned_fund_rankings.csv',
            help='Path to the CSV file containing cleaned fund rankings'
        )

    def handle(self, *args, **options):
        csv_file = options['csv']
        
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file)
            
            # Verify required columns
            required_columns = ['Fund_Name', 'Overall_Score', 'Fund_Category']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"CSV must contain columns: {required_columns}")

            # Fetch all FundCategory records and create a lookup by name
            all_categories = {cat.name: cat for cat in FundCategory.objects.all()}

            # Process each row
            for _, row in df.iterrows():
                fund_name = row['Fund_Name']
                fund_category_names = row['Fund_Category']
                try:
                    score = Decimal(str(row['Overall_Score'])).quantize(Decimal('0.01'))  # Round to 2 decimal places
                except (ValueError, TypeError):
                    self.stdout.write(self.style.WARNING(f"Invalid score for {fund_name}. Skipping."))
                    continue

                # Validate fund name length
                if len(fund_name) > 225:
                    self.stdout.write(self.style.WARNING(f"Fund name too long: {fund_name}. Skipping."))
                    continue

                try:
                    # Create or update Fund record
                    fund, created = Fund.objects.update_or_create(
                        name=fund_name,
                        defaults={'score': score}
                    )

                    # Splits category names and fetches all matching category objects (including duplicates)
                    category_names = [name.strip() for name in fund_category_names.split(',')]
                    categories = []
                    for name in category_names:
                        matches = list(FundCategory.objects.filter(name=name))
                        if matches:
                            categories.extend(matches)

                    if categories:
                        fund.categories.set([])  
                        fund.categories.add(*categories)
                    else:
                        self.stdout.write(self.style.WARNING(f"No valid categories found for fund '{fund_name}'."))
                        continue

                    action = "Created" if created else "Updated"
                    self.stdout.write(self.style.SUCCESS(f"{action}: {fund_name} (Score: {score}, Categories: {', '.join(category_names)})"))

                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"Error saving {fund_name}: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Unexpected error for {fund_name}: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Seeding complete. Processed {len(df)} funds."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: {csv_file} not found."))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR(f"Error: {csv_file} is empty."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading CSV: {e}"))