#ONE(seq): returns true if there is only one true element in the sequence
def one(seq):
    
    if not hasattr(seq, '__iter__'):
        return False #object not iterable, i.e. not a sequence
    
    found_one = False
    for v in seq:
        if bool(v) == True:
            if found_one:
                return False
            else:
                found_one = True
    return found_one

#INJECT(fun): returns an injector function of the kind: INJECTOR(seq, [init])
def inject(fun):
    
    def myinjector(seq, init=None):
        if not hasattr(seq, '__iter__'):
            return seq

        if init is not None:
            result = fun(init, seq[0])
        else:
            result = seq[0]

        for v in seq[1:]:
            result = fun(result, v)

        return result
    
    return myinjector

#UNFOLD(initial, step, condition, [skip])
def unfold(initial, step, condition, skip=None):
    if not hasattr(step, "__call__") or not hasattr(condition, "__call__"):
        return initial

    if skip is not None and not hasattr(skip, "__call__"):
        skip = None

    result = []
    #initial could not satisfy condition or skip, that's why one
    #should not be prejudiced as to the inclusion of the initial
    #value in the result

    current_result = initial

    while condition(current_result):
        if skip is None or not skip(current_result):
            result.append(current_result)

        current_result = step(current_result)

    return result
        
#THETA(predicate, *sequences): theta join on sequences usising a predicate
def theta(predicate, *sequences):
    from itertools import product
    mygen = product(*sequences)

    result = []
    for v in mygen:
        if(predicate(*v)):
            result.append(v)

    return result

#MEMOIZE(fun): ...
def memoize(fun):

    remembered_values = {}
    
    def memoized_function(*seq):

        if seq not in remembered_values:
            remembered_values.update({seq : fun(*seq)})
            #print("adding value!")

        return remembered_values[seq]

    def graph_function():
        result = []
        for k in remembered_values: #dunno why dict doesn't seem to implement iteritems() anymore
            #result.append((k, remembered_values[k])) #<- this is the more general way, i.e. (args, return_value)
            result.append(k+(remembered_values[k],))
        return result
        
    return memoized_function, graph_function
