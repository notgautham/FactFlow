from transformers import AutoTokenizer

def tokenize_data(data, tokenizer):
    """ Tokenize the text data using the tokenizer. """
    encodings = tokenizer(list(data), truncation=True, padding=True, max_length=512)
    return encodings
