
fname = '/Users/mehdi/PycharmProjects/PyKEEN/data/train.txt'
fname2 = '/Users/mehdi/PycharmProjects/PyKEEN/data/valid.txt'

with open(fname) as f:
    content = f.readlines()

with open(fname2) as f:
    content2 = f.readlines()

l = [item for item in content if item in content2]

print(l)