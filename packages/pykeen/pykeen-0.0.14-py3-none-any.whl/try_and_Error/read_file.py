
fname = '/Users/mehdi/PycharmProjects/PyKEEN/data/train.txt'
fname2 = '/Users/mehdi/PycharmProjects/PyKEEN/data/test.txt'

with open(fname) as f:
    content = f.readlines()

with open(fname2) as f:
    content2 = f.readlines()

l = [item for item in content2 if item in content]

print(len(l))