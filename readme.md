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

Run main.py

```bash
python main.py
```

Demo:

<video controls src="./assests/solver_demo.mp4" title="Title" ></video>


All contributions are welcome.

*TODO*

1.  ~~Get the answers.~~ -> ~~Generate proposed answers.~~
2.  ~~Explain the questions, topics, and solution.~~
3.  ~~Generate HTML report for visualization.~~
4.  Make relevant explanation for question based on lecture transcripts (Advanced).
5.  Improve robustness of LLM output parsing for report generation.
6.  Add support for other browsers.
7.  Add options to customize report content (e.g., hide proposed answers initially).
