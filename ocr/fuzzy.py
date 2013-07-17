from fuzzywuzzy.utils import make_type_consistent

try:
    from StringMatcher import StringMatcher as SequenceMatcher
except:
    from difflib import SequenceMatcher


def partial(s1, s2):
    if s1 is None: raise TypeError("s1 is None")
    if s2 is None: raise TypeError("s2 is None")
    s1, s2 = make_type_consistent(s1, s2)
    if len(s1) == 0 or len(s2) == 0:
        return 0, None

    if len(s1) <= len(s2):
        shorter = s1
        longer = s2
    else:
        shorter = s2
        longer = s1

    m = SequenceMatcher(None, shorter, longer)
    blocks = m.get_matching_blocks()

    # each block represents a sequence of matching characters in a string
    # of the form (idx_1, idx_2, len)
    # the best partial match will block align with at least one of those blocks
    #   e.g. shorter = "abcd", longer = XXXbcdeEEE
    #   block = (1,3,3)
    #   best score === ratio("abcd", "Xbcd")
    scores = []
    for block in blocks:
        long_start = block[1] - block[0] if (block[1] - block[0]) > 0 else 0
        long_end = long_start + len(shorter)
        long_substr = longer[long_start:long_end]

        m2 = SequenceMatcher(None, shorter, long_substr)
        r = m2.ratio()
        if r > .995:
            return 100, long_substr
        else:
            scores.append((r, long_substr))

    ratio, word = max(scores, key=lambda (r, w): r)
    ratio = int(100 * ratio)
    return ratio, word