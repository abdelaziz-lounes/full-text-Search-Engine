import json
from collections import defaultdict #defaultdict is a dictionary subclass that provides a default value for a nonexistent key.

# File path
PROCESSED_DATA_FILE = "./data/processed_data.json"

# Load processed data
def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Build inverted index
def build_inverted_index(data):
    inverted_index = defaultdict(set) #initializes an empty defaultdict with a set as the default value.
    for entry in data:
        doc_id = entry["id"]
        for word in entry["processed"]:
            inverted_index[word].add(doc_id)
    return inverted_index



# inverted_index = {
#     "there": {0, 1},
#     "noth": {0},
#     "to": {0},
#     "tell": {0},
#     "he": {0, 2, 3},
#     "just": {0},
#     "some": {0},
#     "guy": {0, 1},
#     "i": {0},
#     "work": {0},
#     "with": {0, 1},
#     "cmon": {1},
#     "youre": {1},
#     "go": {1},
#     "out": {1},
#     "the": {1},
#     "gotta": {1},
#     "be": {1, 2},
#     "someth": {1},
#     "wrong": {1},
#     "him": {1},
#     "all": {2},
#     "right": {2},
#     "joey": {2},
#     "nice": {2},
#     "so": {2},
#     "doe": {2, 3},
#     "have": {2},
#     "a": {2},
#     "hump": {2},
#     "and": {2},
#     "hairpiec": {2},
#     "wait": {3},
#     "eat": {3},
#     "chalk": {3}
# }


# Search function
def search(query, inverted_index, data, preprocess_func):
    processed_query = preprocess_func(query)
    if not processed_query:
        return []
    # Find documents containing all query terms
    result_sets = [inverted_index.get(term, set()) for term in processed_query]
    matching_doc_ids = set.intersection(*result_sets) if result_sets else set() #returns the intersection of two or more sets as a new set.
    # Retrieve original documents
    return [data[doc_id] for doc_id in matching_doc_ids]

if __name__ == "__main__":
    # Load data and build index
    data = load_data(PROCESSED_DATA_FILE)
    inverted_index = build_inverted_index(data)
    print("Inverted index built successfully.")
