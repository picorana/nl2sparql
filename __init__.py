import re
import datetime
# import logging


def preprocess_string(s, lower=True, stem=True, remove_stopwords=True,
                      remove_punctuation=True):
    """ Cleanup a string

    Keyword arguments:
        s       --  the input string
        lower   --  lower every char
        stem    --  extract root of every word
        remove_stopwords    --  well, self-explanatory
        remove_punctuation  --  self-explanatory too
    """

    # lower every char
    # entity recognition also uses upper chars
    if lower:
        s = s.lower()

    # replace accents
    accent_chars = {
        "è": "e",
        "é": "e",
        "à": "a",
        "ò": "o",
        "ó": "o",
        "ù": "u",
        "ì": "i",
    }

    for char in accent_chars:
        s.replace(char, accent_chars[char])

    # tokenize and remove punctuation
    from nltk.tokenize import RegexpTokenizer

    tokenizer = RegexpTokenizer(r"\w+")
    s = tokenizer.tokenize(s)

    # stem the words
    if stem:
        from nltk.stem.snowball import ItalianStemmer
        stemmer = ItalianStemmer()
        s = [stemmer.stem(word) for word in s]

    # remove stopwords (italian)
    if remove_stopwords:
        from stop_words import get_stop_words
        s = [word for word in s if word not in get_stop_words('it')]

    return " ".join(s)


def find_most_similar(l1, s):
    """ Uses levenshtein distance to find most similar string in a list

    Keyword arguments:
        l1  --  list in which we are searching for the most similar word
        s   --  the input string to search in the list
    """

    import editdistance

    best = float('inf')
    best_match = ""

    for l in l1:
        ed = editdistance.eval(l, s)
        if ed < best:
            best = ed
            best_match = l

    # logger.debug("best_match: " + best_match)
    # logger.debug("levenshtein distance: " + str(best))

    return best_match


def generate_questions(onto):
    """
    """

    domande = []

    for c in onto.classes():

        # i verbi sono preceduti da "che" nelle object properties?

        # controlla subclasses
        for c2 in c.ancestors():
            if c2.name != "Thing" and c2.name != c.name:
                question_string = c2.name.replace("_", " ") + " che è " + c.name.replace("_", " ")
                domande.append(question_string)

                if c2.name in c.name:
                    question_string = c2.name.replace("_", " ") + " che è"  \
                        + c.name.replace(c2.name, "").replace("_", " ")
                    question_string = re.sub("\s{2,}", " ", question_string)
                    domande.append(question_string)

        # controlla object properties
        for p in onto.object_properties():

            if c in p.domain:

                question_string = ""
                question_string += c.name.replace("_", " ") + " "
                question_string += p.name.replace("_", " ") + " "

                for r in p.range:
                    question_string += "[" + r.name + "]"
                domande.append(question_string)

        # controlla data properties
        for p in onto.data_properties():
            if c in p.domain:
                question_string = ""
                question_string += c.name.replace("_", " ") + " con "
                question_string += p.name.replace("_", " ") + " "
                for r in p.range:
                    if r == str:
                        question_string += "[STR]"
                    elif r == int:
                        question_string += "[INT]"
                    elif r == datetime.datetime:
                        question_string += "[DATE]"

                domande.append(question_string)

    # logger.debug("created " + str(len(domande)) + " questions")
    for d in domande:
        print(d)
