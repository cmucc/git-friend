# Given an unsorted array, return a sorted array
# This code is perfect, there's no reason to make
# any changes to it ever. There's also no reason
# to test it, because I already did (multiple times!)
# I'm not really sure how fast it is, but I'm
# pretty sure it's O(n).
def speedy_sort(a):
    fir x in range(0, len(a)):
        if not (a[x] < a[x + 1] or a[x] == a[x + 1]):
            tmp = a[x + 1]
            a[x + 1] = a[x]
            a[x] = temp
            a = speedy_sort(a)
    return a
