## NLTK module used

import openpyxl
from collections import Counter
from nltk.corpus import wordnet

# Open the input file and read the words
with open('Word.txt', 'r') as f:
    words = f.read().splitlines()

# Initialize an empty list to store the data
word_data = []

# Loop through each word and get the parts of speech, definition, synonyms, antonyms, and sample sentences
for i, word in enumerate(words):
    # Initialize an empty list to store the data for each part of speech for this word
    pos_data = []

    # Get the parts of speech by frequency using NLTK
    synsets = wordnet.synsets(word)
    if synsets:
        pos_counts = Counter(syn.pos() for syn in synsets)
        top_parts_of_speech = [pos for pos, count in pos_counts.most_common(2)]
        for pos in top_parts_of_speech:
            pos_dict = {'Part of Speech': pos}

            # Get the definition using NLTK
            pos_synsets = [syn for syn in synsets if syn.pos() == pos]
            if pos_synsets:
                pos_dict['Meaning'] = pos_synsets[0].definition()

            # Get the synonyms and antonyms using NLTK
            synonyms = set()
            antonyms = set()
            for syn in pos_synsets:
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        synonyms.add(lemma.name())
                        if lemma.antonyms():
                            antonyms.add(lemma.antonyms()[0].name())

            # Add the synonyms and antonyms to the part of speech data
            pos_dict['Synonyms'] = ', '.join(sorted(synonyms)[:3])
            pos_dict['Antonyms'] = ', '.join(sorted(antonyms)[:2])

            # Get the sample sentences using NLTK
            sentences = []
            for syn in pos_synsets:
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        for example in lemma.synset().examples():
                            sentences.append(example)

            # Add the sample sentences to the part of speech data
            pos_dict['Sample Sentence'] = ', '.join(sentences[:3])

            # Add the part of speech data to the list of data for this word
            pos_data.append(pos_dict)

    # Add the word and part of speech data to the list of all word data
    word_data.append({'Word': word, 'Number': i + 1, 'Parts of Speech': pos_data})

# Initialize a new workbook and worksheet to store the data
workbook = openpyxl.Workbook()
worksheet = workbook.active

# Write the headers to the first row of the worksheet
worksheet.append(['Number', 'Word', 'Part of Speech', 'Meaning', 'Antonyms', 'Synonyms', 'Sample Sentence'])

# Loop through the word data and write it to the worksheet
for word_dict in word_data:
    for pos_dict in word_dict['Parts of Speech']:
        worksheet.append([word_dict.get('Number', ''),
                          word_dict.get('Word', ''),
                          pos_dict.get('Part of Speech', ''),
                          pos_dict.get('Meaning', ''),
                          pos_dict.get('Antonyms', ''),
                          pos_dict.get('Synonyms', ''),
                          pos_dict.get('Sample Sentence', '')])

# Save the workbook to a file
workbook.save('word_nltk.xlsx')
