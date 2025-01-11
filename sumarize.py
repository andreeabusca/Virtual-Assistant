import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import heapq
import string
from speak import speak

nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text):
    if not text.strip():
        return "Text is empty"
    
    sentences = sent_tokenize(text)
    num_sentences = len(sentences) // 2

    stop_words = set(stopwords.words("english"))
    word_frequencies = {}

    for word in word_tokenize(text):
        word = word.lower()
        if word not in stop_words and word not in string.punctuation:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1
    
    max_frequency = max(word_frequencies.values(), default=1)
    word_frequencies = {word: freq / max_frequency for word, freq in word_frequencies.items()}

    # Score sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]

    # Select the top `num_sentences` sentences
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary


