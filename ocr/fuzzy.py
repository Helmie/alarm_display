from difflib import SequenceMatcher

from fuzzywuzzy.utils import make_type_consistent


def bitap(text, pattern, loc=0):
    """Locate the best instance of 'pattern' in 'text' near 'loc' using the
    Bitap algorithm.
  
    Args:
      text: The text to search.
      pattern: The pattern to search for.
      loc: The location to search around.
  
    Returns:
      Best match index or -1.
    """
    # Python doesn't have a maxint limit, so ignore this check.
    #if self.Match_MaxBits != 0 and len(pattern) > self.Match_MaxBits:
    #  raise ValueError("Pattern too long for this application.")

    # Initialise the alphabet.
    s = match_alphabet(pattern)

    def match_bitapScore(e, x):
        """Compute and return the score for a match with e errors and x location.
        Accesses loc and pattern through being a closure.
    
        Args:
          e: Number of errors in match.
          x: Location of match.
    
        Returns:
          Overall score for match (0.0 = good, 1.0 = bad).
        """
        accuracy = float(e) / len(pattern)
        proximity = abs(loc - x)
        return accuracy + (proximity / 1000)

    # Highest score beyond which we give up.
    score_threshold = 1.0
    # Is there a nearby exact match? (speedup)
    best_loc = text.find(pattern, loc)
    if best_loc != -1:
        score_threshold = min(match_bitapScore(0, best_loc), score_threshold)
        # What about in the other direction? (speedup)
        best_loc = text.rfind(pattern, loc + len(pattern))
        if best_loc != -1:
            score_threshold = min(match_bitapScore(0, best_loc), score_threshold)

    # Initialise the bit arrays.
    matchmask = 1 << (len(pattern) - 1)
    best = (0.0, -1, -1)

    bin_max = len(pattern) + len(text)
    # Empty initialization added to appease pychecker.
    last_rd = None
    for d in xrange(len(pattern)):
        # Scan for the best match each iteration allows for one more error.
        # Run a binary search to determine how far from 'loc' we can stray at
        # this error level.
        bin_min = 0
        bin_mid = bin_max
        while bin_min < bin_mid:
            if match_bitapScore(d, loc + bin_mid) <= score_threshold:
                bin_min = bin_mid
            else:
                bin_max = bin_mid
            bin_mid = (bin_max - bin_min) // 2 + bin_min

        # Use the result from this iteration as the maximum for the next.
        bin_max = bin_mid
        start = max(1, loc - bin_mid + 1)
        finish = min(loc + bin_mid, len(text)) + len(pattern)

        rd = [0] * (finish + 2)
        rd[finish + 1] = (1 << d) - 1
        for j in xrange(finish, start - 1, -1):
            if len(text) <= j - 1:
                # Out of range.
                charMatch = 0
            else:
                charMatch = s.get(text[j - 1], 0)
            if d == 0:  # First pass: exact match.
                rd[j] = ((rd[j + 1] << 1) | 1) & charMatch
            else:  # Subsequent passes: fuzzy match.
                rd[j] = (((rd[j + 1] << 1) | 1) & charMatch) | (
                    ((last_rd[j + 1] | last_rd[j]) << 1) | 1) | last_rd[j + 1]
            if rd[j] & matchmask:
                score = match_bitapScore(d, j - 1)
                # This match will almost certainly be better than any existing match.
                # But check anyway.
                if score <= score_threshold:
                    # Told you so.
                    score_threshold = score
                    begin = j - 1
                    end = begin + len(pattern)
                    best = 1.0 - score, text[begin:end], begin, end
                    if begin > loc:
                        # When passing loc, don't exceed our current distance from loc.
                        start = max(1, 2 * loc - begin)
                    else:
                        # Already passed loc, downhill from here on in.
                        break
        # No hope for a (better) match at greater error levels.
        if match_bitapScore(d + 1, loc) > score_threshold:
            break
        last_rd = rd

    return best


def match_alphabet(pattern):
    """Initialise the alphabet for the Bitap algorithm.
  
    Args:
      pattern: The text to encode.
  
    Returns:
      Hash of character locations.
    """
    s = {}
    for char in pattern:
        s[char] = 0
    for i in xrange(len(pattern)):
        s[pattern[i]] |= 1 << (len(pattern) - i - 1)
    return s


def substring(longer, shorter):
    if len(longer) is 0 or len(shorter) is 0:
        return 0.0, None, None, None

    def substrings(string):
        for i in range(len(string)):
            for j in range(i + 1, len(string) + 1):
                yield string[i:j], i, j

    matcher = SequenceMatcher(None, shorter)

    lines = longer.splitlines()
    bests = []

    for line_number, line in enumerate(lines):
        matches = []

        for substring, start, end in substrings(line):
            matcher.set_seq2(substring)
            match = matcher.ratio(), substring, start
            matches.append(match)

        if matches:
            ratio, word, start = max(matches, key=lambda (r, w, s): r)
            best = ratio, word, line_number, start
            bests.append(best)

    if bests:
        ratio, word, line_number, start = max(bests, key=lambda (r, w, l, s): r)
        lines = lines[:line_number]
        # don't forget to count newlines
        offset = reduce(lambda count, line: count + len(line), lines, len(lines))

        return ratio, word, offset + start, offset + start + len(word)
    else:
        return 0.0, None, None, None


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
    print blocks
    for block in blocks:
        long_start = block[1] - block[0] if (block[1] - block[0]) > 0 else 0
        long_end = long_start + len(shorter)
        long_substr = longer[long_start:long_end]

        m2 = SequenceMatcher(None, shorter, long_substr)
        r = m2.ratio()
        if r > .995:
            return 100, long_substr, long_start, long_end
        else:
            scores.append((r, long_substr, long_start, long_end))

    print scores
    ratio, word, start, end = max(scores, key=lambda (r, w, s, e): r)
    ratio = int(100 * ratio)
    return ratio, word, start, end