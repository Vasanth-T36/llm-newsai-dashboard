from nltk.tokenize import sent_tokenize

def summarize(text, n=5):
    if not text:
        return ""
    sentences = sent_tokenize(text)
    return " ".join(sentences[:n])