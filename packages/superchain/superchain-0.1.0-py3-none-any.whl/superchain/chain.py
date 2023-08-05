

class chain(object):
    def __init__(self, *args):
        if not args:
            self.keys = None
            self.values = []
        elif isinstance(args[0], str):
            self.keys = list(args)
        elif isinstance(args[0], (tuple, list)):
            self.keys = list(args[0])
        else:
            raise Exception('args must be a list or tuple of types')
        self.values = []

    def addkeys(self, keys):
        if isinstance(keys, (tuple, list)):
            self.keys = list(keys)
        else:
            self.keys = None
            raise Exception('args must be a list or tuple of types')

    def getkeys(self):
        return self.keys

    def getvalues(self):
        return self.values

    def add(self, *args):
        if not args:
            raise Exception('inputs is illegal')
        elif len(args) != 1:
            self.values = list(args)
        elif isinstance(args[0], (tuple, list)):
            if len(args[0]) > len(self.keys):
                raise Exception('The len of values(%s) > the len of keys(%s)' % (len(args[0]), len(self.keys)))
            self.values = list(args[0])
        else:
            raise Exception('args must be a list or tuple of types')

    def get(self, *args):
        if not args:
            return self.values
        is_in = True
        for arg in args:
            if arg not in self.values:
                is_in = False
        if is_in:
            return self.values
        else:
            return []

    def getdict(self):
        temp_dict = {}
        for key in self.keys:
            temp_dict[key] = self.values[self.keys.index(key)]
        return temp_dict

    def delete(self):
        del self.keys
        del self.values
        return None


if __name__ == '__main__':
    c0 = chain()
    c1 = chain('app', 'job')
    c2 = chain(['job', 'model'])
    c3 = chain(('job', 'model'))
    # c3 = chain({'job', 'model'})
    print(c0.getkeys())
    print(c0.delete())
    print(type(c0))
    # print(c1.getkeys())
    # print(c2.getkeys())
    # print(c2.getvalues())
    # # print(c3.getkeys())
    # c1.add(1, 2)
    # print(c1)
    # print(c1.values)
    # print(c1.get())
    # print(c1.get(3))
    # print(c2.getkeys())
    # c2.add(('a', 'b'))
    # print(c2.getkeys())
    # print(c2.getvalues())
    # print(c2.get())
    # print(c2.getdict())
    # print(c2.getvalues())
