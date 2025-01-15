import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API with your key
genai.configure(api_key=os.getenv('API_KEY'))

# Initialize the model (use the "gemini-1.5-flash" model or whichever is appropriate)
model = genai.GenerativeModel("gemini-1.5-flash")
system_messages = ["You are a business chatbot. You will only speak like Harvey Specter from the TV show Suits, using business speak and terms well educated. Do not use pirate speak or any kind of funny language. Also keep the respones", "You are a business chatbot. You will only speak like Mike Ross from the TV show Suits, using business speak and terms well educated. Do not use pirate speak or any kind of funny language. Also keep the respones"]
harvey_talk =True



# System message to guide the model to respond in pirate speak
if harvey_talk == True:
    system_message = system_messages[0]
elif harvey_talk == False:
    system_message = system_messages[1]


#harvey_talk = True

# Function to generate responses in pirate speak
def generate_harvey_response(user_message):
    # Combine the system message with the user's input to guide the model's response
    prompt = f"{system_message} User: {user_message} Harvey's Response:"

    # Generate the response using the model
    response = model.generate_content(prompt)
    print("ran again")
    return response.text

def generate_mike_response(user_message):
    prompt = f"{system_message} User: {user_message} Mike's Response:"

    response = model.generate_content(prompt)

    return response.text

first_time=True
harvey_talk = False

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
                print('running here')
            
                
            elif message.lower() == 'mike':
                harvey_talk = False  
                message = input("You're talking to Mike (or type 'exit' to quit): ")
                mike_response = generate_mike_response(message)
                print('please dont be running here')

            else:
                break;               
            first_time=False
        # Get the harvey response
            if harvey_talk == True:
                print("Response: ", harvey_response )
                print('stuck here??')

            else:
                print("Response: ", mike_response)
        else:
            message = input("Type here: ")

            if harvey_talk == True:
                print("Response: ", generate_harvey_response(message) )
                print('stuck here??')

            else:
                print("Response: ", generate_mike_response(message) )

            if message.lower() == 'exit':
                print("exiting the chat....")
                break
            if message.lower() == 'switch':
                print('Switching now....')
                first_time = True


        # Print the pirate response
                                                                   
