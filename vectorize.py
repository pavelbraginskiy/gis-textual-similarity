from typing import Optional

import TrajectoryDistance
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk import word_tokenize
import nltk

model: Optional[Doc2Vec] = None


def initialize(strings: [str]) -> None:
    nltk.download('punkt')
    global model
    tagged_data = [TaggedDocument(words=word_tokenize(s), tags=[str(i)])
                   for i, s in enumerate(strings)]
    model = Doc2Vec(vector_size=TrajectoryDistance.num_dimensions, min_count=2, epochs=50)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    model.save('model')


def vectorize(document: [str]) -> [[float]]:
    global model
    if model is None:
        model = Doc2Vec.load('model')
    return [
        model.infer_vector(word_tokenize(paragraph)).tolist()
        for paragraph in document
    ]
