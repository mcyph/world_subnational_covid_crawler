import re
from re import IGNORECASE


def word_to_number(s):
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
    ordinals = [
        'first', 'second', 'third', 'fourth', 'fifth',
        'sixth', 'seventh', 'eighth', 'ninth', 'tenth'
    ]

    s = re.sub(r'\b(a|an)\b', '1', s,
               flags=IGNORECASE)
    s = re.sub(r'\bboth\b', '2', s,
               flags=IGNORECASE)

    for x, ten in enumerate(tens):
        ten = ten.lower()

        for y, num in enumerate(less_than_20):
            num = num.lower()
            s = re.sub(r'\b'+ten+' '+num+r'\b',
                       str((10*(x+2))+y), s,
                       flags=IGNORECASE)
            s = re.sub(r'\b'+ten+'-'+num+r'\b',
                       str((10*(x+2))+y), s,
                       flags=IGNORECASE)
        s = re.sub(r'\b%s\b' % ten, str(10*(x+2)), s,
                   flags=IGNORECASE)

    for x, num in enumerate(less_than_20):
        num = num.lower()
        s = re.sub(r'\b%s\b' % num, str(x), s,
                   flags=IGNORECASE)

    # Convert "first case" etc to "1 case"
    for x, ordinal in enumerate(ordinals):
        ordinal = ordinal.lower()
        s = re.sub(r'\b%s\b' % ordinal, '1', s,
                   flags=IGNORECASE)

    return s


if __name__ == '__main__':
    print(word_to_number('dsajkldjsa gklrewfjkd twenty five four five'))
    print(word_to_number('20 March 2020'))
    print(word_to_number('first case'))
    print(word_to_number('The new cases include 18 males and 12 females, aged between 21 and 80.'))
    print(word_to_number('Both cases are men. One is from Southern Tasmania and one is from Northern Tasmania. One is aged in their 20s and the other is in their 70s.'))
    print(word_to_number('Tasmania has today confirmed six more cases of coronavirus'))
