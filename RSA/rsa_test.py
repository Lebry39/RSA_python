import numpy as np
import math
import time
import random

BIT_RESOLUTION = 2**8

def calc_time(func):
    def wrapper(*args, **kargs):
        st = time.perf_counter()
        result = func(*args, **kargs)
        st = time.perf_counter() - st
        print("\n[ TIME ] %.5f s" % st)
        return result
    return wrapper

def seachPrimeNumpy(begign, N):
    # seachListには sqrt(N) で割り切れる値が N しかありえない
    # つまりこれ以上の値を調べる意味がない
    maxium = int(np.sqrt(N))

    # 2 ~ Nまでのリストを生成
    seachList = np.arange(3, N+1, 2, dtype=np.uint64)
    seachList = np.append(np.array([2], dtype=np.uint64), seachList)

    primeNum = np.array([], dtype=np.uint64)
    while seachList[0] <= maxium:
        # seachListで一番小さい値は確実に素数になっている
        primeNum = np.append(primeNum, seachList[0])
        tmp = seachList[0]

        # 一番小さい素数で割り切れるものをsearchリストから取り除きながら
        # tempで使用した値自身も削除する
        seachList = seachList[seachList % tmp != 0]

    # 最後まで取り除かれなかったものは素数
    primeNum = np.append(primeNum, seachList)
    primeNum = primeNum[primeNum >= begign]

    return primeNum

def get_pq(a, b):
    pass

def gen_keys(p_nums):
    p, q = np.random.choice(p_nums, 2, replace=False)
    p, q = int(p), int(q)
    print("p q", p, q)

    print("Calc N and L ...")
    N = p * q
    L = (p - 1) * (q - 1) // math.gcd((p - 1), (q - 1))
    print("= ", N, L)

    print("Calc E ...")
    while True:
        E = np.random.randint(1, L, dtype=np.uint64)
        if math.gcd(E, L) == 1:
            break
    print("= ",E)

    x = 1000 * 10**3
    if L < x:
        x = L // 10
    x_part_list = np.arange(0, L-x, x, dtype=np.uint64)
    x_part_list = np.append(x_part_list, np.array([L-x], dtype=np.uint64))
    np.random.shuffle(x_part_list)

    print("Calc D...")
    for i, begin_num in enumerate(x_part_list):
        temp = np.arange(begin_num, begin_num+x, dtype=np.uint64)
        temp = temp[(E * temp) % L == 1]
        if len(temp) > 0:
            D = np.random.choice(temp, 1)[0]
            break

    # while True:
    #     D = np.random.randint(1, L)
    #     if ((E * D) % L) == 1:
    #         break
    print("= ",D)

    return N, E, D

def encrypt(ptext, N, E):
    # return (ptext ** E) % N
    x = 5000

    mul_x_times = int(E // x)
    mul_rest_num = int(E % x)

    muled_by_x = (ptext ** x) % N
    muled_by_rest = (ptext ** mul_rest_num) % N

    result = 1
    for i in range(mul_x_times):
        result = (result * muled_by_x) % N
    result = (result * muled_by_rest) % N

    return result

def encrypt_array(parray, N, E):
    init = random.randint(1, N)

    etext = encrypt(parray[0] ^ init, N, E)
    earray = [init, etext]
    for ptext in parray[1:]:
        etext = encrypt(ptext ^ etext, N, E)
        earray.append(etext)

    return earray

def dencrypt_array(earray, N, D):
    earray = [i for i in reversed(earray)]

    parray = []
    for etext, xor in zip(earray[:-1], earray[1:]):
        ptext = encrypt(etext, N, D) ^ xor
        parray.append(ptext)
        print(ptext)

    return [i for i in reversed(parray)]

@calc_time
def main():
    BIT_RESOLUTION = 2 ** 16

    prime_num = seachPrimeNumpy(100, BIT_RESOLUTION)

    # 鍵の生成
    print("# 共通鍵の生成")
    N, E, D = gen_keys(prime_num)
    print()
    print("N, E, D = ", N, E, D)

    # 数字の暗号化
    plan_num = 3939

    e_num = encrypt(plan_num, N, E)
    d_num = encrypt(e_num,    N, D)

    print()
    print("# 整数の暗号化")
    print("plan_num ",plan_num)
    print("e_num    ", e_num)
    print("d_num    ", d_num)

    exit()

    # 文字列の暗号化
    p_text = "Hello World !!"
    p_ary = [ord(i) for i in p_text]

    e_ary = encrypt_array(p_ary, N, E)
    e_text = "".join([chr(i) for i in e_ary])

    d_ary  = dencrypt_array(e_ary, N, D)
    d_text = "".join([chr(i) for i in d_ary])

    print()
    print("# 文字列の暗号化")
    print("plan_text ",p_text)
    print("e_text    ",e_text)
    print("d_text    ",d_text)


if __name__ == "__main__":
    main()
