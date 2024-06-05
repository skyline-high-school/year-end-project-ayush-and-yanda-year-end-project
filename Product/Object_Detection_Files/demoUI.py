import tkinter as tk
from tkinter import messagebox

# Initialize variables to store the inputs
user_word = None
user_email = None

def save_input():
    global user_word, user_email
    user_word = word_entry.get()
    user_email = email_entry.get()

    if user_word and user_email:
        messagebox.showinfo("Success", "Inputs saved successfully!")
        word_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill in both fields.")

# Create the main window
root = tk.Tk()
root.title("Input Saver")

# Create and place the word label and entry
word_label = tk.Label(root, text="Enter a word:")
word_label.pack(pady=5)
word_entry = tk.Entry(root)
word_entry.pack(pady=5)

# Create and place the email label and entry
email_label = tk.Label(root, text="Enter an email:")
email_label.pack(pady=5)
email_entry = tk.Entry(root)
email_entry.pack(pady=5)

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=save_input)
submit_button.pack(pady=20)

# Run the application
root.mainloop()

# Print the stored variables after the window is closed
print(f"Word: {user_word}, Email: {user_email}")