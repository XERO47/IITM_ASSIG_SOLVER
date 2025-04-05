from get_questions import main1
import asyncio
import os         
import sys        
import contextlib   
# from answer_questions import main3
from llm_interface import get_llm_response,get_llm_response_link
import requests 
import mimetypes 
import subprocess, signal

#
 
if __name__ == '__main__':
    print("Make sure you are logged in your accounton chrome browser. and there is NO OPEN WINDOW/INSTANCE of Chrome. \n\n For now only support for GOOGLE CHROME.\n")
    assigment_link=input("Link to assigment:")
    
    asyncio.run(main1(assigment_link))
    subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"], shell=True)
    

    lst=os.listdir("temp")
    counter=1
    
    # For storing images from questions.
    images_dir = "images" 
    os.makedirs(images_dir, exist_ok=True)

    for i in lst:
        with open(f"temp/{i}", "r", encoding='utf-8') as f: # Added encoding here too

            question=str(f.read())
            system_prompt="You are a helpful assistant that can answer questions Solve step by step.start the output with 'Answer:', nothing else.If the answer has more than 1 options, then output all the options in a new line. OR if the question asks for value, then output the single value INTEGER OR DECIMAL in a new line."
            prompt=f"Question: {question}\nAnswer:"
            link=get_llm_response_link(prompt=question)
            
            if "No link found" in link:
                answer=get_llm_response(system_prompt, prompt)
              
                with open(f"answers.txt", "a", encoding='utf-8') as j:
                    j.write(f"<Question>:\n{question} </Question>\n<Answer >:\n{answer}\n</Answer >\n\n")
                counter+=1
            else:
                # --- Download Image Logic ---
                try:
                    response = requests.get(str(link).strip(), stream=True, timeout=15) # Added timeout
                    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

                    
                    filename = link.split('/')[-1].split('?')[0].replace(" ","_").replace("\n","") # Basic parsing
                    if not filename: # Fallback filename
                         filename = f"q{counter}_image"

                    content_type = response.headers.get('content-type')
                    extension = mimetypes.guess_extension(content_type) if content_type else None

                    if extension:
                         # Ensure filename has the correct extension
                         name_part, _ = os.path.splitext(filename)
                         filename = name_part + extension
                    elif '.' not in filename: # Add a default if no extension guessed/present
                         filename += ".jpg" # Default to .jpg


                    save_path = os.path.join(images_dir, filename)
                    

                    with open(save_path, 'wb') as img_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            img_file.write(chunk)
                    

                except requests.exceptions.RequestException as e:
                    print(f"Error downloading image: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred during image download: {e}")
                answer=get_llm_response(system_prompt, prompt,"images/"+filename.strip().replace(" ","_").replace("\n",""))
                
                with open(f"answers.txt", "a", encoding='utf-8') as j:
                    j.write(f"<Question >:\n{question} </Question >\n<Answer >:\n{answer}\n</Answer >\n\n")
                counter+=1
    print("All answers have been saved to answers.txt")
    print("YOU ARE WELCOME.")
    # asyncio.run(main3(assigment_link))        


