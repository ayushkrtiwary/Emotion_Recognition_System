# def dass21_score(responses, selected_emojis):
#     """
#     Calculate DASS-21 scores for Depression, Anxiety, and Stress,
#     including adjustments based on selected emojis.
#     """
#     if len(responses) != 21:
#         raise ValueError("All 21 questions must be answered.")

#     # Indices for each category based on the DASS-21 questionnaire
#     depression_indices = [2, 4, 5, 10, 13, 16, 20]
#     anxiety_indices = [1, 6, 8, 9, 15, 18, 19]
#     stress_indices = [0, 3, 7, 11, 12, 14, 17]

#     # Compute initial scores
#     depression_score = sum(responses[i] for i in depression_indices) * 2
#     anxiety_score = sum(responses[i] for i in anxiety_indices) * 2
#     stress_score = sum(responses[i] for i in stress_indices) * 2

#     # Emoji adjustment mapping
#     emoji_mapping = {
#         "😢": "Depression", "😭": "Depression", "😞": "Depression", "😔": "Depression", "🥀": "Depression", "💔": "Depression",
#         "😩": "Depression", "😶": "Depression", "🖤": "Depression",
#         "😰": "Anxiety", "😨": "Anxiety", "😱": "Anxiety", "🤯": "Anxiety", "🫨": "Anxiety", "😬": "Anxiety", "😖": "Anxiety",
#         "🫣": "Anxiety", "🏃💨": "Anxiety",
#         "😡": "Stress", "😖": "Stress", "😤": "Stress", "😵": "Stress", "🤬": "Stress", "😓": "Stress", "🤦": "Stress", "💢": "Stress",
#         "😠": "Stress"
#     }

#     # Adjust scores based on emoji selection
#     depression_adjustment = sum(1 for emoji in selected_emojis if emoji_mapping.get(emoji) == "Depression")
#     anxiety_adjustment = sum(1 for emoji in selected_emojis if emoji_mapping.get(emoji) == "Anxiety")
#     stress_adjustment = sum(1 for emoji in selected_emojis if emoji_mapping.get(emoji) == "Stress")

#     depression_score += depression_adjustment
#     anxiety_score += anxiety_adjustment
#     stress_score += stress_adjustment

#     # Display final score at the end of emoji selection
#     final_scores = {
#         "Depression": depression_score,
#         "Anxiety": anxiety_score,
#         "Stress": stress_score
#     }
    
#     print("\nFinal Scores After Emoji Selection:")
#     for category, score in final_scores.items():
#         print(f"{category}: {score}")

#     return final_scores


def dass21_score(responses, selected_emojis=None):
    
    #Calculate DASS-21 scores for Depression, Anxiety, and Stress.
    
    if len(responses) != 21:
        raise ValueError("All 21 questions must be answered.")

    # Indices for each category based on the DASS-21 questionnaire
    depression_indices = [2, 4, 5, 10, 13, 16, 20]
    anxiety_indices = [1, 6, 8, 9, 15, 18, 19]
    stress_indices = [0, 3, 7, 11, 12, 14, 17]

    # Compute initial scores
    depression_score = sum(responses[i] for i in depression_indices) * 2
    anxiety_score = sum(responses[i] for i in anxiety_indices) * 2
    stress_score = sum(responses[i] for i in stress_indices) * 2

    # Emoji adjustment mapping
    emoji_mapping = {
        "😢": "Depression", "😭": "Depression", "😞": "Depression", "😔": "Depression", "🥀": "Depression", "💔": "Depression",
        "😩": "Depression", "😶": "Depression", "🖤": "Depression",
        "😰": "Anxiety", "😨": "Anxiety", "😱": "Anxiety", "🤯": "Anxiety", "🫨": "Anxiety", "😬": "Anxiety", "😖": "Anxiety",
        "🫣": "Anxiety", "🏃💨": "Anxiety",
        "😡": "Stress", "😖": "Stress", "😤": "Stress", "😵": "Stress", "🤬": "Stress", "😓": "Stress", "🤦": "Stress", "💢": "Stress",
        "😠": "Stress"
    }

    # Adjust scores based on emoji selection
    if selected_emojis:
        depression_adjustment = sum(1 for emoji in selected_emojis if emoji_mapping.get(emoji) == "Depression")
        anxiety_adjustment = sum(1 for emoji in selected_emojis if emoji_mapping.get(emoji) == "Anxiety")
        stress_adjustment = sum(1 for emoji in selected_emojis if emoji_mapping.get(emoji) == "Stress")

        depression_score += depression_adjustment
        anxiety_score += anxiety_adjustment
        stress_score += stress_adjustment

    return {
        "Depression": depression_score,
        "Anxiety": anxiety_score,
        "Stress": stress_score
    }




