import re
from re import compile, IGNORECASE


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

    out = []
    for x, ten in enumerate(tens):
        ten = ten.lower()
        for y, num in enumerate(less_than_20):
            num = num.lower()
            out.append(rf'\b{ten})[- ]({num}\b')

    RE_TEN_COMBS = compile('(%s)' % '|'.join(out),
                           flags=IGNORECASE)
    RE_TENS = compile('(%s)' % '|'.join(tens),
                      flags=IGNORECASE)
    RE_LESS_THAN_20 = compile('(%s)' % '|'.join(less_than_20),
                              flags=IGNORECASE)
    RE_ORDINALS = compile('(%s)' % '|'.join(ordinals),
                          flags=IGNORECASE)

    def replace_ten_combs(ten, num):
        return str(
           ((tens.index(ten.group().lower())+2)*10) +
           less_than_20.index(num.lower())
        )

    def replace_tens(ten):
        return str((tens.index(ten.group().lower())+2)*10)

    def replace_less_than_20(num):
        return str(less_than_20.index(num.group().lower()))

    def replace_ordinals(num):
        # Convert "first case" etc to "1 case"
        return str(ordinals.index(num.group().lower()))

    s = RE_TEN_COMBS.sub(replace_ten_combs, s)
    s = RE_TENS.sub(replace_tens, s)
    s = RE_LESS_THAN_20.sub(replace_less_than_20, s)
    s = RE_ORDINALS.sub(replace_ordinals, s)

    return s


if __name__ == '__main__':
    print(word_to_number('dsajkldjsa gklrewfjkd twenty five four five'))
    print(word_to_number('20 March 2020'))
    print(word_to_number('first case'))
    print(word_to_number('The new cases include 18 males and 12 females, aged between 21 and 80.'))
    print(word_to_number('Both cases are men. One is from Southern Tasmania and one is from Northern Tasmania. One is aged in their 20s and the other is in their 70s.'))
    print(word_to_number('Tasmania has today confirmed six more cases of coronavirus'))
