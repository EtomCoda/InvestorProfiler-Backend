from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Question, Option

class Command(BaseCommand):
    help = 'Seeds the database with questions and options'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Clear existing data (optional, comment out if not needed)
            # Question.objects.all().delete()
            # Option.objects.all().delete()

            # Question 1
            q1 = Question.objects.create(
                text="When do you intend to start withdrawing money from your investments?",
                order=1,
                category="TIME"
            )
            Option.objects.bulk_create([
                Option(question=q1, text="Less than 3 years", score=1),
                Option(question=q1, text="3 - 5 years", score=3),
                Option(question=q1, text="6 - 10 years", score=7),
                Option(question=q1, text="11 years or more", score=10),
            ])

            # Question 2
            q2 = Question.objects.create(
                text="Once you start withdrawing money from your investments, when do you plan to withdraw all the invested funds?",
                order=2,
                category="TIME"
            )
            Option.objects.bulk_create([
                Option(question=q2, text="Less than 2 years", score=0),
                Option(question=q2, text="2 - 5 years", score=1),
                Option(question=q2, text="6 - 10 years", score=4),
                Option(question=q2, text="11 years or more", score=8),
            ])

            # Question 3
            q3 = Question.objects.create(
                text="How would you describe your knowledge of investments?",
                order=3,
                category="TOLERANCE"
            )
            Option.objects.bulk_create([
                Option(question=q3, text="None", score=1),
                Option(question=q3, text="Limited", score=3),
                Option(question=q3, text="Good", score=7),
                Option(question=q3, text="Extensive", score=10),
            ])

            # Question 4
            q4 = Question.objects.create(
                text="What are you most concerned about when you invest your money?",
                order=4,
                category="TOLERANCE"
            )
            Option.objects.bulk_create([
                Option(question=q4, text="My investment losing value", score=0),
                Option(question=q4, text="Equally concerned about my investment losing or gaining value", score=4),
                Option(question=q4, text="My investment gaining value", score=8),
            ])

            # Question 5
            q5 = Question.objects.create(
                text="Which investments do you currently own?",
                order=5,
                category="TOLERANCE"
            )
            Option.objects.bulk_create([
                Option(question=q5, text="Bonds and/or bond funds", score=3),
                Option(question=q5, text="Stocks and/or stock funds", score=6),
                Option(question=q5, text="International securities and/or international funds", score=8),
            ])

            # Question 6
            q6 = Question.objects.create(
                text="Suppose that over the past three months, the stock market lost 25% of its value. A stock you invested in also lost 25% of its value. How would you react?",
                order=6,
                category="TOLERANCE"
            )
            Option.objects.bulk_create([
                Option(question=q6, text="Sell all my shares", score=0),
                Option(question=q6, text="Sell some of my shares", score=2),
                Option(question=q6, text="Do nothing", score=5),
                Option(question=q6, text="Buy more shares", score=8),
            ])

            # Question 7
            q7 = Question.objects.create(
                text="Outlined in the chart below are the most likely best-case and worst-case annual returns of five hypothetical investment plans. Which range of outcomes is most acceptable to you?",
                order=7,
                category="TOLERANCE"
            )
            Option.objects.bulk_create([
                Option(question=q7, text="A", score=0),
                Option(question=q7, text="B", score=3),
                Option(question=q7, text="C", score=6),
                Option(question=q7, text="D", score=8),
                Option(question=q7, text="E", score=10),
            ])

        self.stdout.write(self.style.SUCCESS('Successfully seeded questions and options'))