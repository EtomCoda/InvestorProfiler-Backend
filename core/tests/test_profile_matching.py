from django.test import TestCase
from core.models import RiskProfile, ProfileMapping

class ProfileMappingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # You can optionally run the load_profile_mappings command here if needed
        from django.core.management import call_command

        RiskProfile.objects.bulk_create([
            RiskProfile(name="Conservative"),
            RiskProfile(name="Moderate"),
            RiskProfile(name="Moderately Conservative"),
            RiskProfile(name="Moderately Aggressive"),
            RiskProfile(name="Aggressive"),
        ])
        call_command('load_profile_mappings')

    def test_profile_match(self):
        test_cases = [
            # (time_score, tolerance_score, expected_profile_name)
            (3, 20, "Moderately Conservative"),
            (14, 10, "Conservative"),
            (8, 38, "Aggressive"),
            (5, 37, "Moderately Aggressive"),
            (6, 30, "Moderate"),
            (10, 26, "Moderate"),
            (7, 12, "Conservative"),
        ]

        for time_score, risk_score, expected_name in test_cases:
            with self.subTest(time_score=time_score, risk_score=risk_score):
                match = ProfileMapping.objects.filter(
                    time_score_min__lte=time_score,
                    time_score_max__gte=time_score,
                    tolerance_score_min__lte=risk_score,
                    tolerance_score_max__gte=risk_score,
                ).first()
                self.assertIsNotNone(match, f"No profile match found for {time_score}, {risk_score}")
                self.assertEqual(match.profile.name, expected_name)
