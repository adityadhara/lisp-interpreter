class funcs:
    FUNCTIONS = {}
    FUNCTIONS['+'] = lambda li: add(li)
    FUNCTIONS['-'] = lambda li: subtract(li)


    def add(li):
        if "." in li[0] or "." in li[1]:
            return float(li[0])+float(li[1])
        else:
            return int(li[0])+int(li[1])

    def subtract(li):
        if "." in li[0] or "." in li[1]:
            return float(li[0])-float(li[1])
        else:
            return int(li[0])-int(li[1])