import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font
from generate_essay import generate_essay, save_essay, load_resume_from_docx

class EssayBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Marcus's Scholarship Essay Writer")

        # Set window size and styling
        self.root.geometry("700x600")
        self.root.config(bg="#add8e6")  # Light blue background

        # Initialize variables
        self.resume_path = ""
        self.scholarship_name = tk.StringVar()
        self.essay_question = tk.StringVar()
        self.anecdotes = tk.StringVar()
        self.career_goals = tk.StringVar()

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Heading with Facebook blue color and sans-serif font
        self.heading_label = tk.Label(self.root, text="Marcus's Scholarship Essay Writer", font=("Arial", 18, "bold"), bg="#1877F2", fg="white")
        self.heading_label.pack(fill="x", pady=20)

        # Resume upload section
        self.resume_label = tk.Label(self.root, text="Upload Resume (.docx):", font=("Arial", 12), fg="black", bg="#add8e6", highlightthickness=0)  # Transparent label
        self.resume_label.pack(pady=5)

        self.upload_button = tk.Button(self.root, text="Choose Resume", command=self.upload_resume, bg="#1877F2", fg="white", font=("Arial", 12, "bold"))
        self.upload_button.pack(pady=5)

        # Show the resume file name after it's uploaded
        self.resume_name_label = tk.Label(self.root, text="No file chosen", fg="gray", font=("Arial", 10), bg="#add8e6", highlightthickness=0)  # Transparent label
        self.resume_name_label.pack(pady=5)

        # Scholarship name (transparent label background)
        self.scholarship_label = tk.Label(self.root, text="Scholarship Name:", font=("Arial", 12), fg="black", bg="#add8e6", highlightthickness=0)  # Transparent label
        self.scholarship_label.pack(pady=5)

        self.scholarship_entry = tk.Entry(self.root, textvariable=self.scholarship_name, width=50, font=("Arial", 12), bd=0, highlightthickness=0, relief="flat", bg="white", fg="black")
        self.scholarship_entry.pack(pady=5)

        # Essay question (transparent label background)
        self.essay_question_label = tk.Label(self.root, text="Essay Question:", font=("Arial", 12), fg="black", bg="#add8e6", highlightthickness=0)  # Transparent label
        self.essay_question_label.pack(pady=5)
        
        self.essay_question_entry = tk.Entry(self.root, textvariable=self.essay_question, width=50, font=("Arial", 12), bd=0, highlightthickness=0, relief="flat", bg="white", fg="black")
        self.essay_question_entry.pack(pady=5)

        # Personal anecdotes (transparent label background)
        self.anecdotes_label = tk.Label(self.root, text="Anecdotes/Achievements:", font=("Arial", 12), fg="black", bg="#add8e6", highlightthickness=0)  # Transparent label
        self.anecdotes_label.pack(pady=5)
        
        self.anecdotes_entry = tk.Entry(self.root, textvariable=self.anecdotes, width=50, font=("Arial", 12), bd=0, highlightthickness=0, relief="flat", bg="white", fg="black")
        self.anecdotes_entry.pack(pady=5)

        # Career goals (transparent label background)
        self.career_goals_label = tk.Label(self.root, text="Career Goals:", font=("Arial", 12), fg="black", bg="#add8e6", highlightthickness=0)  # Transparent label
        self.career_goals_label.pack(pady=5)
        
        self.career_goals_entry = tk.Entry(self.root, textvariable=self.career_goals, width=50, font=("Arial", 12), bd=0, highlightthickness=0, relief="flat", bg="white", fg="black")
        self.career_goals_entry.pack(pady=5)

        # Generate Essay button
        self.generate_button = tk.Button(self.root, text="Generate Essay", command=self.generate_essay, bg="#1877F2", fg="white", font=("Arial", 12, "bold"))
        self.generate_button.pack(pady=10)

        # Text widget to display generated essay
        self.essay_output = tk.Text(self.root, height=10, width=70, font=("Arial", 12), bd=0, highlightthickness=0, bg="white", fg="black")
        self.essay_output.pack(pady=10)

        # Save Essay button
        self.save_button = tk.Button(self.root, text="Save Essay", command=self.save_essay, bg="#1877F2", fg="white", font=("Arial", 12, "bold"))
        self.save_button.pack(pady=5)

    def upload_resume(self):
        # Open file dialog to choose the resume file
        self.resume_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if self.resume_path:
            # Display the file name after it is uploaded
            self.resume_name_label.config(text=self.resume_path.split("/")[-1])
            messagebox.showinfo("Resume Uploaded", "Resume successfully uploaded!")

    def generate_essay(self):
        # Check if all inputs are filled
        if not self.resume_path or not self.scholarship_name.get() or not self.essay_question.get():
            messagebox.showerror("Input Error", "Please fill in all fields and upload your resume.")
            return
        
        # Load resume and generate the essay
        try:
            resume_data = load_resume_from_docx(self.resume_path)
            scholarship_name = self.scholarship_name.get()
            essay_question = self.essay_question.get()
            anecdotes = self.anecdotes.get()
            career_goals = self.career_goals.get()

            # Generate the essay
            essay_text = generate_essay(scholarship_name, essay_question, resume_data, career_goals, anecdotes)

            # Display the generated essay in the text box
            self.essay_output.delete(1.0, tk.END)
            self.essay_output.insert(tk.END, essay_text)

            messagebox.showinfo("Success", "Essay generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_essay(self):
        # Open file dialog to save the essay as a .txt file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                essay_text = self.essay_output.get(1.0, tk.END).strip()
                if not essay_text:
                    messagebox.showwarning("No Content", "There is no essay to save.")
                    return
                with open(file_path, "w") as file:
                    file.write(essay_text)
                messagebox.showinfo("Saved", "Essay successfully saved!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save essay: {e}")

# Main function to run the app
def main():
    root = tk.Tk()
    app = EssayBuilderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
