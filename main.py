import tkinter as tk
from tkinter import scrolledtext, messagebox, Toplevel
import google.generativeai as genai

# Configure Gemini API
API_KEY = "AIzaSyD_OiQ7LZgTQs17ciAQbumzseFCqHBR-S4"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat()

chat_history = []

def send_message():
    user_input = user_entry.get()
    if not user_input.strip():
        return

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_input}\n", "user")
    user_entry.delete(0, tk.END)

    try:
        response = chat.send_message(user_input)
        reply = response.text.strip()
        chat_display.insert(tk.END, f"Gemini: {reply}\n\n", "gemini")
        chat_history.append((user_input, reply))
    except Exception as e:
        error_msg = str(e)
        chat_display.insert(tk.END, f"Error: {error_msg}\n", "error")
        chat_history.append((user_input, f"Error: {error_msg}"))

    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

def on_enter(e):
    send_button.config(bg="#005f99")
def on_leave(e):
    send_button.config(bg="#007acc")
def on_history_enter(e):
    history_button.config(bg="#1a6d2b")
def on_history_leave(e):
    history_button.config(bg="#228B22")

def open_history_window():
    history_window = Toplevel(root)
    history_window.title("Chat History")
    history_window.geometry("1000x700")
    history_window.configure(bg="#f5f7fa")

    header = tk.Label(history_window, text="📜 Chat History", font=("Helvetica", 18, "bold"), bg="#2d2f31", fg="white", pady=10)
    header.pack(fill=tk.X)

    history_display = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, font=("Segoe UI", 12), bg="white", fg="#333", state=tk.NORMAL)
    history_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    if chat_history:
        for user_msg, bot_reply in chat_history:
            history_display.insert(tk.END, f"You: {user_msg}\n", "user")
            history_display.insert(tk.END, f"Gemini: {bot_reply}\n\n", "gemini")
    else:
        history_display.insert(tk.END, "No history yet.", "info")

    history_display.tag_config("user", foreground="#0b6fa4", font=("Segoe UI", 12, "bold"))
    history_display.tag_config("gemini", foreground="#1c8f4c", font=("Segoe UI", 12))
    history_display.tag_config("info", foreground="gray", font=("Segoe UI", 12, "italic"))
    history_display.config(state=tk.DISABLED)

    back_button = tk.Button(history_window, text="⬅ Back to Chat", font=("Arial", 12, "bold"), bg="#444", fg="white", command=history_window.destroy)
    back_button.pack(pady=10)

def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

root = tk.Tk()
root.title("Gemini Chat Assistant")
root.geometry("1000x700")
root.configure(bg="#e9ecf2")
root.state('zoomed')

# Header
header_frame = tk.Frame(root, bg="#1e1f22")
header_frame.pack(fill=tk.X)

header_label = tk.Label(header_frame, text="💬 Gemini Chat Assistant", font=("Helvetica", 22, "bold"), bg="#1e1f22", fg="white", pady=15)
header_label.pack(side=tk.LEFT, padx=20)

exit_button = tk.Button(header_frame, text="❌ Exit", font=("Arial", 12, "bold"), bg="#aa2e25", fg="white", padx=20, pady=5, command=exit_app, cursor="hand2")
exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Main Chat Area
main_frame = tk.Frame(root, bg="#e9ecf2")
main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

chat_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=("Segoe UI", 13), bg="white", fg="#222", state=tk.DISABLED, relief=tk.FLAT, borderwidth=10)
chat_display.tag_config("user", foreground="#0b6fa4", font=("Segoe UI", 13, "bold"))
chat_display.tag_config("gemini", foreground="#1c8f4c", font=("Segoe UI", 13))
chat_display.tag_config("error", foreground="red", font=("Segoe UI", 13, "italic"))
chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

bottom_frame = tk.Frame(root, bg="#e9ecf2")
bottom_frame.pack(fill=tk.X, padx=30, pady=(0, 20))

user_entry = tk.Entry(bottom_frame, font=("Segoe UI", 14), bg="white", fg="black", relief=tk.FLAT, bd=4)
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=10)

send_button = tk.Button(bottom_frame, text="Send", font=("Segoe UI", 12, "bold"), bg="#007acc", fg="white", padx=20, pady=8, relief=tk.FLAT, command=send_message, cursor="hand2")
send_button.pack(side=tk.LEFT, padx=(0, 10))
send_button.bind("<Enter>", on_enter)
send_button.bind("<Leave>", on_leave)

history_button = tk.Button(bottom_frame, text="📜 History", font=("Segoe UI", 12, "bold"), bg="#228B22", fg="white", padx=20, pady=8, relief=tk.FLAT, command=open_history_window, cursor="hand2")
history_button.pack(side=tk.LEFT)
history_button.bind("<Enter>", on_history_enter)
history_button.bind("<Leave>", on_history_leave)

root.bind("<Return>", lambda event=None: send_message())

root.mainloop()
