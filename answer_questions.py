from browser_use import Agent, Browser, BrowserConfig, Controller
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


from browser_use import Agent, SystemPrompt

class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        # Get existing rules from parent class
        existing_rules = super().important_rules()

        # Add your custom rules
        new_rules = """
9. MOST IMPORTANT RULE:
-Input the asnwers same to same as given in <context> tag.
-Solve only one question at a step compare and find the correct question and answers in the <context>.
-Wait for the page to load completely before answering the question.

"""

        # Make sure to use this pattern otherwise the exiting rules will be lost
        return f'{existing_rules}\n{new_rules}'


answers=None

with open("answers.txt", "r", encoding='utf-8') as f:
    answers=f.read()

# Define Browser Configuration with launch options
browser_config = BrowserConfig(
    # Specify the path to your Chrome executable
    chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',  # macOS path
    # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    # For Linux, typically: '/usr/bin/google-chrome'
    headless=True,
    disable_security=True,
    # Add launch options to block images
     extra_chromium_args=[
        '--blink-settings=imagesEnabled=false',
        '--force-device-scale-factor=0.15',
    ]
)

# 2. Initialize Browser with Config
browser = Browser(config=browser_config)
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=os.getenv("GEMINI_API_KEY"))

async def main3(assigment_link):
    agent = Agent(
        task=f"<context> Questions and Answers : {answers} </context> <task> go to {assigment_link}, and answer the questions. </task> ",
        llm=llm,
        browser=browser,
        # use_vision = True,
        # use_vision_for_planner=  True,
        save_conversation_path="logs/conversation",
        max_failures=10,
        retry_delay=30,
        system_prompt_class=MySystemPrompt,
        # message_context=f"{answers}",
        # max_actions_per_step=10,

        

    )
    await agent.run(max_steps=25)
    await browser.close()

    
    

