## **SolveQL: Question Analyzer & Learning Aid**

Analyzes questions from assignment links (specifically designed for IITM online degree platform structure), generates detailed explanations, lists related topics to study, and creates an HTML report to help visualize question structure and verify understanding.

**Ethical Use Note:** This tool is intended as a learning aid to supplement your studies. Use it to understand question structures, review concepts, verify your own answers, and identify topics needing further review. **It should not be used to submit answers for graded assignments you haven't attempted yourself.** Academic integrity is crucial.

#### **Automatic Analysis and Report Generation.**

*How to start?*

1.  **Get API Key:** Obtain your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/u/0/apikey) (it's free).
2.  **Create `.env` file:** In the project's root directory, create a file named `.env` and add your API key:
    ```
    GEMINI_API_KEY='YOUR_API_KEY_HERE'
    ```
3.  **Install Dependencies:** Install the necessary libraries from `requirements.txt`:
    ```bash
    pip install -r requirements.txt 
    ```
    *(Note: Ensure you have Google Chrome installed, as the script currently relies on it.)*

4.  **Run the Script:** Execute `main.py` from your terminal:
    ```bash
    python main.py
    ```
    The script will prompt you for the assignment link. It will then proceed to:
    *   Extract questions from the link (saving temporary files in `temp/`).
    *   Use the Gemini LLM to generate a *proposed answer*, a detailed explanation, and related topics for each question, aiding comprehension.
    *   Download any images associated with questions into the `images/` directory.
    *   Save the structured, tagged output to `answers.txt`.
    *   Automatically generate an HTML report (`assignment_report_YYYYMMDD_HHMMSS.html`) in the `reports/` directory for review.

*Output Files for Review:*

*   `answers.txt`: Contains the raw, structured output from the LLM for each question (including the proposed answer, explanation, topics, etc.), using specific XML-like tags (`<QuestionText>`, `<Answer>`, `<Explanation>`, `<Topics>`, `<ImageLink>`). This file is overwritten each time `main.py` runs.
*   `reports/assignment_report_*.html`: A user-friendly HTML file visualizing the questions, options, the LLM's proposed answer, explanation, topics, and images. Useful for studying and verifying your work. A new report is generated with a timestamp each time `main.py` runs.
    *   **[View a Sample Report](reports/assignment_report_20250407_220231.html)**
*   `images/`: Stores images downloaded from questions.
*   `temp/`: Temporary storage for extracted question text (can likely be ignored or cleared).

*Demo:*

<video src="https://raw.githubusercontent.com/XERO47/IITM_ASSIG_SOLVER/main/assests/solver_demo.mp4" 
data-canonical-src="https://raw.githubusercontent.com/XERO47/IITM_ASSIG_SOLVER/main/assests/solver_demo.mp4" controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px"></video>

All contributions are welcome.

*TODO*

1.  ~~Get the answers.~~ -> ~~Generate proposed answers.~~
2.  ~~Explain the questions, topics, and solution.~~
3.  ~~Generate HTML report for visualization.~~
4.  Make relevant explanation for question based on lecture transcripts (Advanced).
5.  Improve robustness of LLM output parsing for report generation.
6.  Add support for other browsers.
7.  Add options to customize report content (e.g., hide proposed answers initially).
