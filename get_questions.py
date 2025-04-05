from browser_use import Agent, Browser, BrowserConfig, Controller
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr, BaseModel
from typing import List, Optional
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


class Question(BaseModel):
    question_text: str
    options: Optional[List[str]] = None

class Questions(BaseModel):
    questions: List[Question]
browser_config = BrowserConfig(
    chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',  # macOS path
   
    extra_chromium_args=[
        # '--blink-settings=imagesEnabled=false',
        '--force-device-scale-factor=0.45'
    ]
)

browser = Browser(config=browser_config)

controller = Controller(
    output_model=Questions, 

)

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=os.getenv("GEMINI_API_KEY"))



import psutil
import os


async def main1(assigment_link):
    agent = Agent(
    task=f"go to {assigment_link}, and give me all the Questions along with their datasets/images links. For each question append the dataset/images paths to the question text download the images and save them in the images folder and append the path to the question text, and the Options to options. appends all the common data for question where mentioned with each question text",
    llm=llm,
    controller=controller,
    browser=browser,
    use_vision = True,
    save_conversation_path="logs/conversation",

    )
    history = await agent.run()
    
    final_result_json = None
    if hasattr(history, 'final_result') and callable(history.final_result):
        final_result_json = history.final_result()
    elif isinstance(history, str): # Fallback if run directly returns JSON string
        final_result_json = history
   
    print(f"\n--- Agent Final Result (JSON Attempt) ---")
    print(f"Type: {type(final_result_json)}")
    print(f"Content: {final_result_json}")
    print(f"-----------------------------------------\n")

    parsed_questions = None
    if final_result_json:
        try:
            parsed_questions = Questions.model_validate_json(final_result_json)
        except Exception as e:
            print(f"Error validating agent result with Pydantic model: {e}")

    if parsed_questions and parsed_questions.questions:
        temp_dir = "temp"
        try:
            os.makedirs(temp_dir, exist_ok=True) # Create temp directory if it doesn't exist
            print(f"Writing {len(parsed_questions.questions)} extracted questions to individual files in '{temp_dir}' directory...")
            
            for index, question_item in enumerate(parsed_questions.questions):
                filename = os.path.join(temp_dir, f"q{index + 1}.txt")
                with open(filename, 'w', encoding='utf-8') as f:
                    # Write question text
                    f.write(f"{question_item.question_text}\n")
                    # Write options if they exist
                    if question_item.options:
                        for option in question_item.options:
                            f.write(f"{option}\n")
                            
            print("Successfully wrote questions to text files.")
        except OSError as e:
            print(f"Error creating directory or writing files: {e}")
        except Exception as e:
             print(f"An unexpected error occurred during file writing: {e}")

    else:
        print("Could not extract or parse questions using the defined Pydantic model.")
        if final_result_json:
             print("Please examine the 'Agent Final Result (JSON Attempt)' printed above.")

   
    # await controller.close()
    await browser.close()

