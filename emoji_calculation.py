def calculate_emojis_scores(selected_emojis):
    # Define emoji weights (consistent lowercase keys)
    emoji_weight = {
        "😡": "stress", "😖": "anxiety","😤": "stress", "😰": "anxiety",
        "😨": "anxiety", "😱": "anxiety","😢": "depression", "😭": "depression",
        "😞": "depression", "🤬": "stress", "😵": "anxiety", "😠": "stress",
        "😬": "anxiety", "🫣": "anxiety", "😔": "depression", "🥀": "depression",
        "💔": "depression", "💢": "stress", "😓": "stress", "🤦": "stress",
        "😧": "anxiety", "🏃💨": "anxiety", "😩": "depression", "🖤": "depression",
        "😶": "depression","😩": "stress","🤯": "stress",
        "🙂": "normal", "😁": "normal", "😏": "normal", "😇 ": "normal", "🤗": "normal", "😊": "normal", "😄": "normal", "😎": "normal", "😆": "normal",
    }

    # Initialize the count dictionary
    emoji_count = {"depression": 0, "anxiety": 0, "stress": 0, "normal": 0}

    # Count occurrences of each category
    for emoji in selected_emojis:
        category = emoji_weight.get(emoji)
        if category:
            emoji_count[category] += 1  # Increment count for respective category

    return emoji_count  # Return the count dictionary
