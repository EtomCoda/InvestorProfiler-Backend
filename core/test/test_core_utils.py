
from django.test import TestCase
from core.models import Question, Option, RiskProfile, ProfileMapping
from core.utils import calculate_risk_profile, ShortTimeHorizonError

class CoreUtilsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create Questions
        cls.q1 = Question.objects.create(text="Time Horizon Q1", order=1, category='TIME')
        cls.q2 = Question.objects.create(text="Time Horizon Q2", order=2, category='TIME')
        cls.q3 = Question.objects.create(text="Tolerance Q1", order=3, category='TOLERANCE')
        cls.q4 = Question.objects.create(text="Tolerance Q2", order=4, category='TOLERANCE')
        cls.q5 = Question.objects.create(text="Tolerance Q3", order=5, category='TOLERANCE')
        cls.q6 = Question.objects.create(text="Tolerance Q4", order=6, category='TOLERANCE')
        cls.q7 = Question.objects.create(text="Tolerance Q5", order=7, category='TOLERANCE')

        # Create Options for a valid submission
        cls.time_o1 = Option.objects.create(question=cls.q1, text="5-7 years", score=5)
        cls.time_o2 = Option.objects.create(question=cls.q2, text="> 10 years", score=5)
        cls.tolerance_o3 = Option.objects.create(question=cls.q3, text="High", score=10)
        cls.tolerance_o4 = Option.objects.create(question=cls.q4, text="High", score=10)
        cls.tolerance_o5 = Option.objects.create(question=cls.q5, text="High", score=10)
        cls.tolerance_o6 = Option.objects.create(question=cls.q6, text="High", score=10)
        cls.tolerance_o7 = Option.objects.create(question=cls.q7, text="High", score=10)

        # Create Options for short time horizon
        cls.short_time_o1 = Option.objects.create(question=cls.q1, text="< 1 year", score=1)
        cls.short_time_o2 = Option.objects.create(question=cls.q2, text="1-2 years", score=1)

        # Create RiskProfile and ProfileMapping
        cls.profile = RiskProfile.objects.create(name="Aggressive", description="High risk")
        ProfileMapping.objects.create(
            time_score_min=8, time_score_max=10,
            tolerance_score_min=40, tolerance_score_max=50,
            profile=cls.profile
        )

    def test_calculate_risk_profile_success(self):
        option_ids = [
            self.time_o1.id, self.time_o2.id, self.tolerance_o3.id, self.tolerance_o4.id,
            self.tolerance_o5.id, self.tolerance_o6.id, self.tolerance_o7.id
        ]
        profile = calculate_risk_profile(option_ids)
        self.assertEqual(profile.name, 'Aggressive')

    def test_calculate_risk_profile_missing_question(self):
        option_ids = [self.time_o1.id, self.time_o2.id, self.tolerance_o3.id]
        with self.assertRaises(ValueError):
            calculate_risk_profile(option_ids)

    def test_calculate_risk_profile_short_time_horizon(self):
        option_ids = [
            self.short_time_o1.id, self.short_time_o2.id, self.tolerance_o3.id, self.tolerance_o4.id,
            self.tolerance_o5.id, self.tolerance_o6.id, self.tolerance_o7.id
        ]
        with self.assertRaises(ShortTimeHorizonError):
            calculate_risk_profile(option_ids)

    def test_calculate_risk_profile_no_mapping(self):
        # These scores do not map to any profile
        option_ids = [
            self.time_o1.id, self.short_time_o2.id, self.tolerance_o3.id, self.tolerance_o4.id,
            self.tolerance_o5.id, self.tolerance_o6.id, self.tolerance_o7.id
        ]
        profile = calculate_risk_profile(option_ids)
        self.assertIsNone(profile)
