from google import genai
from google.genai import types, errors
from tkinter import messagebox

client = genai.Client()

def get_response_ai(prompt, param, parent_widget=None):
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=param),
        )
        return response.text
    except errors.APIError as e:

        if parent_widget:
            parent_widget.after(0, lambda: messagebox.showerror("Errore API", e.message))
        else:

            messagebox.showerror("Errore API", e.message)

        raise e


