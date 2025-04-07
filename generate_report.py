import re
from datetime import datetime
import os

def extract_tag_content(tag_name, text, default=""):
    """Extract content between specified XML-like tags."""
    # Regex to find content between <tag_name> and </tag_name>, handling multiline
    match = re.search(f'<{tag_name}>(.*?)</{tag_name}>', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Handle self-closing or empty tags specifically for ImageLink
    if tag_name == "ImageLink":
        match_self_closing = re.search(f'<ImageLink>(.*?)</ImageLink>', text)
        if match_self_closing:
            return match_self_closing.group(1).strip()
    return default

def parse_answers_tagged(file_path):
    """Parse the answers.txt file with tagged content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into individual question blocks using the new separator
    question_blocks = re.split(r'--- Question \d+ ---', content)[1:]
    
    questions = []
    for i, block in enumerate(question_blocks, 1):
        question_text = extract_tag_content("QuestionText", block)
        options_text = extract_tag_content("Options", block)
        answer = extract_tag_content("Answer", block)
        explanation = extract_tag_content("Explanation", block)
        topics_text = extract_tag_content("Topics", block)
        image_link = extract_tag_content("ImageLink", block)

        # Process options and topics into lists
        options = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
        topics = [topic.strip() for topic in topics_text.split('\n') if topic.strip()] 
        # Alternative split if topics are comma-separated:
        # topics = [topic.strip() for topic in topics_text.split(',') if topic.strip()]
        
        questions.append({
            'number': i,
            'text': question_text,
            'options': options,
            'answer': answer,
            'explanation': explanation,
            'topics': topics,
            'image_link': image_link if image_link else None # Ensure None if empty
        })
    
    return questions

def generate_html_report(questions, output_path='report.html'):
    """Generate an HTML report from the parsed tagged questions."""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Assignment Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }}
            .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            .question {{ background-color: white; padding: 20px; margin-bottom: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .question-number {{ font-size: 1.2em; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }}
            .question-text {{ margin-bottom: 15px; font-size: 1.1em; white-space: pre-wrap; /* Preserve whitespace */ }}
            .options {{ margin-left: 20px; margin-bottom: 15px; }}
            .option {{ margin-bottom: 5px; }}
            .answer {{ background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin-top: 10px; border-left: 4px solid #4caf50; }}
            .explanation, .topics-section {{ background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin-top: 10px; border-left: 4px solid #2196f3; }}
            .explanation h4, .topics-section h4 {{ margin-top: 0; color: #1e88e5; }}
            .topics-list {{ list-style: disc; margin-left: 20px; padding-left: 0; }}
            .image-container {{ margin-top: 15px; text-align: center; }}
            .image-container img {{ max-width: 100%; height: auto; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .timestamp {{ color: #666; font-size: 0.9em; margin-top: 30px; text-align: right; }}
            h1 {{ margin-top: 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Assignment Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    """
    
    for q in questions:
        html += f"""
        <div class="question">
            <div class="question-number">Question {q['number']}</div>
            <div class="question-text">{q['text']}</div>
        """
        # Only show options section if options exist
        if q['options']:
             html += f"""
            <div class="options">
                <strong>Options:</strong>
                {''.join(f'<div class="option">{opt}</div>' for opt in q['options'])}
            </div>
            """

        html += f"""
            <div class="answer">
                <strong>Answer:</strong> {q['answer']}
            </div>
        """
        
        # Add Explanation section
        if q['explanation']:
             html += f"""
            <div class="explanation">
                 <h4>Explanation</h4>
                 <p>{q['explanation']}</p>
             </div>
             """
        
        # Add Topics section
        if q['topics']:
             html += f"""
             <div class="topics-section">
                 <h4>Related Topics</h4>
                 <ul class="topics-list">
                    {''.join(f'<li>{topic}</li>' for topic in q['topics'])}
                 </ul>
             </div>
             """

        # Add Image section
        if q['image_link']:
            # Make image link clickable and display image
            html += f"""
            <div class="image-container">
                 <p><a href="{q['image_link']}" target="_blank">View Image</a></p>
                 <img src="{q['image_link']}" alt="Question {q['number']} Image">
            </div>
            """
        
        html += "</div>" # Close question div
    
    html += f"""
        <div class="timestamp">
            Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path

def gen_report():
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    # Generate timestamp for the report filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = f'reports/assignment_report_{timestamp}.html'
    
    # Parse answers using the new tagged format parser
    try:
        questions = parse_answers_tagged('answers.txt')
        if not questions:
             print("Warning: No questions found or parsed from answers.txt. Report will be empty.")
        report_path = generate_html_report(questions, output_path)
        print(f"Report generated successfully: {report_path}")
        print("You can open the report in your web browser to view the results.")
    except FileNotFoundError:
         print("Error: answers.txt not found. Please run the main script first.")
    except Exception as e:
         print(f"An error occurred while generating the report: {e}")

# if __name__ == "__main__":
#     main() 