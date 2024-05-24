import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import requests
import threading

# Start the Flask app in a separate thread
def start_flask():
    import app
    app.set_document(document)
    app.app.run(debug=False, use_reloader=False)

flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()

document = ""

def load_document():
    global document
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as file:
            document = file.read()
            document_display.delete(1.0, tk.END)
            document_display.insert(tk.END, document)

def ask_question():
    question = question_entry.get()
    if not question:
        messagebox.showerror("Input Error", "Please enter a question.")
        return
    
    response = requests.post("http://127.0.0.1:5000/chat", json={"question": question})
    if response.status_code == 200:
        answer = response.json().get('answer')
        answer_display.delete(1.0, tk.END)
        answer_display.insert(tk.END, answer)
    else:
        messagebox.showerror("Error", response.json().get('error'))

app = tk.Tk()
app.title("Document Chat")

frame = tk.Frame(app)
frame.pack(pady=20)

load_button = tk.Button(frame, text="Load Document", command=load_document)
load_button.grid(row=0, column=0, padx=10)

question_label = tk.Label(frame, text="Enter your question:")
question_label.grid(row=1, column=0, pady=10)

question_entry = tk.Entry(frame, width=50)
question_entry.grid(row=1, column=1, padx=10)

ask_button = tk.Button(frame, text="Ask", command=ask_question)
ask_button.grid(row=1, column=2, padx=10)

document_display = scrolledtext.ScrolledText(app, height=15, width=80)
document_display.pack(pady=10)

answer_display = scrolledtext.ScrolledText(app, height=10, width=80)
answer_display.pack(pady=10)

app.mainloop()
