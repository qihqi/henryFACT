

def valid(w):
    try:
        float(w)
        return False
    except ValueError:
        if w in ['DE'] or 'x' in w:
            return False
        return True

with open('lista.csv') as f:
    lines = f.readlines()
    word_set = set()
    for l in lines:
        words = l.split(';')[1].split()
        for w in words:
            if valid(w):
                word_set.add(w)
    li = sorted(word_set)
    for w in li:
        print w,';'
