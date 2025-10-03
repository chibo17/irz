
def Nto2N(n):
    return 2*n


# preštevanje parov naravnih števil ()
def NtoNN(n):
    i,j= 1, 1
    k=1
    while k<n:
        if j==1:
            j = i + 1
            i = 1
        else:
            j -= 1
            i += 1
        #if gcd(i,j)==1:   # ulomki
        k+=1 
    return (i,j)


# inverz (bijektivne) funkcije f: N -> X
def inverse(f):
    def g(y):
        x = 0
        while True:
            if f(x) == y:
                return x
            x += 1
    return g


# pomožna funkcija
def gcd(a,b):
    while b:
        a, b = b, a % b
    return a