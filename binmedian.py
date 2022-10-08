def binmedian_compute(x, k):
    """
    binmedian algorithm based exactly on https://www.stat.cmu.edu/~ryantibs/median/binmedian.c
    and paper: https://www.stat.cmu.edu/~ryantibs/papers/median.pdf
    generalized to even and odd input. More work/refactoring to be done when I have time.
    """
    n = len(x)
    mu = sum(x)/n
    sigma = (sum([(i-mu)**2 for i in x])/(n-1))**.5

    # Bin x across the interval [mu-sigma, mu+sigma]
    bottomcount = 0
    bincounts = [0] * 1001
    scalefactor = 1000 / (2 * sigma)
    leftend = mu - sigma
    rightend = mu + sigma

    for i in x:
        if i < leftend:
            bottomcount += 1
        elif i < rightend:
            binn = int((i - leftend) * scalefactor)
            bincounts[binn] += 1

    r, count, medbin = 0, 0, 0
    while True:
        # find the bin that contains the median and order
        # of median within that bin
        count = bottomcount
        for i in range(1000):
            count += bincounts[i]
            if count >= k:
                medbin = i
                k = k - (count - bincounts[i])
                break

        bottomcount = 0
        bincounts = [0] * 1000
        oldscalefactor = scalefactor
        oldleftend = leftend
        scalefactor = 1000 * oldscalefactor
        leftend = medbin / oldscalefactor + oldleftend
        rightend = (medbin + 1) / oldscalefactor + oldleftend

        # Determine which points map to medbin, and put
        # them in spots r,...n-1
        i, r = r, n
        while i < r:
            oldbin = int((x[i] - oldleftend) * oldscalefactor)
            if oldbin == medbin:
                r -= 1
                x[i], x[r] = x[r], x[i]
                if x[i] < leftend:
                    bottomcount += 1
                elif x[i] < rightend:
                    binn = int((x[i] - leftend) * scalefactor)
                    bincounts[binn] += 1
            else:
                i += 1

        # Stop if all points in medbin are the same
        samepoints = 1
        for i in range(r + 1, n):
            if x[i] != x[r]:
                samepoints = 0
                break

        if samepoints:
            return x[r]

        # Stop if there's <= 20 points left
        if n - r <= 20:
            break

    # Perform insertion sort on the remaining points,
    # and then pick the kth smallest
    a, j = 0, 0
    for i in range(r + 1, n):
        a = x[i]
        j = i - 1
        while j >= r:
            if x[j] < a:
                break
            x[j + 1] = x[j]
            j -= 1
        x[j + 1] = a
    return x[r - 1 + k]

def output_binmed(x):
    """
    output median based on binmedian algo above
    easily generalizes to even case :)
    """
    n = len(x)
    if n % 2 == 1:
        return binmedian_compute(x=x, k=(n + 1) / 2)
    return (binmedian_compute(x=x, k=(n + 1) / 2) + binmedian_compute(x=x, k=n / 2)) / 2
