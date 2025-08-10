import openai
from docx import Document
import os

# Your OpenAI API key
openai.api_key = ""
# Function to load resume from a .docx file
def load_resume_from_docx(file_path="resume.docx"):
    doc = Document(file_path)
    resume_text = ""
    for para in doc.paragraphs:
        resume_text += para.text + "\n"
    return resume_text

# Function to generate essay using GPT-3.5 (or GPT-4 if available)
def generate_essay(scholarship_title, essay_question, resume_data, career_goals, persona_info):
    prompt = f"""
    Scholarship Name: {scholarship_title}
    Essay Question: {essay_question}
    Resume: {resume_data}
    Career Goals: {career_goals}
    Persona Information: {persona_info}
    
    Write a thoughtful and compelling scholarship essay based on the above details.
    Make the tone professional and reflect the experience and goals outlined in the resume and career section.
    """

    # Using GPT-3.5 turbo model (as the new version of davinci is deprecated)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the gpt-3.5-turbo model (or gpt-4 if you have access)
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=600,  # Adjust the token count based on essay length
        temperature=0.7,  # Adjust for creativity
        n=1  # Number of responses
    )

    # Extract the essay text from the response
    essay = response['choices'][0]['message']['content'].strip()
    return essay

# Function to save the generated essay to a file
def save_essay(scholarship_title, essay_text):
    # Sanitize scholarship title for folder and file names
    folder_name = f"ScholarShipResumes/{scholarship_title.replace(' ', '_')}"
    os.makedirs(folder_name, exist_ok=True)

    # Save the essay to a text file within the respective folder
    with open(f"{folder_name}/{scholarship_title}_essay.txt", 'w') as file:
        file.write(essay_text)

# Example usage
if __name__ == "__main__":
    # Example data
    scholarship_title = "Example Scholarship"
    essay_question = "Why do you deserve this scholarship?"
    resume_data = load_resume_from_docx("resume.docx")  # Path to your resume.docx file
    career_goals = "Marcus plans to lead AI initiatives in the DOD..."  # Example career goals
    persona_info = "Marcus is a passionate technologist who believes in the power of AI."  # Example persona

    # Generate the essay
    essay = generate_essay(scholarship_title, essay_question, resume_data, career_goals, persona_info)

    # Save the generated essay
    save_essay(scholarship_title, essay)

    print("Essay generation complete and saved successfully!")
