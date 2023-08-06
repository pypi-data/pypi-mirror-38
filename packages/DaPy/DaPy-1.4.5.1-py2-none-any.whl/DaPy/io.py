from os import path

__all__ = ['read', 'save', 'encode']


def read(addr, dtype='col', **kward):
    '''dp.read('file.xlsx') -> return DataSet object
        more info on help(dp.DataSet.read)
    '''
    from core import DataSet
    data = DataSet()
    data.read(addr, dtype, **kward)
    return data

def save(addr, data, sheet='sheet0', decode='utf-8', encode='utf-8'):
    '''dp.save('file.xlsx', [1,2,3,4]) -> save dataset into file
        more info on help(dp.DataSet.read)
    '''
    from core import DataSet
    data = DataSet(data, sheet=sheet)
    data.save(addr, decode=decode, encode=encode, sheet=sheet)

def encode(code='cp936'):
    '''change the python environment encode
    '''
    import sys
    stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
    reload(sys)
    sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
    sys.setdefaultencoding(code)
    return


