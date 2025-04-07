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
from generate_report import gen_report
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

    # Clear or create answers.txt before starting
    with open("answers.txt", "w", encoding='utf-8') as j:
        j.write("") # Start with an empty file

    for i in lst:
        question_text_raw = "" # Initialize variable to store question text
        with open(f"temp/{i}", "r", encoding='utf-8') as f:
            question_text_raw = f.read() # Store the raw question text

        # --- NEW STRUCTURED SYSTEM PROMPT with Original Content Request ---
        system_prompt = """You are a helpful assistant. Solve the question step-by-step.

IMPORTANT: Format your final output EXACTLY as follows, wrapping each section in the specified tags:

<QuestionText>
[Paste the original question text here]
</QuestionText>

<Options>
[Paste option 1 here, if applicable]
[Paste option 2 here, if applicable]
...
</Options>

<Answer>
[Write the text of the single correct answer or the calculated value here]
</Answer>

<Explanation>
[Provide a short explanation of the steps to solve the answer]
</Explanation>

<Topics>
[List related topics, comma-separated or one per line]
</Topics>

<ImageLink>[Paste the image link here if provided, otherwise leave empty]</ImageLink>

Only output the content within these tags. Do not add any other text, introductions, or conclusions."""

        prompt = f"Solve the following question (details might be in the system prompt context or image):\n{question_text_raw}" # Keep prompt simple

        image_link = get_llm_response_link(prompt=question_text_raw) # Check for image link first
        image_path_for_llm = None
        image_link_for_output = "" # Initialize image link for the final output

        if "No link found" not in image_link:
            image_link_for_output = str(image_link).strip()
            # --- Download Image Logic (keep as is) ---
            try:
                response = requests.get(image_link_for_output, stream=True, timeout=15)
                response.raise_for_status()
                filename = image_link_for_output.split('/')[-1].split('?')[0].replace(" ","_").replace("\n","")
                if not filename: filename = f"q{counter}_image"
                content_type = response.headers.get('content-type')
                extension = mimetypes.guess_extension(content_type) if content_type else None
                if extension: name_part, _ = os.path.splitext(filename); filename = name_part + extension
                elif '.' not in filename: filename += ".jpg"
                save_path = os.path.join(images_dir, filename)
                with open(save_path, 'wb') as img_file:
                    for chunk in response.iter_content(chunk_size=8192): img_file.write(chunk)
                image_path_for_llm = save_path
            except requests.exceptions.RequestException as e: print(f"Error downloading image for q{counter}: {e}")
            except Exception as e: print(f"An unexpected error occurred during image download for q{counter}: {e}")

        # --- Call LLM to get the structured answer ---
        structured_answer_block = get_llm_response(system_prompt, prompt, image_path_for_llm if image_path_for_llm else None)

        # --- Write the raw LLM output (now expected to be tagged) --- 
        # Remove the previous post-processing block
        with open(f"answers.txt", "a", encoding='utf-8') as j:
            j.write(f"--- Question {counter} ---\n") # Use a clear separator
            # Ensure the correct ImageLink is embedded if the LLM didn't include it
            # This is a simple check; more robust parsing could be added.
            if "<ImageLink>" not in structured_answer_block:
                 # Try to inject it before the end
                 lines = structured_answer_block.strip().split('\n')
                 lines.append(f"<ImageLink>{image_link_for_output}</ImageLink>")
                 structured_answer_block = '\n'.join(lines)
            elif "<ImageLink></ImageLink>" in structured_answer_block and image_link_for_output:
                 # Fill empty tag if we have a link
                 structured_answer_block = structured_answer_block.replace("<ImageLink></ImageLink>", f"<ImageLink>{image_link_for_output}</ImageLink>")
            
            # Ensure QuestionText is present
            if "<QuestionText>" not in structured_answer_block:
                 lines = structured_answer_block.strip().split('\n')
                 lines.insert(0, f"<QuestionText>\n{question_text_raw.strip()}\n</QuestionText>")
                 structured_answer_block = '\n'.join(lines)

            j.write(structured_answer_block.strip()) 
            j.write("\n\n") # Add blank lines between questions

        counter+=1

    print("All answers have been saved to answers.txt in a structured format.")
    gen_report()
    print("And the reports are saved in reports folder.")
    print("YOU ARE WELCOME.")
    # asyncio.run(main3(assigment_link))      


