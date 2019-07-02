from functools import reduce

test = [1, 2, 3, 4, 5]
test_sum = reduce(lambda val, acc: val + acc, test)
print(test_sum)
