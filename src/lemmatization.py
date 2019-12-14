import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import os


# replace " ' . , with ' '
pat_letter = re.compile(r'[^a-zA-Z \']+')
# common abbreviations
pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
pat_s = re.compile("(?<=[a-zA-Z])\'s") #
pat_s2 = re.compile("(?<=s)\'s?")
pat_not = re.compile("(?<=[a-zA-Z])n\'t") # not
pat_would = re.compile("(?<=[a-zA-Z])\'d") # would
pat_will = re.compile("(?<=[a-zA-Z])\'ll") # will
pat_am = re.compile("(?<=[I|i])\'m") # am
pat_are = re.compile("(?<=[a-zA-Z])\'re") # are
pat_ve = re.compile("(?<=[a-zA-Z])\'ve") # have
lmtzr = WordNetLemmatizer()


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return ''


def merge(words):
    new_words = []
    for word in words:
        if word:
            tag = nltk.pos_tag(word_tokenize(word)) # tag is like [('bigger', 'JJR')]
            pos = get_wordnet_pos(tag[0][1])
            if pos:
                # lemmatize(): word to pos format of word
                lemmatized_word = lmtzr.lemmatize(word, pos)
                new_words.append(lemmatized_word)
            else:
                new_words.append(word)
    return new_words


def replace_abbreviations(text):
    new_text = text
    new_text = pat_letter.sub(' ', text).strip().lower()
    new_text = pat_is.sub(r"\1 is", new_text)
    new_text = pat_s.sub("", new_text)
    new_text = pat_s2.sub("", new_text)
    new_text = pat_not.sub(" not", new_text)
    new_text = pat_would.sub(" would", new_text)
    new_text = pat_will.sub(" will", new_text)
    new_text = pat_am.sub(" am", new_text)
    new_text = pat_are.sub(" are", new_text)
    new_text = pat_ve.sub(" have", new_text)
    new_text = new_text.replace('\'', ' ')
    return new_text


def load_data(input_filename, output_filename):
    data = pd.read_csv(input_filename)
    header = list(data.columns)
    print(header)
    title_column = -1
    summary_column = -1
    tags_column = -1
    body_column = -1
    for i in range(len(header)):
        if header[i] == 'title':
            title_column = i
        elif header[i] == 'summary':
            summary_column = i
        elif header[i] == 'tags':
            tags_column = i
        elif header[i] == 'body':
            body_column = i
    data = data.values.tolist()

    new_data = []
    for item in data:
        title = str(item[title_column]).lower()
        summary = str(item[summary_column]).lower()
        tags = str(item[tags_column]).lower()
        body = str(item[body_column]).lower()

        item[title_column] = ' '.join(merge(replace_abbreviations(title).split()))
        item[summary_column] = ' '.join(merge(replace_abbreviations(summary).split()))
        item[tags_column] = ' '.join(merge(replace_abbreviations(tags).split()))
        item[body_column] = ' '.join(merge(replace_abbreviations(body).split()))

        new_data.append(item)

    df = pd.DataFrame(new_data, columns=header)
    df.to_csv(output_filename, index=False)
    print(data[0])


def load_social_data(input_filename, output_filename):
    data = pd.read_csv(input_filename)
    header = list(data.columns)
    print(header)
    text_column = -1
    for i in range(len(header)):
        if header[i] == 'text':
            text_column = i
    data = data.values.tolist()

    new_data = []
    for item in data:
        text = str(item[text_column]).lower()
        text = remove_urls(text)
        item[text_column] = ' '.join(merge(replace_abbreviations(text).split()))
        new_data.append(item)

    df = pd.DataFrame(new_data, columns=header)
    df.to_csv(output_filename, index=False)
    print(len(data))


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def remove_urls(text):
    # remove urls start with http or https
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text)
    # remove urls contains certain domainS
    text = re.sub(r'(\w|\.|\/|\?|\=|\&|\%)*'
                   r'(\.com|\.net|\.xyz|\.top|\.tech|\.org|\.gov|\.edu|\.ink|\.red|\.int|\.mil|\.pub|\.me|\.TV|\.info|\.mobi|\.travel|\.cn)'
                   r'(\w|\.|\/|\?|\=|\&|\%)*\b', '', text)
    return text


def main():
    # -------------------------------------mainstream media data-------------------------------------
    topics = ["arts", "community", "housing", "library", "program", "resident", "school", "service", "street", "youth"]
    input_filenames = ["boston_globe", "boston_herald", "wbur", "wgbh"]
    for input_filename in input_filenames:
            load_data("mainstream_mayor/" + input_filename + ".csv", "mainstream_lemmatization_cleaned/"
                + input_filename + "_lemmatization_cleaned.csv")

    # -----------------------------------------social media data--------------------------------------
    for topic in topics:
        input_filename = 'twitter_mayor/' + topic + '.csv'
        output_filename = 'twitter_lemmatization_cleaned/' + topic + '.csv'
        load_social_data(input_filename, output_filename)


main()
