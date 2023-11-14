from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk import word_tokenize
import nltk
nltk.download('punkt')

model = Doc2Vec(vector_size=2, min_count=2, epochs=50)
initialized = False

def initialize(strings: [str]) -> None:
    tagged_data = [TaggedDocument(words=word_tokenize(s), tags=[str(i)])
                   for i, s in enumerate(strings)]
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    global initialized
    initialized = True


def vectorize(document: [str]) -> [[float]]:
    if not initialized:
        raise Exception("Call initialize first")
    return [
        model.infer_vector(word_tokenize(paragraph)).tolist()
        for paragraph in document
    ]