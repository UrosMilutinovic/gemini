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
        response_box.tag_configure("user", justify='right', background='#AECCE4', foreground='#fff', spacing1=5)  # Change to light blue
        response_box.tag_configure("bot", justify='left', spacing1=10)
        response_box.insert(tk.END, f"\n{user_message}\n", "user")
        response_box.insert(tk.END, f"\n{'Harvey' if harvey_talk else 'Mike'}: {response}\n\n", "bot")
        response_box.config(state='disabled')
        user_input.set("")

root = tk.Tk()
root.title("Chat with Harvey or Mike from Suits")
root.geometry("600x800")  # Adjust window size here
root.configure(bg="#003366")  # Dark blue background

harvey_talk = True
user_input = tk.StringVar()

# Custom font
custom_font = font.Font(family="Helvetica", size=16, weight="bold")

# Start screen
start_frame = tk.Frame(root, bg="#003366")  # Dark blue background
start_frame.pack(fill="both", expand=True)

# Add the banner
banner_text = tk.Label(start_frame, text="Business Chatbot", bg="#003366", fg="#fff", font=("Helvetica", 30, "bold"))
banner_subtext = tk.Label(start_frame, text="Second Brain For Any Business Issues", bg="#003366", fg="#fff", font=("Helvetica", 14))

# Place the banner in the top half of the screen
banner_text.pack(pady=(50, 5))  # Adjust the padding as needed
banner_subtext.pack(pady=(5, 40))

# Existing buttons
harvey_button = tk.Button(start_frame, text="Talk to Harvey", command=lambda: start_chat(True), bg="#336699", fg="#fff", width=15, font=custom_font)  # Medium blue background
mike_button = tk.Button(start_frame, text="Talk to Mike", command=lambda: start_chat(False), bg="#336699", fg="#fff", width=15, font=custom_font)  # Medium blue background

harvey_button.pack(side="left", padx=30, pady=5)
mike_button.pack(side="right", padx=30, pady=5)

# Chat screen
chat_frame = tk.Frame(root, bg="#003366")  # Dark blue background

switch_button = tk.Button(chat_frame, text="Switch / Home", command=lambda: switch_screen("start"), bg="#336699", fg="#fff", height=1, font=custom_font)  # Medium blue background
switch_button.pack(anchor="nw", padx=10, pady=5)

# Create Canvas for rounded corners
canvas = tk.Canvas(chat_frame, bg="#003366", highlightthickness=0)
canvas.pack(expand=True, fill="both", padx=10, pady=5)

# Draw a rounded rectangle on the canvas
def create_rounded_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Define rounded rectangle with desired attributes
rounded_rect = create_rounded_rectangle(10, 10, 580, 580, radius=25, fill="#003366", outline="white", width=3)

# Create the Text widget on top of the canvas
response_box = tk.Text(canvas, bg="#003366", fg="#fff", state='disabled', wrap='word', height=20, width=80, bd=0, highlightthickness=0, padx=15, pady=15)
response_box.place(x=20, y=20, width=560, height=560)
response_box.tag_configure("user", justify='right', background='#ADD8E6', foreground='#fff', spacing1=5)  # Light blue background
response_box.tag_configure("bot", justify='left', spacing1=10)

bottom_frame = tk.Frame(chat_frame, bg="#003366")  # Dark blue background
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)  # Move to the bottom

user_entry = tk.Entry(bottom_frame, textvariable=user_input, bg="#336699", fg="#fff")  # Medium blue background
user_entry.pack(side="left", fill="x", expand=True)
user_entry.bind("<Return>", send_message)  # Bind Enter key to send_message function

send_button = tk.Button(bottom_frame, text="Send", command=send_message, bg="#336699", fg="#fff", height=1, font=custom_font)  # Medium blue background
send_button.pack(side="right", padx=5)

switch_screen("start")
root.mainloop()
