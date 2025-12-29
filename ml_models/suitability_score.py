# suitability_score.py

def calculate_suitability(
    interest_match,
    budget_ok,
    activities_per_day,
    travel_style_match,
    variety_score
):
    """
    All inputs should be between 0 and 1
    """

    score = (
        0.30 * interest_match +
        0.25 * budget_ok +
        0.20 * activities_per_day +
        0.15 * variety_score +
        0.10 * travel_style_match
    )

    return round(score * 100, 2)
