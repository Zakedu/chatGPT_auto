import tkinter as tk
import openai

def askGPT(text):
    openai.api_key = "1234"
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = text,
        temperature = 0.6,
        max_tokens = 150,
    )
    return response.choices[0].text

def get_response():
    input_text = input_box.get("1.0", tk.END)
    response_text = askGPT(input_text)
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, response_text)
    output_box.config(state=tk.DISABLED)

# create the main window
root = tk.Tk()
root.title("ChatGPT GUI")

# create the input box and label
input_label = tk.Label(root, text="Enter your question:", font=("Arial", 16))
input_label.pack()
input_box = tk.Text(root, height=12, font=("Arial", 16))
input_box.pack()

# create the submit button
submit_button = tk.Button(root, text="Submit", command=get_response)
submit_button.pack()

# create the output box and label
output_label = tk.Label(root, text="Response:", font=("Arial", 16))
output_label.pack()
output_box = tk.Text(root, height=12, state=tk.DISABLED, font=("Arial", 16))
output_box.pack()



root.mainloop()
