from .models import Option, ProfileMapping
from collections import defaultdict
from django.http import JsonResponse

class ShortTimeHorizonError(Exception):
        """Custom exception for short time horizon."""
    
def calculate_risk_profile(selected_option_ids):
    """
    Calculate risk profile based on selected option IDs.
    Supports multiple selections for question 5.
    """
   
   
    # Remove any duplicate option IDs to avoid double counting
    selected_option_ids = list(set(selected_option_ids))
    print('SELECTED OPT ID',selected_option_ids)

    # Retrieve all selected Option objects with related Question
    options = Option.objects.filter(id__in=selected_option_ids).select_related("question")
    print('OPTIONS ID',options)

    # Group options by question order
    options_by_question = defaultdict(list)
    for option in options:
        options_by_question[option.question.order].append(option)
    
    print('OPTIONS BY QUESTION',options_by_question)

    # Ensure all 7 questions (1 to 7) are represented
    expected_questions = set(range(1, 8))
    actual_questions = set(options_by_question.keys())

    if actual_questions != expected_questions:
        raise ValueError(
            f"You must answer all 7 questions, including at least one choice for question 5. "
            f"Expected questions: {expected_questions}, but got: {actual_questions}"
        )

    # Calculate scores
    time_score = sum(
        option.score for q_order in (1, 2) for option in options_by_question[q_order]
    )
    tolerance_score = sum(
        option.score for q_order in (3, 4, 5, 6, 7) for option in options_by_question[q_order]
    )
    print('time score:', time_score,'tolerance score:',tolerance_score)

    if time_score < 3:
        raise ShortTimeHorizonError(
            'For such a short time horizon, a relatively low-risk portfolio of 40% short-term (average maturity of five years or less) bonds or bond funds and 60% cash investments is suggested, as stock investments may be significantly more volatile in the short term.'
        )

    # Find corresponding profile mapping
    mapping = ProfileMapping.objects.filter(
        time_score_min__lte=time_score,
        time_score_max__gte=time_score,
        tolerance_score_min__lte=tolerance_score,
        tolerance_score_max__gte=tolerance_score,
    ).first()

    return mapping.profile if mapping else None
