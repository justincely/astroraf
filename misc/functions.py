
__all__ = ['unpickle']

def unpickle(pickled_object):
    import pickle
    return pickle.load( open(pickled_object,'r') )
