import json
import re

# Initialize counters for total matches and mismatches
total_matches = 0
total_mismatches = 0

# Define a mapping for cases where GPT's output may be shorter or different
emotion_mapping = {
    "interest curiosity": "Interest-Curiosity",
    "interest-curiosity": "Interest-Curiosity",
    "curiosity": "Interest-Curiosity",
    "sympathy caring": "Sympathy-Caring",
    "sympathy-caring": "Sympathy-Caring",
    "sympathy": "Sympathy-Caring",  # Map "Sympathy" to "Sympathy - Caring"
    "nervousness anxiety": "Nervousness-Anxiety",
    "nervousness": "Nervousness-Anxiety",
    "admiration":"Admiration",
    "adoration":"Adoration",
    "aesthetic appreciation":"Aesthetic Appreciation",
"amusement":"Amusement",
"anger":"Anger",
"awe":"Awe",
"awkwardness":"Awkwardness",
"boredom":"Boredom",
"calmness":"Calmness",
"confusion":"Confusion",
"contempt":"Contempt",
"desire":"Desire",
"craving":"Craving",
"disappointment":"Disappointment",
"disgust":"Disgust",
"empathic pain":"Empathic Pain",
"embarassment-shame":"Embarassment-Shame",
"envy":"Envy",
"excitement":"Excitement",
"fear":"Fear",
"gratitude":"Gratitude",
"grief":"Grief",
"guilt":"Guilt",
"horror":"Horror",
"interest-curiosity":"Interest-Curiosity",
"joy":"Joy",
"nervousness-anxiety":"Nervousness-Anxiety",
"nostalgia":"Nostalgia",
"pride":"Pride",
"relief":"Relief",
"neutral":"Neutral",
"realization":"Realization",
"sadness":"Sadness",
"satisfaction":"Satisfaction",
"surprise":"Surprise",
"sympathy-caring":"Sympathy-Caring",
"triumph":"Triumph",
"annoyance":"Annoyance",
"remorse":"Remorse"


    # Add more mappings if there are other known variations
}

def normalize_string(s):
    """Normalize string by converting to lowercase, removing spaces, and stripping special characters."""
    s = s.lower().strip()  # Convert to lowercase
    s = re.sub(r'[^a-z\s-]', '', s)  # Remove any non-alphabetic characters except hyphens and spaces
    s = re.sub(r'\s+', '', s)  # Remove all spaces
    return s

def normalize_emotion(emotion, emotion_type):
    """Normalize the emotion to match expected complex labels."""
    normalized_emotion = normalize_string(emotion)  # Normalize the input string
    print(f"{emotion_type} Emotion - Original: '{emotion}', Normalized: '{normalized_emotion}'")
    # Check if the normalized emotion is in the mapping dictionary
    return emotion_mapping.get(normalized_emotion, emotion)  # If not found, return the original emotion

def compare_emotions(gpt_emotion, final_emotion):
    """Compare two emotions after normalization."""
    normalized_gpt_emotion = normalize_emotion(gpt_emotion, emotion_type="GPT")
    normalized_final_emotion = normalize_emotion(final_emotion, emotion_type="Annotated")
    match_result = normalized_gpt_emotion == normalized_final_emotion
    match_status = "Match" if match_result else "Mismatch"
    print(f"Comparing GPT Emotion: '{normalized_gpt_emotion}' with Final Emotion: '{normalized_final_emotion}' -> {match_status}")
    return match_result


# Load the JSON data from the file
file_path = '/content/final_results_v3_gpt.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Iterate over all structures and compare emotions
for conversation_id, conversation_data in data.items():
    dialog = conversation_data.get("dialog", [])
    final_emotions = conversation_data.get("final_emotions", {})

    matches = 0
    total = len(dialog)  # Total number of emotions to compare

    # Iterate over each part in the dialog
    for i, part in enumerate(dialog):
        gpt_emotion = part.get("gpt_emotion", "")
        final_emotion = final_emotions.get(f"part_{i}", {}).get("final_emotion", {}).get("emotion", "")

        # Compare the normalized emotions
        if compare_emotions(gpt_emotion, final_emotion):
            match_status = "Match"
            matches += 1
            total_matches += 1
        else:
            match_status = "Mismatch"
            total_mismatches += 1

        # Add match status to the dialog part
        part["comparison_result"] = match_status

    # Calculate match percentage
    match_percentage = (matches / total) * 100 if total > 0 else 0

    # Add statistics to the conversation data
    conversation_data["statistics"] = {
        "matched_emotions": matches,
        "total_emotions": total,
        "match_percentage": match_percentage
    }

# Print the total number of matches and mismatches
print(f"Total Matches: {total_matches}")
print(f"Total Mismatches: {total_mismatches}")

# Save the updated data back to a new JSON file
output_file_path = '/content/stats_final_emotion_v3_gpt.json'
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)

# Provide the download link for the updated file
print(f"Updated JSON file saved and available for download: {output_file_path}")
