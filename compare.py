import cProfile

import parse
import vectorize
import sys
import similarity

if __name__ == '__main__':
    doc_a = parse.paragraphs(sys.argv[1])
    doc_b = parse.paragraphs(sys.argv[2])

    vectorize.initialize([*doc_a, *doc_b])

    a = vectorize.vectorize(doc_a)
    b = vectorize.vectorize(doc_b)

    s = 25  # size of sample from text

    a_sample = a[len(a) // 2 - s:len(a) // 2 + s]
    b_sample = b[len(b) // 2 - s:len(b) // 2 + s]

    print(similarity.erp(a_sample, b_sample))