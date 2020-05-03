import re
from re import compile, IGNORECASE


def word_to_number(s):
    # HACK: replace no-break spaces; get rid of zero width spaces!
    s = s.replace('&nbsp;', ' ') \
         .replace('\u200b', '') \
         .replace('&#8203;', '')

    def longest_first(nums):
        return list(sorted(nums, key=lambda x: -len(x)))

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
    s = re.sub(r'\bno\b', '0', s,
               flags=IGNORECASE)

    out = []
    for x, ten in enumerate(tens):
        ten = ten.lower()
        for y, num in enumerate(less_than_20):
            num = num.lower()
            out.append(rf'\b{ten}[\- ]{num}\b')

    RE_TEN_COMBS = compile(
        '(%s)' % '|'.join(longest_first(out)),
        flags=IGNORECASE
    )
    RE_TENS = compile(
        '(%s)' % '|'.join(longest_first([
            rf'\b{ten}\b'
            for ten in tens
        ])),
        flags=IGNORECASE
    )
    RE_LESS_THAN_20 = compile(
        '(%s)' % '|'.join(longest_first([
            rf'\b{num}\b'
            for num in less_than_20
        ])),
        flags=IGNORECASE
    )
    RE_ORDINALS = compile(
        '(%s)' % '|'.join(longest_first([
            rf'\b{ordinal}\b'
            for ordinal in ordinals
        ])),
        flags=IGNORECASE
    )

    def replace_ten_combs(ten_num):
        ten, num = ten_num.group(0).replace('-', ' ').split()
        return str(
           ((tens.index(ten.lower())+2)*10) +
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

    for i in range(1, 10):
        # HACK: basic support for hundreds!!!
        s = s.replace(f'{i} hundred and ', str(i))
        s = s.replace(f'{i} Hundred and ', str(i))

    return s


if __name__ == '__main__':
    print(word_to_number('dsajkldjsa gklrewfjkd twenty five four five'))
    print(word_to_number('20 March 2020'))
    print(word_to_number('first case'))
    print(word_to_number('The new cases include 18 males and 12 females, aged between 21 and 80.'))
    print(word_to_number('Both cases are men. One is from Southern Tasmania and one is from Northern Tasmania. One is aged in their 20s and the other is in their 70s.'))
    print(word_to_number('Tasmania has today confirmed six more cases of coronavirus'))
    print(word_to_number('Two hundred and forty-eight people have recovered'))
    print(word_to_number('fourteen'))
    print(word_to_number('There are currently 12 COVID-19 cases in our Intensive Care Units and of those cases, 8 require ventilators at this stage.'))
    print(word_to_number('<p>Sadly, NSW Health  confirms the death of 3 people from COVID-19, bringing the state’s total deaths  of confirmed COVID-19 cases to <strong>21.</strong></p>'))
