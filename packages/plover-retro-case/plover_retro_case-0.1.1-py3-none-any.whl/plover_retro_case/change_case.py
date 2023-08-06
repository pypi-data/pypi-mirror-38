from plover.formatting import WORD_RX

def change_case(words, capPrev, capThis, delim):
    if len(words) != 2:
      return words[0]

    text = ''
    leftWord = words[0].rstrip()
    rightWord = words[1].rstrip()

    if capPrev:
      leftWord = leftWord[:1].upper() + leftWord[1:]

    if capThis:
      rightWord = rightWord[:1].upper() + rightWord[1:]

    text = leftWord + delim + rightWord
    return text
