"""
sliding window determinantal point process
"""

import numpy as np
import numpy.linalg as LA
import operator


def brute_force(w, A):
    """
    use numpy.linalg.det function to solve DPP with sliding window
    NOTE. w cannot be too big
    :param w: sliding window size
    :param A: L-ensemble of DPP
    :return: tuple of new index and  un-normalized probabilities
    """
    n = A.shape[0]
    ranks = []
    remains = list(range(n))
    determinants = []
    for _ in range(n):
        candidates = []
        # print(f'ranks={ranks}, remains={remains}')
        for i in range(len(remains)):
            index = remains.pop(0)
            ranks.append(index)
            block_index = ranks[-w:]
            block_matrix = A[block_index, :][:, block_index]
            candidates.append((index, LA.det(block_matrix)))
            remains.append(ranks.pop())

        index, value = max(candidates, key=operator.itemgetter(1))
        determinants.append(value)
        ranks.append(index)
        remains.remove(index)
        # print(f'candidates = {candidates}')
        # print(f'best: index={index}, value={value}')
    return ranks, determinants


def cholupdate(L, x):
    # rank one update
    n = len(x)
    for k in range(n):
        r = np.sqrt(L[k, k] ** 2 + x[k] ** 2)
        c = r / L[k, k]
        s = x[k] / L[k, k]
        L[k, k] = r
        for j in range(k + 1, n):
            L[j, k] = (L[j, k] + s * x[j]) / c
            x[j] = c * x[j] - s * L[j, k]


def chol_inc(minor, L):
    ######################################
    # w = minor.shape[0] - 1
    #
    # for j in range(w):
    #     s = 0.0
    #     for k in range(j):
    #         s += L[j, k] * L[w, k]
    #     L[w, j] = (minor[w, j] - s) / L[j, j]
    #
    # s = 0.0
    # for k in range(w):
    #     s += L[w, k] * L[w, k]
    # L[w, w] = np.sqrt(minor[w, w] - s)
    #
    # return L[w, w], L[w, :].copy()
    ######################################
    w = minor.shape[0] - 1
    for j in range(w):
        s = np.dot(L[j, :j], L[w, :j])
        L[w, j] = (minor[w, j] - s) / L[j, j]
    L[w, w] = np.sqrt(minor[w, w] - np.dot(L[w, :w], L[w, :w]))
    return L[w, w], L[w, :].copy()


def sliding(L):
    beta = L[1:, 0]
    lower = L[1:, 1:]
    cholupdate(lower, beta)
    L[:-1, :-1] = lower


def incremental_cholesky(w, A):
    """
     use cholesky decomposition to solve DPP with sliding window
    :param w:  window size
    :param A:  L-ensemble of DPP
    :return: tuple of new index and  un-normalized probabilities
    """
    # NOTE: slower than brute_force when w is smaller
    n = A.shape[0]

    pivots = []
    determinants = []
    ranks = []
    remains = list(range(n))
    L = np.zeros((w, w))

    da = np.diag(A)
    k = np.argmax(da)
    ranks.append(k)
    remains.remove(k)
    L[0, 0] = np.sqrt(A[k, k])

    pivots.append(L[0, 0])
    determinants.append(da[k])

    for wi in range(1, n):
        if wi >= w:
            sliding(L)

        candidates = []
        for i in range(len(remains)):
            index = remains.pop(0)
            ranks.append(index)
            block_index = ranks[-w:]
            block_matrix = A[block_index, :][:, block_index]
            value, last_row = chol_inc(block_matrix, L)
            candidates.append((index, value, last_row))
            remains.append(ranks.pop())
        index, value, last_row = max(candidates, key=operator.itemgetter(1))

        if wi < w:
            L[wi, :] = last_row
        else:
            L[-1, :] = last_row

        pivots.append(value)
        ranks.append(index)
        remains.remove(index)
        # print(f'pairs = {pairs}')
        # print(f'best: index={index}, value={value}')
        if wi < w:
            determinants.append(np.prod(np.diag(L)[:wi + 1]) ** 2)
        else:
            determinants.append(np.prod(np.diag(L)) ** 2)
    # print(f'pivots={pivots}')
    return ranks, determinants


def vec_near(a, b, tol=1e-6):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if abs(x - y) > tol:
            return False
    return True


def compare_methods():
    """Make sure the results of the two methods are same."""
    n = 30
    w = 5
    pass_times, try_times = 0, 100
    for _ in range(try_times):
        r = np.random.rand(n, n)
        A = r @ r.T
        rank1, determinants1 = incremental_cholesky(w, A)
        rank2, determinants2 = brute_force(w, A)

        if rank1 != rank2 or not vec_near(determinants1, determinants2):
            print(f"ERROR:, n={n}, w={w}, A=\n", A)
        else:
            pass_times += 1

    print(f'try_times = {try_times}, w={w}, n={n}')
    if pass_times == try_times:
        print('ALL PASSED!')


def swdpp(w, L, check_psd=False, method='incremental_cholesky'):
    """
    sliding window DPP
    :param L: L-ensemble of DPP
    :param w: window size
    :param check_psd: check matrix is PSD
    :param method:  support incremental and brute_force
    :return: tuple of new index and  un-normalized probabilities(aka. determinants of principle minors)
    """

    if type(L) == list:
        try:
            L = np.array(L, dtype=np.float64)
        except ValueError:
            print('Input matrix data format error: only support numpy arrays and nested lists')
            raise

    _d1, _d2 = L.shape
    if _d1 != _d2:
        raise Exception('Input Data Error: input L should be a square matrix')
    if w > _d1:
        raise Exception('Input Data Error: input w should not be greater than the dimension of L')

    if check_psd:
        ev, _ = LA.eig(L)
        if any(ev < 0):
            raise Exception('Input Matrix A not PSD')

    if method not in ('incremental_cholesky', 'brute_force'):
        raise Exception('Only support two methods (incremental_cholesky, brute_force)')

    if method == 'incremental_cholesky':
        return incremental_cholesky(w, L)
    else:
        return brute_force(w, L)


def demo():
    n = 10
    r = np.arange(n * n).reshape(n, n) / (n * n)
    A = r @ r.T + np.eye(n)  # PSD matrix
    w = 5

    print(f'INPUT:\n w={w}\n n={n}\n L-ensemble kernel, A=\n', A)

    rank, determinants = swdpp(w, A)
    print(f'OUTPUT:\n rank={rank}\n determinants={determinants}')

    # use the brute force method
    rank, determinants = swdpp(w, A, method='brute_force')
    print(f'OUTPUT:\n rank={rank}\n determinants={determinants}')


if __name__ == '__main__':
    demo()
    # compare_methods()
