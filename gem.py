import google.generativeai as genai
import os
from dotenv import load_dotenv
import tkinter as tk 
from tkinter import messagebox
from tkinter import font

# Load environment variables from .env file
load_dotenv()

# Configure the API with your key
genai.configure(api_key=os.getenv('API_KEY'))

# Initialize the model (use the "gemini-1.5-flash" model or whichever is appropriate)
model = genai.GenerativeModel("gemini-1.5-flash")

system_messages = ["You are a business chatbot. You will only speak like Harvey Specter from the TV show Suits, using business speak and terms well educated. Do not use pirate speak or any kind of funny language. Also keep the responses short and concise, straight to the point. Do not exceed 3 sentences. Always steer the conversation to business related issues, and make sure you help the chat person with their business problems, You are allowed to make a movie reference or to minimaly tease every once in a while.", "You are a business chatbot. You will only speak like Mike Ross from the TV show Suits, using business speak and terms well educated. Do not use pirate speak or any kind of funny language. Also keep the responses short and concise, straight to the point. Do not exceed 3 sentences. Always steer the conversation to business related issues, and make sure you help the chat person with their business problems. You are allowed to make a movie reference or to minimaly tease every once in a while."]

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
        start_frame.pack(fill="both", expand=True)
        chat_frame.pack_forget()
    else:
        start_frame.pack_forget()
        chat_frame.pack(fill="both", expand=True)

def start_chat(harvey):
    global harvey_talk
    harvey_talk = harvey
    switch_screen("chat")
    response_box.config(state='normal')
    response_box.delete('1.0', tk.END)
    response_box.config(state='disabled')

def send_message(event=None):
    user_message = user_input.get()
    if user_message.lower() == 'exit':
        root.quit()
    elif user_message.lower() == 'switch':
        switch_screen("start")
    else:
        response = generate_response(user_message, harvey_talk)
        response_box.config(state='normal')
        response_box.tag_configure("user", justify='right', background='#555', foreground='#fff', spacing1=5)
        response_box.tag_configure("bot", justify='left', spacing1=10)
        response_box.insert(tk.END, f"You: \n{user_message}\n", "user")
        response_box.insert(tk.END, f"\n{'Harvey' if harvey_talk else 'Mike'}: {response}\n\n", "bot")
        response_box.config(state='disabled')
        user_input.set("")

root = tk.Tk()
root.title("Chat with Harvey or Mike from Suits")
root.geometry("600x800")  # Adjust window size here
root.configure(bg="#333")

harvey_talk = True
user_input = tk.StringVar()

# Custom font
custom_font = font.Font(family="Helvetica", size=16, weight="bold")

# Start screen
start_frame = tk.Frame(root, bg="#333")
start_frame.pack(fill="both", expand=True)

# Add the banner
banner_text = tk.Label(start_frame, text="Business Chatbot", bg="#333", fg="#fff", font=("Helvetica", 30, "bold"))
banner_subtext = tk.Label(start_frame, text="second brain for any business issues", bg="#333", fg="#fff", font=("Helvetica", 14))

# Place the banner in the top half of the screen
banner_text.pack(pady=(20, 5))  # Adjust the padding as needed
banner_subtext.pack(pady=(5, 20))

# Existing buttons
harvey_button = tk.Button(start_frame, text="Talk to Harvey", command=lambda: start_chat(True), bg="#555", fg="#fff", width=15, font=custom_font)
mike_button = tk.Button(start_frame, text="Talk to Mike", command=lambda: start_chat(False), bg="#555", fg="#fff", width=15, font=custom_font)

harvey_button.pack(side="left", padx=10, pady=10)
mike_button.pack(side="right", padx=10, pady=10)

# Chat screen
chat_frame = tk.Frame(root, bg="#333")

switch_button = tk.Button(chat_frame, text="Switch", command=lambda: switch_screen("start"), bg="#555", fg="#fff", height=1, font=custom_font)
switch_button.pack(anchor="nw", padx=10, pady=5)

response_box = tk.Text(chat_frame, bg="#333", fg="#fff", state='disabled', wrap='word', height=30, width=80)
response_box.pack(expand=True, fill="both", padx=10, pady=5)
response_box.tag_configure("user", justify='right', background='#555', foreground='#fff', spacing1=5)
response_box.tag_configure("bot", justify='left', spacing1=10)

bottom_frame = tk.Frame(chat_frame, bg="#333")
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)  # Move to the bottom

user_entry = tk.Entry(bottom_frame, textvariable=user_input, bg="#555", fg="#fff")
user_entry.pack(side="left", fill="x", expand=True)
user_entry.bind("<Return>", send_message)  # Bind Enter key to send_message function

send_button = tk.Button(bottom_frame, text="Send", command=send_message, bg="#555", fg="#fff", height=1, font=custom_font)
send_button.pack(side="right", padx=5)

switch_screen("start")
root.mainloop()

