from django.test import TestCase, Client
from core.models import RiskProfile
from funds.models import FundCategory, Fund
import json

class FundsAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create RiskProfiles for testing
        self.conservative_profile = RiskProfile.objects.create(name="Conservative", description="Conservative profile")
        self.aggressive_profile = RiskProfile.objects.create(name="Aggressive", description="Aggressive profile")

        # Create FundCategories
        self.cash_conservative = FundCategory.objects.create(name="Cash/Money Market Funds", percent=30.00, risk_profile=self.conservative_profile)
        self.fixed_income_conservative = FundCategory.objects.create(name="Fixed Income Funds", percent=50.00, risk_profile=self.conservative_profile)
        self.equity_aggressive = FundCategory.objects.create(name="Large Cap Equity Funds", percent=70.00, risk_profile=self.aggressive_profile)

        # Create Funds
        self.fund1 = Fund.objects.create(name="AXA Mansard Money Market Fund", score=2.80)
        self.fund2 = Fund.objects.create(name="Lead Fixed Income Fund", score=3.00)
        self.fund3 = Fund.objects.create(name="United Capital Equity Fund", score=4.50)

        # Add funds to categories
        self.cash_conservative.funds.add(self.fund1)
        self.fixed_income_conservative.funds.add(self.fund2)
        self.equity_aggressive.funds.add(self.fund3)

    def test_fund_category_creation(self):
        """Test that FundCategory objects are created correctly."""
        self.assertEqual(self.cash_conservative.name, "Cash/Money Market Funds")
        self.assertEqual(self.cash_conservative.percent, 30.00)
        self.assertEqual(self.cash_conservative.risk_profile, self.conservative_profile)

    def test_fund_creation(self):
        """Test that Fund objects are created correctly."""
        self.assertEqual(self.fund1.name, "AXA Mansard Money Market Fund")
        self.assertEqual(self.fund1.score, 2.80)

    def test_fund_category_fund_relationship(self):
        """Test the ManyToMany relationship between FundCategory and Fund."""
        self.assertIn(self.fund1, self.cash_conservative.funds.all())
        self.assertIn(self.fund2, self.fixed_income_conservative.funds.all())
        self.assertIn(self.fund3, self.equity_aggressive.funds.all())

    def test_get_fund_profile_view_success(self):
        """Test the get_fund_profile view for a successful GET request."""
        response = self.client.get('/funds/get-fund-profile/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertIn("Conservative", data)
        self.assertIn("Aggressive", data)

        # Verify Conservative profile data
        conservative_data = data["Conservative"]
        self.assertEqual(len(conservative_data), 2) # Cash and Fixed Income
        
        cash_category = next(item for item in conservative_data if item["category"] == "Cash/Money Market Funds")
        self.assertEqual(cash_category["percent"], "30.00")
        self.assertIn(["AXA Mansard Money Market Fund", "2.80"], cash_category["funds"])

        fixed_income_category = next(item for item in conservative_data if item["category"] == "Fixed Income Funds")
        self.assertEqual(fixed_income_category["percent"], "50.00")
        self.assertIn(["Lead Fixed Income Fund", "3.00"], fixed_income_category["funds"])

        # Verify Aggressive profile data
        aggressive_data = data["Aggressive"]
        self.assertEqual(len(aggressive_data), 1) # Large Cap Equity

        equity_category = next(item for item in aggressive_data if item["category"] == "Large Cap Equity Funds")
        self.assertEqual(equity_category["percent"], "70.00")
        self.assertIn(["United Capital Equity Fund", "4.50"], equity_category["funds"])

    def test_get_fund_profile_view_invalid_method(self):
        """Test the get_fund_profile view for an invalid request method (e.g., POST)."""
        response = self.client.post('/funds/get-fund-profile/', {})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data["error"], "Invalid request method")