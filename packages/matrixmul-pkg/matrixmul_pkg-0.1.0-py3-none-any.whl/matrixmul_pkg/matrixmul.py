# Date 2018/11/19
# WQ
# Date 2018/11/19
# WQ
def mxmul(A, B, nrow, nl, ncol):
    rst = [[0 for y in range(ncol)] for x in range(nrow)]
    for i in range(nrow):
        for j in range(ncol):
            for k in range(nl):
                rst[i][j] = A[i][k] * B[k][j]
    return rst

def mxsum(A, nrow, ncol):
    s = 0
    for i in nrow:
        for j in range(ncol):
            s += A[i][j]
    return s

if __name__ == '__main__':
    import time
    nrow, nl, ncol = 10, 10, 10
    A = [[y for y in range(nl)] for x in range(nrow)]
    B = [[y for y in range(ncol)] for x in range(nl)]
    start = time.perf_counter()
    rst = mxmul(A, B, nrow, nl, ncol)
    end = time.perf_counter()
    print(A, B)
    print("运算时间为{}".format(end-start))