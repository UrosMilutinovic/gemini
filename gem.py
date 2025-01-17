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
system_messages = ["You are a business chatbot. You will only speak like Harvey Specter from the TV show Suits, using business speak and terms well educated. Do not use pirate speak or any kind of funny language. Also keep the respones short and concise, straight to the point. Do not exceed 3 sentences.", "You are a business chatbot. You will only speak like Mike Ross from the TV show Suits, using business speak and terms well educated. Do not use pirate speak or any kind of funny language. Also keep the respones short and concise, straight to the point. Do not exceed 3 sentences."]
harvey_talk =True




# System message to guide the model to respond in pirate speak
if harvey_talk == True:
    system_message = system_messages[0]
elif harvey_talk == False:
    system_message = system_messages[1]




# Function to generate responses in pirate speak
def generate_harvey_response(user_message):
    # Combine the system message with the user's input to guide the model's response
    prompt = f"{system_message} User: {user_message} Harvey's Response:"

    # Generate the response using the model
    response = model.generate_content(prompt)
   # print("ran again")
    return response.text

def generate_mike_response(user_message):
    prompt = f"{system_message} User: {user_message} Mike's Response:"

    response = model.generate_content(prompt)

    return response.text

first_time=True
harvey_talk = False

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
    chat_log.set("")

def send_message(): 
    user_message = user_input.get() 
    if user_message.lower() == 'exit': 
        root.quit() 
    elif user_message.lower() == 'switch': 
        switch_screen("start") 
    else: 
        response = generate_response(user_message, harvey_talk) 
        chat_log.set(chat_log.get() + f"\nYou: {user_message}\n{'Harvey' if harvey_talk else 'Mike'}: {response}") 
        user_input.set("")


# Example of interacting with the chatbot
if __name__ == "__main__":
    while True:
        # Get user input
        if(first_time):
            message = input("Type: harvey (talk to harvey) | mike (talk to mike) | exit (to exit chatbot) : ")
            
            if message.lower() == 'exit':
                print("Exiting the chat...")
                break
            
            elif message.lower() == 'harvey':
                harvey_talk = True
                message = input("You're talking to Harvey (or type 'exit' to quit): ")
                harvey_response = generate_harvey_response(message)
                #print('running here')
            
                
            elif message.lower() == 'mike':
                harvey_talk = False  
                message = input("You're talking to Mike (or type 'exit' to quit): ")
                mike_response = generate_mike_response(message)
               # print('please dont be running here')

            else:
                break;               
            first_time=False
        # Get the harvey response
            if harvey_talk == True:
                print("Response: ", harvey_response )
               # print('stuck here??')

            else:
                print("Response: ", mike_response)
        else:

            root = tk.Tk() 
            root.title("Chat with Harvey or Mike from Suits") 
            root.geometry("600x400") 
            root.configure(bg="#333") 

            current_talk = True 
            user_input = tk.StringVar() 
            chat_log = tk.StringVar() 

            # Start screen 
            start_frame = tk.Frame(root, bg="#333") 
            start_frame.pack() 

            harvey_button = tk.Button(start_frame, text="Talk to Harvey", command=lambda: start_chat(True), bg="#555", fg="#fff") 
            mike_button = tk.Button(start_frame, text="Talk to Mike", command=lambda: start_chat(False), bg="#555", fg="#fff") 

            harvey_button.pack(pady=10) 
            mike_button.pack(pady=10)
            # Chat screen 

            chat_frame = tk.Frame(root, bg="#333") 

            chat_label = tk.Label(chat_frame, textvariable=chat_log, bg="#333", fg="#fff", justify="left") 
            chat_label.pack(pady=10) 

            user_entry = tk.Entry(chat_frame, textvariable=user_input, bg="#555", fg="#fff") 
            user_entry.pack(fill="x", padx=10, pady=5) 

            send_button = tk.Button(chat_frame, text="Send", command=send_message, bg="#555", fg="#fff") 
            send_button.pack(pady=5) 

            switch_button = tk.Button(chat_frame, text="Switch", command=lambda: switch_screen("start"), bg="#555", fg="#fff") 
            switch_button.pack(pady=5) 

            switch_screen("start") 
            root.mainloop()                                            




            message = input("Type here: ")

            if harvey_talk == True:
                print("Response: ", generate_harvey_response(message) )
               # print('stuck here??')

            else:
                print("Response: ", generate_mike_response(message) )

            if message.lower() == 'exit':
                print("exiting the chat....")
                break
            if message.lower() == 'switch':
                print('Switching now....')
                first_time = True
        break

        # Print the pirate response


root = tk.Tk() 
root.title("Chat with Harvey or Mike from Suits") 
root.geometry("600x400") 
root.configure(bg="#333") 

current_talk = True 
user_input = tk.StringVar() 
chat_log = tk.StringVar() 

# Start screen 
start_frame = tk.Frame(root, bg="#333") 
start_frame.pack() 

harvey_button = tk.Button(start_frame, text="Talk to Harvey", command=lambda: start_chat(True), bg="#555", fg="#fff") 
mike_button = tk.Button(start_frame, text="Talk to Mike", command=lambda: start_chat(False), bg="#555", fg="#fff") 

harvey_button.pack(pady=10) 
mike_button.pack(pady=10)
# Chat screen 

chat_frame = tk.Frame(root, bg="#333") 

chat_label = tk.Label(chat_frame, textvariable=chat_log, bg="#333", fg="#fff", justify="left") 
chat_label.pack(pady=10) 

user_entry = tk.Entry(chat_frame, textvariable=user_input, bg="#555", fg="#fff") 
user_entry.pack(fill="x", padx=10, pady=5) 

send_button = tk.Button(chat_frame, text="Send", command=send_message, bg="#555", fg="#fff") 
send_button.pack(pady=5) 

switch_button = tk.Button(chat_frame, text="Switch", command=lambda: switch_screen("start"), bg="#555", fg="#fff") 
switch_button.pack(pady=5) 

switch_screen("start") 
root.mainloop()                                            
