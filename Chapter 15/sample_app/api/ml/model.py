MALE_WORDS = ['he', 'him', 'his']
FEMALE_WORDS = ['she', 'her']
min_length = 10

def preprocess(text): return text.lower().split(' ')
def predict(text):
    m = 0
    f = 0
    preprocessed = preprocess(text)
    for word in MALE_WORDS:
        if word.lower() in preprocessed:
            m += 1
    for word in FEMALE_WORDS:
        if word.lower() in preprocessed:
            f += 1

    return {
        "gender_content": {
            "male": m/(m+f) if (m+f) != 0 else 0,
            "female": f/(m+f) if (m+f) != 0 else 0
        },
        "text_processed": preprocessed,
    }