import sys
from collections import UserDict

class ModuleFinderMap(UserDict):
    def __setitem__(self, name, value):
        '''call `partial(MetaFinder)(module_name=name)` and insert result to sys.meta_path'''
        value = value(name)
        sys.meta_path.insert(0, value)
        self.data[name] = value

    def __delitem__(self, name):
        sys.meta_path.remove(self.data[name])
        del self.data[name]

finder = ModuleFinderMap()
