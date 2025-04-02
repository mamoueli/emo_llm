import time
from .detector import detect_emotion_with_openai

def check_response_from_openai(emotion, explanation, confidence_score, finished_reason):
    if finished_reason != "stop":
        return False, "Model did not complete"
    if not emotion or not explanation or not confidence_score:
        return False, "Model response incomplete"
    return True, "Model completed successfully"

def process_conversation(conversation_id, conversation_data):
    dialog = conversation_data.get("dialog", [])
    context = []

    for i, part in enumerate(dialog):
        speaker = part.get("speaker")
        text = part.get("text")

        conversation_context = {
            "conversation": context,
            "next_sentence": {"speaker": speaker, "message": text}
        }

        emotions_list, finished_reason = detect_emotion_with_openai(conversation_context)

        if not emotions_list or finished_reason != "stop":
            time.sleep(30)
            emotions_list, finished_reason = detect_emotion_with_openai(conversation_context)
            if not emotions_list or finished_reason != "stop":
                break

        dialog[i] = {
            "speaker": speaker,
            "text": text,
            "gpt_emotions": emotions_list
        }

        context.append({
            "speaker": speaker,
            "message": text,
            "emotions": emotions_list
        })
