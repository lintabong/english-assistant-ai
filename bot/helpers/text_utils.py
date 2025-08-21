
import html

def build_voice_to_text_reply(text_from_spech, response_in_json):
    return (
        f"<b>📌 Original Transcript:</b>\n"
        f"{html.escape(text_from_spech)}\n\n"
        f"<b>✅ Corrected English:</b>\n"
        f"{response_in_json['corrected_text']}\n\n"
        f"<b>📝 Scores:</b>\n"
        f"English: {response_in_json['english_score']}/100\n"
        f"Context: {response_in_json['context_score']}/100"
    )
