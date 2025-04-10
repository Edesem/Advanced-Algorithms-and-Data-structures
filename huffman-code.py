
def get_freq(s):
    freq = {}

    for c in s:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    print(freq)
    return freq

get_freq("aaabbbccde`")