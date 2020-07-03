def normalize_locality_name(s):
    s = s.lower().replace(' - ', '-')
    s = s.replace('the corporation of the city of ', '')
    s = s.replace('the corporation of the town of ', '')
    s = s.replace('pastoral unincorporated area', 'pua')
    s = s.replace('district council', '')
    s = s.replace('regional council', '')
    s = s.replace('unincorporated sa', 'pua')

    s = s.replace(' province', '')
    s = s.replace(' oblast', '')

    s = s.replace(' shire', '')
    s = s.replace(' council', '')
    s = s.replace(' regional', '')
    s = s.replace(' rural', '')
    s = s.replace(' city', '')
    s = s.replace('the dc of ', '')
    s = s.replace('town of ', '')
    s = s.replace('city of ', '')
    if s.startswith('the '):
        s = s[4:]
    return s.strip()