"""def dass21_score(responses):
    #Calculate DASS-21 scores for Depression, Anxiety, and Stress.
    #Each category consists of 7 specific questions in the DASS-21 scale.

    if len(responses) != 21:
        raise ValueError("All 21 questions must be answered.")
    
    # Indices for each category based on the DASS-21 questionnaire
    depression_indices = [2, 4, 5, 10, 13, 16, 20]
    anxiety_indices = [1, 6, 8, 9, 15, 18, 19]
    stress_indices = [0, 3, 7, 11, 12, 14, 17]
    
    # Compute scores by summing values for each category
    depression_score = sum(responses[i] for i in depression_indices) * 2
    anxiety_score = sum(responses[i] for i in anxiety_indices) * 2
    stress_score = sum(responses[i] for i in stress_indices) * 2
    
    return {
        "Depression": depression_score,  # ✅ Changed key name
        "Anxiety": anxiety_score,        # ✅ Changed key name
        "Stress": stress_score           # ✅ Changed key name
    }
"""




"""def dass21_score(responses, selected_emojis):
    
    Calculate DASS-21 scores for Depression, Anxiety, and Stress.
    
    if len(responses) != 21:
        raise ValueError("All 21 questions must be answered.")

    # Indices for each category based on the DASS-21 questionnaire
    depression_indices = [2, 4, 5, 10, 13, 16, 20]
    anxiety_indices = [1, 6, 8, 9, 15, 18, 19]
    stress_indices = [0, 3, 7, 11, 12, 14, 17]

    # Compute initial scores
    depression_score = sum(responses[i] for i in depression_indices) * 2
    anxiety_score = sum(responses[i] for i in anxiety_indices) * 2
    stress_score = sum(responses[i] for i in stress_indices) * 2

    # Emoji adjustment mapping
    emoji_mapping = {
        "😢": "Depression", "😭": "Depression", "😞": "Depression", "😔": "Depression", "🥀": "Depression", "💔": "Depression",
        "😩": "Depression", "😶": "Depression", "🖤": "Depression",
        "😰": "Anxiety", "😨": "Anxiety", "😱": "Anxiety", "🤯": "Anxiety", "🫨": "Anxiety", "😬": "Anxiety", "😖": "Anxiety",
        "🫣": "Anxiety", "🏃💨": "Anxiety",
        "😡": "Stress", "😖": "Stress", "😤": "Stress", "😵": "Stress", "🤬": "Stress", "😓": "Stress", "🤦": "Stress", "💢": "Stress",
        "😠": "Stress"
    }

    # Adjust scores based on emoji selection
    depression_adjustment = sum(1 for emoji in selected_emojis if emoji_mapping.get(emoji) == "Depression")
    anxiety_adjustment = sum(1 for emoji in selected_emojis if emoji_mapping.get(emoji) == "Anxiety")
    stress_adjustment = sum(1 for emoji in selected_emojis if emoji_mapping.get(emoji) == "Stress")

    final_scores = {
        "Depression": depression_score + depression_adjustment,
        "Anxiety": anxiety_score + anxiety_adjustment,
        "Stress": stress_score + stress_adjustment
    }

    return final_scores
"""