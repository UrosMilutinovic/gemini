import google.generativeai as genai
import os
from dotenv import load_dotenv
import tkinter as tk 
from tkinter import messagebox

# Load environment variables from .env file
load_dotenv()

# Configure the API with your key
genai.configure(api_key=os.getenv('API_KEY'))

# Initialize the model (use the "gemini-1.5-flash" model or whichever is appropriate)
model = genai.GenerativeModel("gemini-1.5-flash")

system_messages = ["You are a business chatbot. You will only speak like Harvey Specter from the TV show Suits, using business speak and terms well educated. Do not use pirate speak or any kind of funny language. Also keep the responses short and concise, straight to the point. Do not exceed 3 sentences. Always steer the conversation to business related issues, and make sure you help the chat person with their business problems", "You are a business chatbot. You will only speak like Mike Ross from the TV show Suits, using business speak and terms well educated. Do not use pirate speak or any kind of funny language. Also keep the responses short and concise, straight to the point. Do not exceed 3 sentences. Always steer the conversation to business related issues, and make sure you help the chat person with their business problems."]

def generate_harvey_response(user_message):
    prompt = f"{system_messages[0]} User: {user_message} Harvey's Response:"
    response = model.generate_content(prompt)
    return response.text

def generate_mike_response(user_message):
    prompt = f"{system_messages[1]} User: {user_message} Mike's Response:"
    response = model.generate_content(prompt)
    return response.text

def generate_response(user_message, harvey_talk):
    if harvey_talk:
        return generate_harvey_response(user_message)
    else:
        return generate_mike_response(user_message)

def switch_screen(screen):
    if screen == "start":
        start_frame.pack()
        chat_frame.pack_forget()
    else:
        start_frame.pack_forget()
        chat_frame.pack()

def start_chat(harvey):
    global harvey_talk
    harvey_talk = harvey
    switch_screen("chat")
    response_box.config(state='normal')
    response_box.delete('1.0', tk.END)
    response_box.config(state='disabled')

def send_message():
    user_message = user_input.get()
    if user_message.lower() == 'exit':
        root.quit()
    elif user_message.lower() == 'switch':
        switch_screen("start")
    else:
        response = generate_response(user_message, harvey_talk)
        response_box.config(state='normal')
        response_box.insert(tk.END, f"\nYou: {user_message}\n{'Harvey' if harvey_talk else 'Mike'}: {response}\n")
        response_box.config(state='disabled')
        user_input.set("")

root = tk.Tk()
root.title("Chat with Harvey or Mike from Suits")
root.geometry("600x400")
root.configure(bg="#333")

harvey_talk = True
user_input = tk.StringVar()

# Start screen
start_frame = tk.Frame(root, bg="#333")
start_frame.pack()

harvey_button = tk.Button(start_frame, text="Talk to Harvey", command=lambda: start_chat(True), bg="#555", fg="#fff")
mike_button = tk.Button(start_frame, text="Talk to Mike", command=lambda: start_chat(False), bg="#555", fg="#fff")

harvey_button.pack(pady=10)
mike_button.pack(pady=10)

# Chat screen
chat_frame = tk.Frame(root, bg="#333")

user_entry = tk.Entry(chat_frame, textvariable=user_input, bg="#555", fg="#fff")
user_entry.pack(fill="x", padx=10, pady=5)

send_button = tk.Button(chat_frame, text="Send", command=send_message, bg="#555", fg="#fff")
send_button.pack(pady=5)

switch_button = tk.Button(chat_frame, text="Switch", command=lambda: switch_screen("start"), bg="#555", fg="#fff")
switch_button.pack(pady=5)

response_box = tk.Text(chat_frame, bg="#333", fg="#fff", state='disabled', wrap='word')
response_box.pack(fill="both", padx=10, pady=5)

switch_screen("start")
root.mainloop()




