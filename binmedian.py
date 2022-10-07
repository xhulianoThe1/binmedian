import statistics as st
import numpy as np

# implementing binmedian
def binmedian(x):
    n = len(x)
    mu = st.mean(x)
    sigma = st.stdev(x)

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

    ###TODO: optimize this
    if n % 2 == 1:
        k = (n + 1) / 2
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


test_list = [
    # [np.random.randint(0, 100) for _ in range(101)],
    [1, 3, 5],
    # [1, 3, 5, 7], ##even n
    # [1, 2, 3, 4, 5, 6], ##even n
    [1, 2, 3, 4, 5, 6, 9],
    # [2.25, 2.5, 2.5, 2.75, 2.75, 3.0, 3.0, 3.25, 3.5, 3.75], ##even n
    [2.25, 2.5, 2.5, 2.75, 2.75, 2.75, 3.0, 3.0, 3.25, 3.5, 3.75],
    # [220, 220, 240, 260, 260, 260, 260, 280, 280, 300, 320, 340], ##even n
    # [1, 2, 3, 4], ##even n
    [12, 12, 4],
    [12, 2, 4],
]

for i in test_list:
    print(
        f"The answer given {binmedian(i)}, this is {binmedian(i)==st.median(i)}, should be {st.median(i)}"
    )


# def my_version(x):
#     ## 1. Compute mean and std
#     B = 1000
#     n = len(x)
#     mu = st.mean(x)
#     sigma = st.stdev(x)
#     # form b bins
#     bins = np.linspace(mu - sigma, mu + sigma, B)
#     ##this is the idx withins the bins that each value is "in"
#     ## i.e. we are mapping each data pint to a bin
#     map_vals = np.digitize(x, bins)

#     n_l, n_i = 0, 0
#     for idx, val in enumerate(bins):
#         if idx in map_vals:
#             n_l += (map_vals == idx).sum()
#         n_i = (map_vals == idx).sum()
#         if n_l + n_i >= (n + 1) / 2:
#             b = idx + 1
#             break
#     # while:
#     print(x)
#     print(map_vals)
#     print(n_i)
#     print(n_l)
#     print(b)
#     print(bins[b])
#     return float(bins[b])


# # my_version([1, 3, 5, 6, 7])
# test_list = [
#     # [np.random.randint(0, 100) for _ in range(101)],
#     [1, 3, 5],
#     # # [1, 3, 5, 7], ##even n
#     # # [1, 2, 3, 4, 5, 6], ##even n
#     [1, 2, 3, 4, 5, 6, 9],
#     # # [2.25, 2.5, 2.5, 2.75, 2.75, 3.0, 3.0, 3.25, 3.5, 3.75], ##even n
#     [2.25, 2.5, 2.5, 2.75, 2.75, 2.75, 3.0, 3.0, 3.25, 3.5, 3.75],
#     # # [220, 220, 240, 260, 260, 260, 260, 280, 280, 300, 320, 340], ##even n
#     # # [1, 2, 3, 4], ##even n
#     # [12, 12, 4],
#     [12, 2, 4],
# ]

# # my_version([np.random.randint(0, 100) for _ in range(1010)])
# # my_version([1, 3, 5, 6, 7])

# for i in test_list:
#     print(
#         f"The answer given {my_version(i)}, this is {my_version(i)==st.median(i)}, should be {st.median(i)}"
#     )


#     ## count how many points lie in each of the bins
#     ## and to the left of the bins

#     n_l, n_i = 0, 0
#     for idx, val in enumerate(bins):
#         n_i += (map_vals == idx).sum()  # maybe idx
#         if n_l + n_i >= (n + 1) / 2:
#             b = idx
#             break
#         if idx in map_vals:
#             n_l += n_i

#     # print(n_i)
#     # print(n_l)
#     # print(x)
#     # print(bins)
#     print(map_vals)
#     print(b)
#     bins
#     # print(bins[map_vals[b]])
#     # print(x[map_vals == b])

#     # for idx, val in enumerate(x):
#     #     if n_l + val >= (n + 1) / 2:
#     #         # print("yes")
#     #         n_i = idx
#     #         break
#     #     # n_l = sum(bins[:idx])
#     #     if idx in map_vals:
#     #         n_l += 1
#     # # print(n_i)
#     # # print(n_l)
#     # # print(int(bins[map_vals[n_i]]))
#     # return int(bins[map_vals[n_i]])
#     # # print(n_i)


# # digitized = numpy.digitize(data, bins)
# # bin_means = [data[digitized == i].mean() for i in range(1, len(bins))]

# # test_list = [
# #     # [np.random.randint(0, 100) for _ in range(101)],
# #     # [1, 3, 5],
# #     # # [1, 3, 5, 7], ##even n
# #     # # [1, 2, 3, 4, 5, 6], ##even n
# #     [1, 2, 3, 4, 5, 6, 9],
# #     # # [2.25, 2.5, 2.5, 2.75, 2.75, 3.0, 3.0, 3.25, 3.5, 3.75], ##even n
# #     # [2.25, 2.5, 2.5, 2.75, 2.75, 2.75, 3.0, 3.0, 3.25, 3.5, 3.75],
# #     # # [220, 220, 240, 260, 260, 260, 260, 280, 280, 300, 320, 340], ##even n
# #     # # [1, 2, 3, 4], ##even n
# #     # [12, 12, 4],
# #     # [12, 2, 4],
# # ]

# # my_version([np.random.randint(0, 100) for _ in range(1010)])
# my_version([1, 3, 5, 6, 7])

# # for i in test_list:
# #     print(
# #         f"The answer given {my_version(i)}, this is {my_version(i)==st.median(i)}, should be {st.median(i)}"
# #     )

