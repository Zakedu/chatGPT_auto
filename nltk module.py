## NLTK module used

import openpyxl
from collections import Counter
from nltk.corpus import wordnet

# TXT 파일에 추가되어있는 단어 리스트를 읽어온다.
with open('Word.txt', 'r') as f:
    words = f.read().splitlines()

# 데이터 저장할 리스트 지정
word_data = []

# 각 단어에 대한 품사, 뜻(dfnt), 유의어, 반의어, 그리고 예시 문장을 찾는다. 

for i, word in enumerate(words):

    # 각 단어에 대해 품사 별 단어 리스트를 넣을 리스트 생성 
    pos_data = []

    # NLTK 모듈 활용해서 빈도에 따른 품사 별 단어 정보 모으기
    synsets = wordnet.synsets(word)
    if synsets:
        pos_counts = Counter(syn.pos() for syn in synsets)
        top_parts_of_speech = [pos for pos, count in pos_counts.most_common(2)]
        for pos in top_parts_of_speech:
            pos_dict = {'Part of Speech': pos}

            # NLTK 속 단어의 정의(뜻) 불러오기
            pos_synsets = [syn for syn in synsets if syn.pos() == pos]
            if pos_synsets:
                pos_dict['Meaning'] = pos_synsets[0].definition()

            # NLTK 속 유의어, 반의어 불러오기
            synonyms = set()
            antonyms = set()
            for syn in pos_synsets:
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        synonyms.add(lemma.name())
                        if lemma.antonyms():
                            antonyms.add(lemma.antonyms()[0].name())

            # 각 품사에 대한 반의어 유의어 찾아내기
            pos_dict['Antonyms'] = ', '.join(sorted(antonyms)[:2])
            pos_dict['Synonyms'] = ', '.join(sorted(synonyms)[:3])

            # NLTK 속 예문 불러오기
            sentences = []
            for syn in pos_synsets:
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        for example in lemma.synset().examples():
                            sentences.append(example)

            # 각 품사 데이터 속 예문 불러오기
            pos_dict['Sample Sentence'] = ', '.join(sentences[:3])

            # 이 단어에 대한 품사 정보 모은 것을 리스트에 넣기
            pos_data.append(pos_dict)

    # 모든 단어 정보를 단어와 품사 리스트에 넣기
    word_data.append({'Word': word, 'Number': i + 1, 'Parts of Speech': pos_data})

# 단어 정보를 새로운 WB와 WS에 이니셜라이즈 
workbook = openpyxl.Workbook()
worksheet = workbook.active

# 워크시트 첫번째 행에 열 값 정의
worksheet.append(['Number', 'Word', 'Part of Speech', 'Meaning', 'Antonyms', 'Synonyms', 'Sample Sentence'])

# 단어 데이터를 단어 정보에 돌아가며 저장하기
for word_dict in word_data:
    for pos_dict in word_dict['Parts of Speech']:
        worksheet.append([word_dict.get('Number', ''),
                          word_dict.get('Word', ''),
                          pos_dict.get('Part of Speech', ''),
                          pos_dict.get('Meaning', ''),
                          pos_dict.get('Antonyms', ''),
                          pos_dict.get('Synonyms', ''),
                          pos_dict.get('Sample Sentence', '')])

workbook.save('word_nltk.xlsx')
