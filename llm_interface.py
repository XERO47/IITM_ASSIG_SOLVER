from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_llm_response(system_prompt, prompt,image_path=None):
    global client
    img_path = image_path
    response=None
    modeln="gemini-2.0-flash-thinking-exp"
    if img_path is not None:
        
        file_ref = client.files.upload(file=img_path)
        response = client.models.generate_content(
            # model="gemini-2.5-pro-exp-03-25",
            model=modeln,
            config=types.GenerateContentConfig(
                system_instruction=f"{system_prompt}"),
            contents=[f"{prompt}",file_ref]
        )
    else:
        response = client.models.generate_content(
            # model="gemini-2.5-pro-exp-03-25",
            model=modeln,
            config=types.GenerateContentConfig(
                system_instruction=f"{system_prompt}"),
            contents=[f"{prompt}"]
        )

    return response.text


def get_llm_response_link(model="gemini-1.5-flash-8b-exp-0827",system_prompt=None, prompt=None):
    global client
    response = client.models.generate_content(
        model=f"{model}",
        # config=types.GenerateContentConfig(
        #     system_instruction=f"{system_prompt}"),
        contents=f"if there is a link(link means hyperlink, weblink) in the text, then output the link, otherwise output 'No link found', Dont output anything else. Text: {prompt}"
    )

    return response.text

# print(get_llm_response_link(prompt="if there is a link in the text, then output the link, otherwise output 'No link found', Dont output anything else. Text: "))