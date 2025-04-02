import pandas as pd

# Data provided by the user
data = {
    "Model": ["gpt-4o-2024-08-06", "claude-3-5-sonnet-20240620", "llama 3"],
    "V1_Correct": [137, 129, 100],
    "V2_Correct": [141, 133, 106],
    "V3_Correct": [151, 144, 116],
    "Total": [313, 313, 313]
}

# Fine-tuned GPT result
fine_tuned_gpt_result = 0.5294

# Create a dataframe
df = pd.DataFrame(data)

# Calculate percentages for each prompt version
df['V1_Percentage'] = (df['V1_Correct'] / df['Total']) * 100
df['V2_Percentage'] = (df['V2_Correct'] / df['Total']) * 100
df['V3_Percentage'] = (df['V3_Correct'] / df['Total']) * 100

# Calculate improvement margins
df['V1_to_V2_Improvement'] = df['V2_Percentage'] - df['V1_Percentage']
df['V2_to_V3_Improvement'] = df['V3_Percentage'] - df['V2_Percentage']

# Add fine-tuned GPT data
fine_tuned_gpt_data = {
    'Model': ['Fine-Tuned GPT'],
    'V1_Correct': [None],
    'V2_Correct': [None],
    'V3_Correct': [None],
    'Total': [None],
    'V1_Percentage': [fine_tuned_gpt_result * 100],
    'V2_Percentage': [None],
    'V3_Percentage': [None],
    'V1_to_V2_Improvement': [None],
    'V2_to_V3_Improvement': [None]
}

# Append fine-tuned GPT result to the dataframe
df_fine_tuned = pd.DataFrame(fine_tuned_gpt_data)
df_combined = pd.concat([df, df_fine_tuned], ignore_index=True)

# Display the dataframe to the user
display(df_combined) # Use the display function to show the dataframe

df_combined


import matplotlib.pyplot as plt
# Adjust the number of tick locations and labels to avoid the mismatch
index = list(range(len(df['Model']) + 1))

# Set up the figure again
fig, ax = plt.subplots(figsize=(10, 6))

# Bar width for spacing
bar_width = 0.2

# Bar plots for each version
bar1 = plt.bar([i - bar_width for i in range(len(df['Model']))], df['V1_Percentage'], bar_width, label='V1 Percentage')
bar2 = plt.bar(range(len(df['Model'])), df['V2_Percentage'], bar_width, label='V2 Percentage')
bar3 = plt.bar([i + bar_width for i in range(len(df['Model']))], df['V3_Percentage'], bar_width, label='V3 Percentage')

# Add the fine-tuned GPT result as a separate bar
plt.bar([len(df['Model'])], [fine_tuned_gpt_result * 100], bar_width, label='Fine-Tuned GPT (V1)', color='orange')

# Add labels and title
plt.xlabel('Models')
plt.ylabel('Percentage Correct')
plt.title('Emotion Detection Model Performance by Prompt Version')
plt.xticks(index, df['Model'].tolist() + ['Fine-Tuned GPT'], rotation=45)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()


import json
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# Load the JSON data
file_path = '/content/modified_json_file_updated.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Initialize a counter for emotions
emotion_counter = Counter()

# Iterate through the dialogues
for dialogue_key, dialogue_value in data.items():
    # Check if 'final_emotions' section is present
    if 'final_emotions' in dialogue_value:
        final_emotions = dialogue_value['final_emotions']

        # Iterate through each part in final_emotions
        for part_key, part_value in final_emotions.items():
            # Extract the final emotion for that part
            emotion = part_value.get('final_emotion', {}).get('emotion', None)
            if emotion:
                emotion_counter[emotion] += 1

# Convert the emotion counter to a pandas DataFrame for easy visualization and manipulation
emotion_df = pd.DataFrame(emotion_counter.items(), columns=['Emotion', 'Count']).sort_values(by='Count', ascending=False)

# Display the emotion distribution statistics as a table
print("\nEmotion Distribution Table:\n")
print(emotion_df)

# Plot the emotion distribution as a bar chart
plt.figure(figsize=(10, 6))
plt.bar(emotion_df['Emotion'], emotion_df['Count'], color='skyblue')
plt.xlabel('Emotion', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('Emotion Distribution', fontsize=15)
plt.xticks(rotation=90, fontsize=10)
plt.tight_layout()

# Save the bar chart
plt.savefig('emotion_distribution_chart.png', dpi=300)

# Show the bar chart
plt.show()

# Optional: Save the table as a CSV for further use
emotion_df.to_csv('emotion_distribution.csv', index=False)

# Fixing the data by adding missing values to match the length of the longest list
# Adding `None` or zeros as needed to fill up the missing entries

data = {
    'Emotion': ['Admiration', 'Adoration', 'Aesthetic appreciation', 'Amusement', 'Anger', 'Annoyance',
                'Awkwardness', 'Boredom', 'Calmness', 'Confusion', 'Contempt', 'Disappointment', 'Disgust',
                'Embarrassment-Shame', 'Empathic pain', 'Excitement', 'Fear', 'Gratitude', 'Guilt',
                'Interest - Curiosity', 'Joy', 'Nervousness - Anxiety', 'Neutral', 'Nostalgia', 'Pride',
                'Realization', 'Relief', 'Remorse', 'Sadness', 'Satisfaction', 'Surprise', 'Sympathy', 'Triumph'],
    'ambiguous': [0, 1, 1, 1, 0, 0, 2, 2, 7, 5, 5, 0, 0, 1, 5, 0, 0, 0, 6, 73, 0, 10, 47, 1, 0, 21, 0, 0, 4, 0, 16, 1, None],
    'negative': [0, 0, 0, 0, 5, 8, 0, 0, 0, 0, 0, 20, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 13, 0, 0, 0, None, None],
    'positive': [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 4, 0, 0, 7, 0, 0, 6, 0, 9, 0, 0, 0, 0, 0, None, None]
}

# Now, creating the DataFrame
import pandas as pd

df = pd.DataFrame(data)

# Normalize the data to create more color distribution
normalized_df = df.copy()
normalized_df.iloc[:, 1:] = normalized_df.iloc[:, 1:].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

# Visualizing the normalized DataFrame using a heatmap again
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 8))
sns.heatmap(normalized_df.set_index('Emotion'), annot=False, cmap="coolwarm", cbar=True)
plt.title('Emotion Sentiment Spread - Adjusted')
plt.show()
