# distutils: language = c++

from libcpp.map cimport map
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.algorithm cimport sort as cpp_sort
from cython.operator cimport preincrement


cdef map[string,int] _calculate_counts(items, int min_n, int max_n):
    cdef int i, j, n, count, length
    cdef map[string,int] counts
    cdef string item_string
    min_n *= 4
    max_n = (max_n + 1) * 4  # max_n is inclusive
    for item in items:
        item_string = item.encode('utf-32')[4:]  # 0..4 bytes is a BOM
        with nogil:
            length = item_string.length()
            for i in range(0, length - min_n + 4, 4):
                n = max_n
                if i + n > length + 4:
                    n = length + 4 - i
                for j in range(min_n, n, 4):
                    preincrement(counts[item_string.substr(i, j)])
    return counts


def calculate_counts(items, int min_n, int max_n):
    cdef map[string,int] counts = _calculate_counts(items, min_n, max_n)
    cdef pair[string,int] i
    ret = {}
    for i in counts:
        ret[i.first.decode('utf-32')] = i.second
    return ret


def build_topK(items, int min_n, int max_n, int min_df=100, int K=0):
    cdef map[string,int] counts = _calculate_counts(items, min_n, max_n)
    cdef pair[string,int] it
    cdef vector[pair[int,string]] ngrams
    cdef int i, n
    with nogil:
        for it in counts:
            if it.second >= min_df:
                ngrams.push_back(pair[int,string](-it.second, it.first))
        cpp_sort(ngrams.begin(), ngrams.end())
        n = ngrams.size()
        if n < K:
            n = K
    ret = {}
    for i in range(n):
        ret[ngrams[i].second.decode('utf-32')] = i
    return ret
