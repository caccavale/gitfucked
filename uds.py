


class ulist:
    def __init__(self, *args):
        if len(args) == 0:
            self.data = ''
            self.full = False
        elif len(args) == 1:
            self.data = args[0]
            self.full = True
        else:
            raise ValueError('ulist.__init__: too many args')

    def __getitem__(self, i):
        if self.full and i == 0:
            return self.data
        else:
            raise IndexError('ulist.__getitem__(i): index out of range')

    def __setitem__(self, i, x):
        if i == 0:
            self.data = x
            self.full = True
        else:
            raise IndexError('ulist.__getitem__(i): index out of range')

    def __repr__(self):
        if self.full:
            return str([self.data])
        else:
            return str([])

    def append(self, x):
        if self.full:
            raise IndexError('ulist.append(x): index out of range')
        else:
            self.data = x
            self.full = True

    def extend(self, L):
        if type(L) != list:
            raise TypeError('ulist.extend(L): expects a list')
        if len(L) > 1:
            raise ValueError('ulist.extend(L): ulist cannot contain L')
        if self.full:
            raise IndexError('ulist.extend(L): index out of range')
        else:
            self.data = L[0]
            self.full = True

    def insert(self, i, x):
        if i != 0 or self.full:
            raise IndexError('ulist.insert(i, x): index out of range')
        else:
            self.data = x
            self.full = True

    def remove(self, x):
        if not self.full or x != self.data:
            raise ValueError('ulist.remove(x): x not in list')
        else:
            self.data = ''
            self.full = False

    def pop(self, *args): # i
        if not self.full or (len(args) > 0 and args[0] != 0):
            raise IndexError('ulist.pop([i]): index out of range')
        else:
            self.data = ''
            self.full = False

    def clear(self):
        self.data = ''
        self.full = False

    def index(self, x):
        if self.full and x == self.data:
            return 0
        else:
            raise ValueError('ulist.remove(x): x not in list')

    def count(self, x):
        if self.full and x == self.data:
            return 1
        else:
            return 0

    def sort(self, key=None, reverse=False):
        return

    def reverse(self):
        return

    def copy(self):
        if self.full:
            return ulist(self.data)
        else:
            return ulist()
