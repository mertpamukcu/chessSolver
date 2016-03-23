class UniqueElement(object):
    """ Used to find out all unique permutations in remaining empty areas for same kind of pieces """
    def __init__(self, value, occurrences):
        self.value = value
        self.occurrences = occurrences

def perm_unique(elements):
    """ Used to find out all unique permutations in remaining empty areas for same kind of pieces """
    eset = set(elements)
    listunique = [UniqueElement(i, elements.count(i)) for i in eset]
    element_count = len(elements)
    return list(perm_unique_helper(listunique, [0] * element_count, element_count - 1))

def perm_unique_helper(listunique, result_list, element_count):
    """ Used to find out all unique permutations in remaining empty areas for same kind of pieces """
    if element_count < 0:
        yield tuple(result_list)
    else:
        for i in listunique:
            if i.occurrences > 0:
                result_list[element_count] = i.value
                i.occurrences -= 1
                for g in  perm_unique_helper(listunique, result_list, element_count - 1):
                    yield g
                i.occurrences += 1
