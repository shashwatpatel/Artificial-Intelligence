import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dir = {}
    for x in os.listdir(directory):
        way = os.path.join(directory,f"{(x)}")
        file = open(way)
        l = file.read().replace("\n", " ")
        file.close()
        dir[x] = l
    return dir


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    li_words = nltk.word_tokenize(document)
    stp_words = nltk.corpus.stopwords.words("english")
    filter = []
    for x in range(len(li_words)):
        li_words[x] = li_words[x].lower()
        if li_words[x] in stp_words or li_words[x] in string.punctuation:
            filter.append(li_words[x])
            continue
    for x in filter:
        li_words.remove(x)
    return li_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    dic = {}
    for x in documents:
        lis = documents[x]
        for w in lis:
            if w in dic:
                continue
            else:
                ctr = 0
                tot = 0
                for tmp in documents:
                    if w in documents[tmp]:
                        ctr = ctr + 1
                    tot = tot + 1
                dic[w] = math.log(float(tot/ctr))
    return dic



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf = dict()
    result = list()
    for file in files:
        tfidf[file] = 0
        for w in query:
            tfidf[file] = tfidf[file] + files[file].count(w) * idfs[w]
    result = sorted(tfidf, key = tfidf.get, reverse = True)
    return result[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    que = {}
    for s in sentences:
        ctr = 0
        words = sentences[s]
        wor_count = 0
        for w in query:
            if w in words:
                ctr = ctr + idfs[w]
                wor_count = wor_count + 1
        que[s] = (ctr, float(wor_count / len(words),))
    sort = sorted(que.keys(), key = lambda x: que[x], reverse = True)
    sort = list(sort)
    try:
        return sort[0:n]
    except:
        return sort



if __name__ == "__main__":
    main()
