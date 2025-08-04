import json
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Question, Option, RiskProfile, ProfileMapping

class CoreViewsTest(TestCase):
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

        # Create Options
        # Time Horizon
        cls.o1 = Option.objects.create(question=cls.q1, text="< 1 year", score=1)
        cls.o2 = Option.objects.create(question=cls.q2, text="1-2 years", score=1)
        # Tolerance
        cls.o3 = Option.objects.create(question=cls.q3, text="Low", score=5)
        cls.o4 = Option.objects.create(question=cls.q4, text="Low", score=5)
        cls.o5 = Option.objects.create(question=cls.q5, text="Low", score=5)
        cls.o6 = Option.objects.create(question=cls.q6, text="Low", score=5)
        cls.o7 = Option.objects.create(question=cls.q7, text="Low", score=5)

        # Options for a valid submission
        cls.valid_time_o1 = Option.objects.create(question=cls.q1, text="5-7 years", score=5)
        cls.valid_time_o2 = Option.objects.create(question=cls.q2, text="> 10 years", score=5)
        cls.valid_tolerance_o3 = Option.objects.create(question=cls.q3, text="High", score=10)
        cls.valid_tolerance_o4 = Option.objects.create(question=cls.q4, text="High", score=10)
        cls.valid_tolerance_o5 = Option.objects.create(question=cls.q5, text="High", score=10)
        cls.valid_tolerance_o6 = Option.objects.create(question=cls.q6, text="High", score=10)
        cls.valid_tolerance_o7 = Option.objects.create(question=cls.q7, text="High", score=10)

        # Create RiskProfile and ProfileMapping
        cls.profile = RiskProfile.objects.create(name="Aggressive", description="High risk")
        ProfileMapping.objects.create(
            time_score_min=8, time_score_max=10,
            tolerance_score_min=40, tolerance_score_max=50,
            profile=cls.profile
        )

        cls.client = Client()

    def test_get_risk_profile_view(self):
        response = self.client.get(reverse('risk_profile_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risk_form.html')

    def test_submit_risk_profile_form_success(self):
        option_ids = [
            self.valid_time_o1.id, self.valid_time_o2.id,
            self.valid_tolerance_o3.id, self.valid_tolerance_o4.id,
            self.valid_tolerance_o5.id, self.valid_tolerance_o6.id, self.valid_tolerance_o7.id
        ]
        data = json.dumps({'option_ids': option_ids})
        response = self.client.post(reverse('submit_risk_profile_form'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['profile'], 'Aggressive')

    def test_submit_risk_profile_form_not_post(self):
        response = self.client.get(reverse('submit_risk_profile_form'))
        self.assertEqual(response.status_code, 405)

    def test_submit_risk_profile_form_value_error(self):
        # Missing one question
        option_ids = [self.o1.id, self.o2.id, self.o3.id, self.o4.id, self.o5.id, self.o6.id]
        data = json.dumps({'option_ids': option_ids})
        response = self.client.post(reverse('submit_risk_profile_form'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('You must answer all 7 questions', response.json()['error'])

    def test_submit_risk_profile_form_short_time_horizon(self):
        option_ids = [
            self.o1.id, self.o2.id, self.o3.id, self.o4.id,
            self.o5.id, self.o6.id, self.o7.id
        ]
        data = json.dumps({'option_ids': option_ids})
        response = self.client.post(reverse('submit_risk_profile_form'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('For such a short time horizon', response.json()['error'])

    def test_submit_risk_profile_form_no_profile_found(self):
        # These scores do not map to any profile
        option_ids = [
            self.valid_time_o1.id, self.valid_time_o2.id,
            self.o3.id, self.o4.id, self.o5.id, self.o6.id, self.o7.id
        ]
        data = json.dumps({'option_ids': option_ids})
        response = self.client.post(reverse('submit_risk_profile_form'), data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'No matching profile found')

    def test_submit_risk_profile_form_invalid_json(self):
        data = 'not a valid json'
        response = self.client.post(reverse('submit_risk_profile_form'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())