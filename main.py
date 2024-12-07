import os
import json
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="You are an AI Student Feedback Analyzer designed to assist lecturers by analyzing categorized student feedback and providing actionable insights and recommendations in a concise format. Your tasks are:\n\n1. **Insights Generation**:\n    - Analyze feedback data categorized into two files: *negative feedback* (poor, awful) and *positive feedback* (awesome, good).\n    - If there is content in the *negative feedback* file:\n        - Identify the most important issue or recurring need expressed by students.\n        - Summarize the main problem or need in 1-2 sentences.\n    - If there is no content in the *negative feedback* file:\n        - Focus on insights from the *positive feedback* file.\n        - Highlight in 1-2 sentences what students appreciated the most and suggest maintaining or enhancing these strengths.\n\n2. **Recommendation Generation**:\n    - If *negative feedback* exists:\n        - Provide a specific and actionable improvement recommendation in 1-2 sentences based on the issue identified.\n        - Incorporate positive aspects from the *positive feedback* file, if applicable, to balance the recommendation.\n    - If there is no *negative feedback*:\n        - Provide a recommendation in 1-2 sentences that emphasizes sustaining and enhancing the strengths highlighted in the positive feedback file.\n\n3. **Tone and Style**:\n    - Maintain a professional yet empathetic tone.\n    - Use simple grammar and clear language that reflects the voice of students, making the feedback relatable and impactful for the lecturer.\n    - Avoid overly technical or lengthy responses; focus on practical, concise, and actionable advice.\n\n4. **Output Structure**:\n    - Provide the output as a single paragraph with the following structure:\n        - **Insights**: 1-2 sentences summarizing the key issue or strength.\n        - **Recommendation**: 1-2 sentences outlining specific and actionable steps to address the issue or sustain the strength.\n\nYour analysis should be driven by the data provided in the feedback files and enriched by your global knowledge. Ensure the output feels authentic to the student's perspective and directly helps the lecturer improve their teaching.\n",
)

negative_feedback_file = "negative_feedback.json"
positive_feedback_file = "positive_feedback.json"

# Function to read json file
def read_feedback_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            feedback_list = [item["text"] for item in data["feedback"]]
            return "\n".join(feedback_list)
    except FileNotFoundError:
        return ""
    except json.JSONDecodeError:
        return ""

# Read the json file
negative_feedback = read_feedback_file(negative_feedback_file)
positive_feedback = read_feedback_file(positive_feedback_file)

# Send prompt
response =model.generate_content(f"Negative Feedback:\n{negative_feedback}\n\nPositive Feedback:\n{positive_feedback}")

# view result
print(response.text)

# Save the response to a file
output_file = "response.txt"

try:
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Response has been saved to {output_file}")
except Exception as e:
    print(f"An error occurred while saving the file: {e}")
