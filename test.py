one = {999, 888,777,666,555,199}
import copy
two = copy.deepcopy(one)
two.remove(999)
# one.remove(999)

print('one', one, '\ntwo:',two)