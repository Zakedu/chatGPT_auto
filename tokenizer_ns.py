import nltk
import openpyxl

# Load the text file
with open('example_token.txt', 'r') as f:
    text = f.read()

# Tokenize the text
sentences = nltk.sent_tokenize(text)
tokens = [sentence.split() for sentence in sentences]

# Write the tokens to an Excel file
wb = openpyxl.Workbook()
ws = wb.active
for i, sentence in enumerate(sentences):
    for j, token in enumerate(tokens[i]):
        ws.cell(row=i+1, column=j+1, value=token)
wb.save('output.xlsx')
