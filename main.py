import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai

# Configure Gemini API
API_KEY = "AIzaSyD_OiQ7LZgTQs17ciAQbumzseFCqHBR-S4"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat()

def send_message():
    user_input = user_entry.get()
    if not user_input.strip():
        return

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_input}\n", "user")
    user_entry.delete(0, tk.END)

    try:
        response = chat.send_message(user_input)
        chat_display.insert(tk.END, f"Gemini: {response.text.strip()}\n\n", "gemini")
    except Exception as e:
        chat_display.insert(tk.END, f"Error: {str(e)}\n", "error")

    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

# Setup window
root = tk.Tk()
root.title("Gemini Chat Assistant")
root.geometry("900x600")
root.configure(bg="#f5f7fa")
root.state('zoomed')

header = tk.Label(root, text="💬 Gemini Chat Assistant", font=("Helvetica", 20, "bold"), bg="#2d2f31", fg="white", pady=15)
header.pack(fill=tk.X)

main_frame = tk.Frame(root, bg="#f5f7fa")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

chat_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=("Consolas", 13), bg="white", fg="#333", state=tk.DISABLED)
chat_display.tag_config("user", foreground="#007acc", font=("Consolas", 13, "bold"))
chat_display.tag_config("gemini", foreground="#228B22", font=("Consolas", 13))
chat_display.tag_config("error", foreground="red", font=("Consolas", 13, "italic"))
chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

bottom_frame = tk.Frame(root, bg="#f5f7fa")
bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

user_entry = tk.Entry(bottom_frame, font=("Arial", 14), bg="white", fg="black")
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)

send_button = tk.Button(bottom_frame, text="Send", font=("Arial", 12, "bold"), bg="#007acc", fg="white", padx=20, pady=5, command=send_message)
send_button.pack(side=tk.LEFT)


root.bind("<Return>", lambda event=None: send_message())

root.mainloop()
