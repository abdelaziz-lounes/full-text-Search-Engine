import json
import re # Regular expression operations
import string # Common string operations
from nltk.tokenize import word_tokenize #for tokenizing text into words
from nltk.stem import PorterStemmer #for stemming words

# File paths
INPUT_FILE = "./data/utterances.jsonl" 
OUTPUT_FILE = "./data/processed_data.json"

def preprocess_text(text):
    """
    takes a string text and processes it:
    * Converts the text to lowercase.
    * Removes punctuation using a regular expression.
    * Tokenizes the text into words.
    * Stems each word using the Porter Stemmer.
    * Returns a list of stemmed words.
    """
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    words = word_tokenize(text)
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in words]

def process_data():
    processed_data = []
    
    try:
        # with statement ensures that the file is properly closed after its contents are processed.
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                entry = json.loads(line) #This line parses the current line as a JSON object and assigns it to the variable entry
                text = entry.get("text", "") # If the key is not present, it defaults to an empty string
                processed_words = preprocess_text(text)
                
                processed_data.append({
                    "id": i,
                    "original": text,
                    "processed": processed_words
                })
                print(f"Processed {i+1} entries")  # Debugging

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(processed_data, file, indent=4)
        
        print(f"✅ Processed data saved to {OUTPUT_FILE}")

    except FileNotFoundError:
        print(f"❌ Error: {INPUT_FILE} not found!")
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")

if __name__ == "__main__":
    process_data()
