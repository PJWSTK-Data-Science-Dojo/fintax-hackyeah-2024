import re
import nltk
from nltk.corpus import cmudict

# Download the CMU pronouncing dictionary if you haven't already
nltk.download('cmudict')

# Load CMU Pronouncing Dictionary to get syllables count
d = cmudict.dict()

# Function to count syllables in a word
def count_syllables(word):
    word = word.lower()
    if word in d:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word]][0]
    else:
        return sum(1 for char in word if char in 'aeiouy')  # Simple fallback for unknown words

# Function to check if a word is complex (3 or more syllables)
def is_complex_word(word):
    return count_syllables(word) >= 3

# Gunning Fog Index function
def gunning_fog_index(text):
    # Split the text into words
    words = re.findall(r'\w+', text)
    
    # Count the number of sentences (splitting by punctuation marks)
    sentences = re.split(r'[.!?]', text)
    sentences = [s for s in sentences if s.strip()]  # Remove empty strings
    
    # Count the number of words
    total_words = len(words)
    
    # Count the number of complex words (3 or more syllables)
    complex_words = sum(1 for word in words if is_complex_word(word))
    
    # Number of sentences
    total_sentences = len(sentences)
    
    if total_sentences == 0 or total_words == 0:
        return 0  # Prevent division by zero

    # Calculate the Gunning Fog Index
    fog_index = 0.4 * ((total_words / total_sentences) + (100 * (complex_words / total_words)))
    
    return fog_index

# Helper function to count syllables in a word
def count_syllables(word):
    word = word.lower()
    syllables = 0
    vowels = "aeiouy"
    
    # Check if the first character is a vowel
    if word[0] in vowels:
        syllables += 1
    
    # Count vowels in the rest of the word
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllables += 1
    
    # Subtract a syllable for silent 'e'
    if word.endswith("e"):
        syllables -= 1
    
    # Every word has at least one syllable
    if syllables == 0:
        syllables = 1
    
    return syllables

# Function to compute Flesch Reading Ease Score
def flesch_reading_ease(text):
    # Split the text into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if len(s.strip()) > 0]  # Filter empty sentences
    
    # Split the text into words
    words = re.findall(r'\b\w+\b', text)
    
    # Calculate number of syllables in each word
    syllable_count = sum(count_syllables(word) for word in words)
    
    # Calculate ASL and ASW
    asl = len(words) / len(sentences)  # Average Sentence Length
    asw = syllable_count / len(words)  # Average Syllables per Word
    
    # Calculate the Flesch Reading Ease Score
    flesch_score = 206.835 - (1.015 * asl) - (84.6 * asw)
    
    return round(flesch_score, 2)

def indexes_scoring(transcription):
    full_text = ""
    for sentence_dict in transcription:
        full_text += sentence_dict['text']
    
    return {
        flesch_reading_ease: flesch_reading_ease(full_text),
        gunning_fog_index: gunning_fog_index(full_text)
    }
    