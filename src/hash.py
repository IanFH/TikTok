def hash(s: str):
    #hash
    p, m = 31, 10**9 + 7
    length = len(s)
    hash_value = 0
    p_pow = 1
    for i in range(length):
        hash_value = (hash_value + (1 + ord(s[i]) - ord('a')) * p_pow) % m
        p_pow = (p_pow * p) % m
    return hash_value