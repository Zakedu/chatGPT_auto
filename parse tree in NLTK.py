import nltk
from nltk.tree import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
from PIL import Image, ImageTk
import tkinter as tk

# Define a function to tokenize and parse the user's input
def process_input():
    sentence = sentence_entry.get()
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)
    print(tokens)
    print(tagged)
    print(entities)

    # Display parse tree image
    if isinstance(entities, Tree):
        create_parse_tree_image(entities)

# Define a function to create and display the parse tree image
def create_parse_tree_image(tree):
    # Draw the parse tree
    cf = CanvasFrame()
    tc = TreeView(cf.canvas(), tree)
    tc['node_font'] = 'Helvetica 14 bold'
    tc['leaf_font'] = 'Helvetica 14'
    cf.add_widget(tc, 10, 10)
    cf.print_to_file('parse_tree.ps')
    cf.destroy()

    # Load the parse tree image into a Tkinter label widget
    image = Image.open('parse_tree.ps')
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(window, image=photo)
    label.image = photo
    label.pack()

    # Remove the temporary PostScript file
    os.remove('parse_tree.ps')



# Create a GUI window
window = tk.Tk()
window.title("Tokenize and Parse")
window.geometry("400x300")

# Add a label and input box for the user's input
sentence_label = tk.Label(window, text="Enter a sentence to tokenize and parse:")
sentence_label.pack()
sentence_entry = tk.Entry(window)
sentence_entry.pack()

# Add a button to process the input
process_button = tk.Button(window, text="Process", command=process_input)
process_button.pack()

# Start the GUI event loop
window.mainloop()
