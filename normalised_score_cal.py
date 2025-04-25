from dass21 import dass21_score
from emoji_calculation import calculate_emojis_scores


def calculate_normalised_score(dass_score, emoji_scores):
    """
    Computes individual normalized scores for Stress, Anxiety, and Depression.

    Parameters:
    - dass_score (dict): DASS-21 scores with keys ("stress", "anxiety", "depression").
    - emoji_scores (dict): Emoji-based scores with keys ("stress", "anxiety", "depression").

    Returns:
    - normalized_scores (dict): Sum of DASS-21 and emoji scores for each category.
    """

    # List of expected keys
    keys = ["stress", "anxiety", "depression"]

    # Ensure dass_score and emoji_scores have valid values
    for key in keys:
        # If key is missing, assign default value 0
        if key not in dass_score or dass_score[key] is None:
            print(f"Warning: Missing or None value for '{key}' in dass_score. Setting to 0.")
            dass_score[key] = 0
        
        if key not in emoji_scores or emoji_scores[key] is None:
            print(f"Warning: Missing or None value for '{key}' in emoji_scores. Setting to 0.")
            emoji_scores[key] = 0

    # Ensure values are numbers before summing
    try:
        normalised_scores = {
            key: float(dass_score[key])/42 + float(emoji_scores[key])/12 for key in keys
        }
    except ValueError as e:
        print(f"Error: Invalid data type in input scores. Details: {e}")
        return {}

    return normalised_scores



# from dass21 import dass21_score
# from emoji_calculation import calculate_emojis_scores

# def classify_severity(score, category):
#     """
#     Classifies the severity level based on the normalized score and category.

#     Parameters:
#     - score (float): Normalized score for the category.
#     - category (str): One of 'stress', 'anxiety', 'depression'.

#     Returns:
#     - str: Severity level ('Normal', 'Mild', etc.)
#     """
#     if category == "depression":
#         if score <= 0.21:
#             return "Normal"
#         elif score <= 0.31:
#             return "Mild"
#         elif score <= 0.48:
#             return "Moderate"
#         elif score <= 0.64:
#             return "Severe"
#         else:
#             return "Extremely Severe"
        
#     elif category == "anxiety":
#         if score <= 0.18:
#             return "Normal"
#         elif score <= 0.21:
#             return "Mild"
#         elif score <= 0.33:
#             return "Moderate"
#         elif score <= 0.44:
#             return "Severe"
#         else:
#             return "Extremely Severe"
        
#     elif category == "stress":
#         if score <= 0.33:
#             return "Normal"
#         elif score <= 0.42:
#             return "Mild"
#         elif score <= 0.59:
#             return "Moderate"
#         elif score <= 0.78:
#             return "Severe"
#         else:
#             return "Extremely Severe"
        
#     return "Unknown"

# def calculate_normalised_score(dass_score, emoji_scores):
#     """
#     Computes individual normalized scores for Stress, Anxiety, and Depression,
#     and classifies their severity.

#     Parameters:
#     - dass_score (dict): DASS-21 scores with keys ("stress", "anxiety", "depression").
#     - emoji_scores (dict): Emoji-based scores with keys ("stress", "anxiety", "depression").

#     Returns:
#     - result (dict): Dictionary with normalized scores and severity levels.
#     """
#     keys = ["stress", "anxiety", "depression"]
#     result = {}

#     for key in keys:
#         # Handle missing values
#         if key not in dass_score or dass_score[key] is None:
#             print(f"Warning: Missing or None value for '{key}' in dass_score. Setting to 0.")
#             dass_score[key] = 0
        
#         if key not in emoji_scores or emoji_scores[key] is None:
#             print(f"Warning: Missing or None value for '{key}' in emoji_scores. Setting to 0.")
#             emoji_scores[key] = 0

#         try:
#             normalized_score = float(dass_score[key]) / 42 + float(emoji_scores[key]) / 9
#             severity = classify_severity(normalized_score, key)
#             result[key] = {
#                 "normalized_score": round(normalized_score, 2),
#                 "severity": severity
#             }
#         except ValueError as e:
#             print(f"Error: Invalid data type for '{key}'. Details: {e}")
#             result[key] = {
#                 "normalized_score": 0,
#                 "severity": "Unknown"
#             }

#     return result
