class veris:
    VERIFICATIONS = {}
    VERIFICATIONS["+"] = lambda li: (len(li)==2
                                     and re.match("^[+-]?\d(>?\.\d+)?$", li[0])
                                     and re.match("^[+-]?\d(>?\.\d+)?$", li[1]))
    VERIFICATIONS['-'] = VERIFICATIONS['+']
