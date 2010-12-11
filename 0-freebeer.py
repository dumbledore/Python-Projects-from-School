#   Argumentat 'n' tryabva da bade tsyalo ili realno chislo.
#   Ako 'n' e otritsatelno, to redat se obrashta na obratno (moya tupa ideya).
def freebeer(n):

    reverse = False
    
    if (isinstance(n, int) or isinstance(n, float)) is not True:
        return ""

    if n <= 0:
        n *= -1;
        reverse = True

    if isinstance(n, float):
        n = int(n)

    res = "" #Define result
    num = True #Defined outside of the loop

    start = 1
    end = n + 1
    step = 1

    if reverse:
        start = n
        end = 0
        step = -1
    
    for k in range(start,end, step): #main loop

        num = True
        if k % 3 == 0:
            res += "free"
            num = False

        if k % 5 == 0:
            res += "beer"
            num = False

        if num == True:
            res += str(k)
        res += " "
    
    return res.rstrip()
