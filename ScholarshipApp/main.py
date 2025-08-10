from generate_essay import generate_essay, save_essay, load_resume_from_docx

def ask_user_for_details():
    # Asking for user details
    print("Please provide the following details:")

    scholarship_name = input("Enter the scholarship name: ")
    essay_question = input("Enter the essay question: ")

    # Ask for personal anecdotes or achievements (can adjust based on the scholarship)
    anecdotes = input("Enter your work anecdotes/achievements: ")

    # Ask for career goals or additional personal info
    career_goals = input("Enter your career goals or personal mission: ")

    # Load resume (assuming user has uploaded a resume.docx file)
    resume_file = input("Enter the path to your resume (resume.docx): ")
    resume_data = load_resume_from_docx(resume_file)  # Load the resume data

    return scholarship_name, essay_question, resume_data, anecdotes, career_goals

def main():
    # Step 1: Collect user input for the essay builder
    scholarship_name, essay_question, resume_data, anecdotes, career_goals = ask_user_for_details()

    # Step 2: Generate essay using GPT-4 based on the provided details
    print("Generating essay for the scholarship...")
    essay_text = generate_essay(scholarship_name, essay_question, resume_data, career_goals, anecdotes)

    # Step 3: Save the generated essay to a file
    save_essay(scholarship_name, essay_text)

    # Display the generated essay to the user for review
    print("\nGenerated Essay:")
    print(essay_text)

if __name__ == "__main__":
    main()
