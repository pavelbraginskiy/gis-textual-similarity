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

    print("CPD: ", similarity.cpd(a_sample, b_sample))
    print("SPD: ", similarity.spd(a_sample, b_sample))
    print("DTW: ", similarity.dtw(a_sample, b_sample))
    print("LCSS, e=0.5: ", similarity.lcss(a_sample, b_sample, 0.5))
    print("LCSS, e=1: ", similarity.lcss(a_sample, b_sample, 1))
    print("LCSS, e=2: ", similarity.lcss(a_sample, b_sample, 2))
    print("EDR, e=0.5: ", similarity.edr(a_sample, b_sample, 0.5))
    print("EDR, e=1: ", similarity.edr(a_sample, b_sample, 1))
    print("EDR, e=2: ", similarity.edr(a_sample, b_sample, 2))
    print("ERP: ", similarity.erp(a_sample, b_sample))