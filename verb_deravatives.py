import openpyxl
import nltk
from nltk.corpus import wordnet

# Open the text file and read its content
with open('Word_10.txt', 'r') as f:
    text = f.read()

# Find all words in the text
words = nltk.word_tokenize(text)

# Create a dictionary to store the derivatives for each word
derivatives = {}

# Loop through the words and find their derivatives
for word in words:
    # Find all possible inflected forms of the word
    forms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            for form in lemma.derivationally_related_forms():
                forms.add(form.name())
            for form in lemma.pertainyms():
                forms.add(form.name())
        for form in synset.lemma_names():
            if form != word:
                forms.add(form)
        morphy_forms = wordnet.morphy(word)
        if morphy_forms is not None:
            forms.update(morphy_forms)

    # Add the word and its inflected forms to the derivatives dictionary
    derivatives[word] = list(forms)

# Create a new Excel workbook and worksheet
wb = openpyxl.Workbook()
ws = wb.active

# Write the header row
ws['A1'] = 'Word'
ws['B1'] = 'Derivatives'

# Write the derivatives for each word to the worksheet
row = 2
for word, forms in derivatives.items():
    ws.cell(row=row, column=1, value=word)
    ws.cell(row=row, column=2, value=', '.join(forms))
    row += 1

# Save the workbook to a file
wb.save('derivatives.xlsx')
