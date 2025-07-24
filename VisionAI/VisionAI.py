from groq import Groq
import os
from dotenv import load_dotenv
import base64
import mimetypes
import sys


load_dotenv()

client = Groq()
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
    
  
#image_path = "C:/Users/Asus/Desktop/image.jpeg"
# image2 =  "C:/Users/Asus/Desktop/img.jpeg"
print("Welcome to VisionAI! Type 'exit' to end the conversation.")

base64_image_data = None
while True:
    use_image_input = input("Do you want to provide a path to an image? (yes/no): ").lower()
    if use_image_input in ["yes","y"]:
       image_path = input("Please paste the full path to your image and press Enter: ")
       base64_image_data = encode_image(image_path)
       #print(base64_image_data)
       break
    elif use_image_input in ["no", "n"]:
        print("\nStarting text-only chat session.")
        break
    else :
        print("Invalid input. Please enter 'yes' or 'no'.")
    

messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. You can analyze images and engage in conversation."
                }
]

while True:
    user_input = input("\nyou: ")
    if not user_input.strip():
        continue
    if user_input.lower() == 'exit':
        print("VisionAI: Thankyou! Have a good day.")
        break
    user_message_content = [
       {
          "type" : "text",
          "text" : user_input
       }
    ]
    if base64_image_data:
       user_message_content.append(
        {
          "type" : "image_url",
          "image_url" :  {
                        "url": f"data:image/jpeg;base64,{base64_image_data}",
                    }
        }
    )
    messages.append(
            {
                "role" : "user",
                "content" : user_message_content
            })
    completion = client.chat.completions.create(
        messages=messages,
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        stream = True
    )

    assistent_response_content = ""

    for chunk in completion:
       if chunk.choices[0].delta.content:
          print(chunk.choices[0].delta.content,end="")
          sys.stdout.flush()
          assistent_response_content += chunk.choices[0].delta.content
    print()

    messages.append({
       "role" : "assistant",
       "content" : assistent_response_content
    })
