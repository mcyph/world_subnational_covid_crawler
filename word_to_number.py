import re
from re import IGNORECASE


def word_to_number(s):
    # TODO: Convert a/an as well!!! =====================================
    #       "Both"
    #       hyphenated
    #       "first"/"second" etc

    less_than_20 = [
        'zero', 'one', 'two', 'three', 'four', 'five',
        'six', 'seven', 'eight', 'nine', 'ten',
        'eleven', 'twelve', 'thirteen', 'fourteen',
        'fifteen', 'sixteen', 'seventeen', 'eighteen',
        'nineteen'
    ]
    tens = [
        'twenty', 'thirty', 'forty', 'fifty', 'sixty',
        'seventy', 'eighty', 'ninety'
    ]

    for x, ten in enumerate(tens):
        ten = ten.lower()

        for y, num in enumerate(less_than_20):
            num = num.lower()
            s = re.sub(r'\b'+ten+' '+num+r'\b',
                       str((10*(x+2))+y), s,
                       flags=IGNORECASE)
        s = re.sub(r'\b%s\b' % str(10*(x+2)), str(x), s,
                   flags=IGNORECASE)

    for x, num in enumerate(less_than_20):
        num = num.lower()
        s = re.sub(r'\b%s\b' % num, str(x), s,
                   flags=IGNORECASE)
    return s


if __name__ == '__main__':
    print(word_to_number('dsajkldjsa gklrewfjkd twenty five four five'))
