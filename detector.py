class Output_json_openai(BaseModel):
    emotion: str
    explanation: str
    confidence: float
# Detect emotion in dialog using OpenAI's API considering the context
def detect_emotion_with_openai(current_text):

    print(f"-- Running detect_emotion_with_openai with current text: {current_text} ")

    prompt = """
       You are an expert in human psychology and linguistics with a deep understanding of emotional nuances in conversations and written word.

You will receive a JSON input representing a conversation between Speaker A and Speaker B. Each message in the conversation includes the following fields:

"speaker": Indicates whether the speaker is A or B.
"message": The content of the conversation.
The JSON also contains a "next_sentence" that you must analyze the emotional content of. Your task is to:

1)Analyze the "next_sentence" and identify the most appropriate emotion(s) from the provided list, considering the context of the entire conversation up to that point.
2)Assign a "confidence_score" to each selected emotion (ranging from 0 to 1), indicating the intensity of that emotion.
3)Provide a brief explanation for each emotion chosen, taking into account the emotional trajectory from the preceding messages.
Allowed List of Emotions:
admiration
adoration
aesthetic appreciation
amusement
anger
awe
awkwardness
boredom
calmness
confusion
contempt
desire
craving
disappointment
disgust
empathic pain
embarassment-shame
envy
excitement
fear
gratitude
grief
guilt
horror
interest-curiosity
joy
nervousness-anxiety
nostalgia
pride
relief
neutral
realization
sadness
satisfaction
surprise
sympathy-caring
triumph
annoyance
remorse
Important: Only choose emotions from the above list. Do NOT select any emotions outside of this list. This is extremely important because later on i want to do a statistical analysis of the results and in case that the final emotion is one that is not included in the list it will result in errors.

Task Requirements:
Contextual Understanding: You must consider all previous dialog parts and their corresponding emotions to understand the context before analyzing the "next_sentence".
Emotion Selection: Select all emotions from the list that accurately represent the emotional content of the "next_sentence". If the emotions present in the text dont match those in the list, pick the closet one.
Confidence Scoring: For each emotion selected, assign a confidence score between 0 and 1 that reflects the how certain you are of your choice. If the emotional content is ambiguous, assign a lower confidence score.
Explanation: Provide a clear and concise explanation for each emotion chosen, referencing relevant parts of the "next_sentence" and the conversation context.
Output Format: Your response must be a JSON object with a key "emotions" containing a list of emotion objects. Each emotion object should have the following fields:
"emotion": The name of the emotion.
"confidence_score": The intensity score (0-1).
"explanation": The reasoning behind selecting this emotion.
Example Input:
{
  "conversation": [
    {"speaker": "A", "message": "When's your birthday?", "emotion": "interest-curiosity", "confidence_score": 0.8, "explanation": "Speaker A expresses curiosity in finding out the other person's birthday"},
    {"speaker": "B", "message": "It's just around the corner!", "emotion": "excitement", "confidence_score": 0.7, "explanation": "Speaker B responds to Speaker A's question with a sense of enthusiasm, evident by the exclamation mark. Additionally, birthdays are associated with excitement so the emotions are of that nature."}
  ],
  "next_sentence": {
    "speaker": "A",
    "message": "Can't wait to celebrate with you!"
  }
}
Example Output:
{
  "emotions": [
    {
      "emotion": "joy",
      "confidence_score": 0.9,
      "explanation": "The phrase 'Can't wait to celebrate with you!' indicates a high level of happiness and excitement about the upcoming celebration, aligning with the emotion of joy."
    },
    {
      "emotion": "excitement",
      "confidence_score": 0.85,
      "explanation": "The anticipation expressed by 'Can't wait' reflects a strong sense of excitement regarding the event. This also follows the excitement expressed by Speaker A in the previous message, reflecting the infectious nature of such emotions"
    }
  ]
}

Example Input 2:
{
    "next_sentence": {
    "speaker": "A",
    "message": "You are pissing me off!"
  }
}
Example Output 2:
{
  "emotions": [
    {
      "emotion": "anger",
      "confidence_score": 1,
      "explanation": "Without previous context to inform us of anything otherwise, it is evident that the Speaker is expressing great anger."
    }
  ]
}

Example Input 3:
{
  "conversation": [
    {"speaker": "A", "message": "What would like to have today sir?", "emotion": "neutral", "confidence_score": 0.6, "explanation": "It seems that the question is asked in a formal environment, persumably a restaurant, in which the waiter is politely asking what the customer is going to have. This indicates a level of politeness but no particular emotional content, thus the answer is "Neutral""},
    {"speaker": "B", "message": "Just a plain coffee, thanks.", "emotion": "neutral", "confidence_score": 0.8,  "explanation": "Following Speaker A's formal question, the customer politely asks for a coffee without any emotion being explicitely expressed. This indicates a neutrality as well. The fact that Speaker B asks for a drink also proves the restaurant-like setting"}
  ],
  "next_sentence": {
    "speaker": "A",
    "message": "Alright sir, I'll be right back. That's a very beautiful necklace by the way!"
  }
}
Example Output 3:
{
  "emotions": [
    {
      "emotion": "adoration",
      "confidence_score": 0.7,
      "explanation": "This sentence progresses the emotional trajectory of the dialog towards a warmer side, with the waiter expressing an adoration for the other person's accessory."
    },
    {
      "emotion": "aesthetic appreciation",
      "confidence_score": 0.9,
      "explanation": "The speaker clearly expresses an appreciation towards the aesthetically pleasing jewellery the other speaker holds"
    }
  ]
}

Instructions:

Maintain Consistent Formatting: Adhere to the JSON format with correct field names and structure to facilitate seamless integration with downstream processes.
Restrict Emotion Selection: Only use emotions from the provided list. Avoid introducing or inferring emotions not listed.
Leverage Contextual Information: Utilize the entire conversation history, including previous emotions, their confidence scores and explanations to inform your emotion detection in the "next_sentence".
Provide Clear Explanations: Your explanations should be detailed enough to justify the selected emotions, referencing specific parts of the "next_sentence" and relevant context from prior dialogs. Always have thought-out reasoning for your assumptions.

    """

    user_content = f"Current text: {current_text}" # initialize the variable with the current part from the dialog

    try:
        response = client.beta.chat.completions.parse(
          model="ft:gpt-4o-mini-2024-07-18:personal:emo3-retry:A64ekeIB", #ft:gpt-4o-2024-08-06:personal:emo:A5xlLb0u

          messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_content}, # για να γίνει το response format explicit.
          ],

          max_tokens=500,
          temperature=0, #try with temp=1
          response_format=Output_json_openai,
        )

         # Check if the response is empty or improperly formatted
        if not response or not response.choices or len(response.choices) == 0:
            print("The response from the API is empty or improperly formatted.")
            return None, "stop"

        finished_reason = response.choices[0].finish_reason

        # Log the raw response for debugging
        print(f"-- Raw API Response: {response}")

        # Accessing the content attribute directly instead of using subscripting
        result = response.choices[0].message.content

        # Parse the response content into JSON format
        try:
            result_json = json.loads(result)

            # Check if the "emotion" is a single object or a list
            if isinstance(result_json, dict) and "emotion" in result_json:
                # Convert single emotion into a list to keep consistency
                emotions = [{
                    "emotion": result_json["emotion"],
                    "confidence_score": result_json.get("confidence", None),
                    "explanation": result_json.get("explanation", None)
                }]
            else:
                # Assume it's already in a list format if returned as such
                emotions = result_json.get("emotions", [])

            # Check if emotions are returned, otherwise log and return None
            if not emotions:
                print(f"-- No emotions found in the response. Raw content: {result}")
                return None, "stop"

            return emotions, finished_reason  # Return the list of emotions and the finish reason

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw content received: {result}")
            return None, "stop"

    except Exception as e:
        print(f"API Error: {e}")
        return None, "stop"
