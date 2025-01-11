import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from functools import partial
import datetime
from pathlib import Path
import image_to_pdf
from todo_manager import delete_old, add_activity, get_activities
from date_time import gettime, getdate
from speak import speak
from web_search import search, give_recommendations, add_search_to_history
from sumarize import summarize_text

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greet = "Good morning!"
    elif 12 <= hour < 18:
        greet = "Good afternoon!"
    else:
        greet = "Good evening!"
    speak(greet)
    print(greet)


def display_summary_window(summary):
    # Create a new window to display the summary nicely
    summary_window = tk.Toplevel(root)
    summary_window.title("Summary")
    summary_window.geometry("600x400")
    summary_window.configure(bg="#f0f0f0")
    
    # Add title label
    tk.Label(summary_window, text="Summary of Your Text:", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    
    # Add a scrollable Text widget to display the summary
    summary_text = tk.Text(summary_window, font=("Arial", 12), width=70, height=12, wrap=tk.WORD, bg="#f5f5f5", padx=10, pady=10)
    summary_text.insert(tk.END, summary)
    summary_text.config(state=tk.DISABLED)  # Make it non-editable
    summary_text.pack(pady=10)
    
    # Add a close button
    close_button = tk.Button(summary_window, text="Close", command=summary_window.destroy, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
    close_button.pack(pady=20)

def summarize_gui():
    speak("Please introduce the text you want to summarize!")

    # Creating a new top-level window for text input
    summarize_window = tk.Toplevel(root)
    summarize_window.title("Summarize Text")
    summarize_window.geometry("500x400")
    summarize_window.configure(bg="#f0f0f0")
    
    # Adding a label for instructions
    tk.Label(summarize_window, text="Please enter the text to summarize:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)

    # Creating a text box for multi-line text input
    text_box = tk.Text(summarize_window, font=("Arial", 12), width=40, height=8, wrap=tk.WORD)
    text_box.pack(pady=10)
    
    # Function to handle summarization
    def submit_text():
        text = text_box.get("1.0", tk.END).strip()  # Get text from the Text widget
        if text:
            summary = summarize_text(text)  # Summarize the input text
            speak("Here is the summary.")
            display_summary_window(summary)  # Show the summarized text
        else:
            speak("No text provided for summarization.")
            messagebox.showinfo("Error", "No text was provided. Please enter some text to summarize.")

    # Adding a submit button with a professional design
    submit_button = tk.Button(summarize_window, text="Summarize", command=submit_text, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15)
    submit_button.pack(pady=20)

    # Wait for the window to close and then return to the main loop
    summarize_window.mainloop()

def output_pdf_name_gui():
    # Creating a custom top-level window for the PDF name input
    output_window = tk.Toplevel(root)
    output_window.title("Enter PDF Name")
    output_window.geometry("400x200")
    output_window.configure(bg="#f0f0f0")
    
    # Adding a label for instruction
    tk.Label(output_window, text="Enter a name for the PDF:", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
    
    # Entry field for PDF name input
    pdf_name_entry = tk.Entry(output_window, font=("Arial", 12), width=30, justify="center")
    pdf_name_entry.pack(pady=10)

    name = None

    # Function to submit the PDF name
    def submit_pdf_name():
        nonlocal name
        pdf_name = pdf_name_entry.get().strip()
        if not pdf_name:
            pdf_name = "Newpdf.pdf"
        name = pdf_name
        output_window.destroy()

    # Add a submit button with a nice design
    submit_button = tk.Button(output_window, text="Confirm", command=submit_pdf_name, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15)
    submit_button.pack(pady=20)
    
    output_window.wait_window(output_window)
    return name

def images_to_pdf_gui():
    speak("Select the folder where the images are stored!")
    image_folder = filedialog.askdirectory(title="Select Image Folder")
    if not image_folder:
        speak("Image folder was not selected")
        return
    speak("Select the folder where you want to store the newly created pdf!")
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        speak("Output folder was not selected")
        return
    speak("Choose a name for the new pdf!")
    output_pdf_name = output_pdf_name_gui() # output_pdf_name = simpledialog.askstring("Output PDF", "Enter name for the output PDF (e.g., Newpdf.pdf):", parent=root)
    if not output_pdf_name:
        output_pdf_name = "Newpdf.pdf"
    image_to_pdf.images_to_pdf(image_folder, output_folder, output_pdf_name)
    messagebox.showinfo("Images to PDF", f"PDF saved successfully as {os.path.join(output_folder, output_pdf_name)}")

def open_link(link, domain):
    import webbrowser
    webbrowser.open(link)
    speak(f"Opening {domain}")

def search_button_activation(link, domain, query):
    open_link(link, domain)
    add_search_to_history(link, domain, query)

def give_recommendations_gui():
    speak("Here is a list of recommendations based on your search history!")
    recommendations = give_recommendations()
    if recommendations:
        rec_window = tk.Toplevel(root)
        rec_window.title("Recommendations")
        rec_window.configure(bg="#f0f0f0")
        tk.Label(rec_window, text="Here are some recommendations based on your search history:", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=10)
        for topic, link, domain in recommendations:
            btn = tk.Button(rec_window, text=f"Topic: {topic} - Link: {link} - Domain: {domain}", wraplength=350,
                            command=partial(open_link, link, domain), bg="#ffffff", relief=tk.RIDGE)
            btn.pack(pady=5, padx=10, anchor='w')
    else:
        speak("No recommendations available.")
        messagebox.showinfo("Recommendations", "No recommendations available.")

def search_gui():
    speak("Please enter the text you want to search for!")

    # Creating a new top-level window for text input
    search_window = tk.Toplevel(root)
    search_window.title("Search Information")
    search_window.geometry("500x400")
    search_window.configure(bg="#f0f0f0")

    # Adding a label for instructions
    tk.Label(search_window, text="Please enter your search query:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)

    # Creating a text box for multi-line text input
    search_box = tk.Entry(search_window, font=("Arial", 12), width=40, bd=2, relief="solid", 
                           borderwidth=1, highlightthickness=1, highlightcolor="#007BFF", highlightbackground="#d6d6d6")
    search_box.pack(pady=10)

    # Function to handle search
    def submit_search():
        query = search_box.get().strip()  # Get text from the Entry widget
        if query:
            search_results = search(query)  # Perform the search
            choose_and_open_link_gui(search_results, query)  # Handle the search results
        else:
            speak("No search query provided.")
            messagebox.showinfo("Error", "Please enter a search query to proceed.")

    # Adding a submit button with a professional design
    submit_button = tk.Button(search_window, text="Search", command=submit_search, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15)
    submit_button.pack(pady=20)

    # Wait for the window to close and then return to the main loop
    search_window.mainloop()

def choose_and_open_link_gui(search_results, query):
    if not search_results:
        speak("No search results found.")
        messagebox.showinfo("Search Results", "No search results found.")
        return

    result_window = tk.Toplevel(root)
    result_window.title("Search Results")
    result_window.configure(bg="#f0f0f0")

    tk.Label(result_window, text=f"Search results for '{query}':", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=10)

    speak("Here are the results of your search!")
    for idx, (link, domain) in enumerate(search_results, start=1):
        btn = tk.Button(result_window, text=f"{idx}. {link} - {domain}", wraplength=350,
                        command=partial(search_button_activation, link, domain, query), bg="#ffffff", relief=tk.RIDGE)
        btn.pack(pady=5, padx=10, anchor='w')

def add_task_gui():
    def submit_task():
        activity = activity_entry.get()
        day_of_week = day_of_week_entry.get()
        time = time_entry.get()
        day_of_month = day_of_month_entry.get()
        month = month_entry.get()
        year = year_entry.get()

        task = activity + "," + day_of_week + "," + time + "," + day_of_month + "," + month + "," + year
        add_activity(task)

    window = tk.Toplevel(root)
    window.title("Add New Task")
    window.geometry("400x500")
    window.configure(bg="#f0f0f0")

    speak("Please introduce the task details!")
    tk.Label(window, text="Enter Task Details", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

    tk.Label(window, text="Activity:", bg="#f0f0f0").pack(anchor="w", padx=20)
    activity_entry = tk.Entry(window, width=40)
    activity_entry.pack(pady=5)

    tk.Label(window, text="Day of Week (e.g., Monday):", bg="#f0f0f0").pack(anchor="w", padx=20)
    day_of_week_entry = tk.Entry(window, width=40)
    day_of_week_entry.pack(pady=5)

    tk.Label(window, text="Time (HH:MM):", bg="#f0f0f0").pack(anchor="w", padx=20)
    time_entry = tk.Entry(window, width=40)
    time_entry.pack(pady=5)

    tk.Label(window, text="Day of Month (number):", bg="#f0f0f0").pack(anchor="w", padx=20)
    day_of_month_entry = tk.Entry(window, width=40)
    day_of_month_entry.pack(pady=5)

    tk.Label(window, text="Month (e.g., january):", bg="#f0f0f0").pack(anchor="w", padx=20)
    month_entry = tk.Entry(window, width=40)
    month_entry.pack(pady=5)

    tk.Label(window, text="Year:", bg="#f0f0f0").pack(anchor="w", padx=20)
    year_entry = tk.Entry(window, width=40)
    year_entry.pack(pady=5)

    submit_button = tk.Button(window, text="Add Task", command=submit_task, bg="#4CAF50", fg="white", font=("Arial", 12))
    submit_button.pack(pady=20)


def get_tasks_gui():
    all_tasks = get_activities()  # Assuming this function returns a list of tasks

    # Create the window for displaying today's tasks
    rec_window = tk.Toplevel(root)
    rec_window.title("Today's Tasks")
    rec_window.geometry("700x450")
    rec_window.configure(bg="#f4f4f9")

    # Title label (centered and bold)
    title_label = tk.Label(rec_window, text="Your Tasks for Today", font=("Helvetica", 22, "bold"), bg="#f4f4f9", fg="#333333")
    title_label.pack(pady=20)

    # If there are no tasks, show a message
    if not all_tasks:
        speak("No tasks for today.")
        messagebox.showinfo("Tasks", "You don't have any tasks for today.")
        return

    # Create a canvas to add scrolling capability
    canvas = tk.Canvas(rec_window)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar
    scrollbar = tk.Scrollbar(rec_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the task cards inside the canvas
    task_frame = tk.Frame(canvas, bg="#f4f4f9", padx=20)
    canvas.create_window((0, 0), window=task_frame, anchor="nw")

    # Styling for the task cards
    card_style = {
        'bg': '#ffffff',
        'fg': '#333333',
        'font': ('Helvetica', 14),
        'relief': 'flat',
        'borderwidth': 1,
        'width': 45,
        'height': 2,
        'pady': 10,
        'padx': 20,
        'font_color': '#333333',
        'border_color': '#d6d6d6',
        'hover_color': '#007BFF',  # For hover effect (Professional Blue)
        'transition_speed': 200  # Smooth transition speed for hover effects
    }

    # Populate the frame with task cards
    def on_hover_in(btn):
        btn.config(bg=card_style['hover_color'], fg='white')

    def on_hover_out(btn):
        btn.config(bg=card_style['bg'], fg=card_style['font_color'])

    for activity in all_tasks:
        task_button = tk.Button(
            task_frame,
            text=f"• {activity}",
            font=card_style['font'],
            bg=card_style['bg'],
            fg=card_style['font_color'],
            relief=card_style['relief'],
            width=card_style['width'],
            height=card_style['height'],
            pady=card_style['pady'],
            padx=card_style['padx'],
            bd=card_style['borderwidth'],
            highlightthickness=0,
            activebackground=card_style['hover_color'],
            activeforeground='white'
        )

        # Add hover effect with smooth transitions
        task_button.bind("<Enter>", lambda event, btn=task_button: on_hover_in(btn))
        task_button.bind("<Leave>", lambda event, btn=task_button: on_hover_out(btn))
        task_button.pack(pady=15, fill="x")

    # Update the scrollbar
    task_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def main():
    greet_user()
    delete_old()

    global root
    root = tk.Tk()
    root.title("Assistant GUI")
    root.geometry("400x500")
    root.configure(bg="#f0f0f0")

    header = tk.Label(root, text="Virtual Assistant", font=("Arial", 20, "bold"), bg="#3B5998", fg="white")
    header.pack(fill="x", pady=10)

    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=20)

    buttons = [
        ("Search the Web", search_gui),
        ("Get Recommendations", give_recommendations_gui),
        ("Images to PDF", images_to_pdf_gui),
        ("Summarize Text", summarize_gui),
        ("Add New Task", add_task_gui),
        ("Today's Tasks", get_tasks_gui),
        ("Exit", root.quit)
    ]

    for text, command in buttons:
        tk.Button(button_frame, text=text, command=command, width=30, height=2, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

