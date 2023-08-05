from collections import defaultdict

import cygrams


def true_ngrams_counts(items, min_n, max_n):
    ret = defaultdict(int)
    max_n += 1
    for i in items:
        for j in range(len(i)-min_n+1):
            for k in range(j + min_n, min(j + max_n, len(i) + 1)):
                ret[i[j:k]] += 1
    return dict(ret)


def test_topK():
    assert cygrams.build_topK(['Прирвет, мир ир!'], 2, 4, min_df=3) == {'ир': 0}


def test_counts():
    assert cygrams.calculate_counts(['Прирвет, мир ир!'], 1, 4) == true_ngrams_counts(['Прирвет, мир ир!'], 1, 4)


if __name__ == "__main__":
    test_topK()
    test_counts()
