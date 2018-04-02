import os, os.path, pathlib, shutil
from Stat import Stat

class File(Stat):
    def __init__(self, path):
        if not os.path.isabs(path): raise ValueError('引数pathは絶対パスにしてください。path=\'{}\''.format(path))
        super().__init__(path)

    def mk(self, path=None):
        if path is not None and os.path.isabs(path) and os.path.dirname(self.Path) not in path:
            raise ValueError('引数pathは未指定か次のパスの相対パス、または次のパス配下を指定してください。{}'.format(os.path.dirname(self.Path)))
        elif path is None: p = self.Path
        elif os.path.isabs(path): p = path
        else: p = os.path.join(os.path.dirname(self.Path), path)
        self.Create(p)
        self.__make_first(p)
    def __make_first(self, path):
        if not self.IsExist(path): self.Path = path
    def mk_dummy(self, size, path=None):
        if path is not None and os.path.isabs(path) and os.path.dirname(self.Path) not in path:
            raise ValueError('引数pathは未指定か次のパスの相対パス、または次のパス配下を指定してください。{}'.format(os.path.dirname(self.Path)))
        elif path is None: p = self.Path
        elif os.path.isabs(path): p = path
        else: p = os.path.join(os.path.dirname(self.Path), path)
        self.CreateDummy(p, size)
        self.__make_first(p)
        
    def rm(self, path=None):
        if path is not None and os.path.isabs(path) and os.path.basename(self.Path) not in path: raise ValueError('引数pathは未指定か次のパスの相対パス、または次のパス配下を指定してください。{}'.format(os.path.dirname(self.Path)))
        elif path is None: self.Delete(self.Path)
        elif os.path.isabs(path): self.Delete(path)
        else: self.Delete(os.path.join(self.Path, path))

    def cp(self, dst): return self.Copy(self.Path, dst)
    def mv(self, dst):
        self.Path = self.Move(self.Path, dst)
        return self.Path
    
    @classmethod
    def IsExist(cls, path): return os.path.isfile(path)
    @classmethod
    def Create(cls, path): cls.__Create(path, lambda f: None)
    @classmethod
    def CreateDummy(cls, path, size): cls.__Create(path, lambda f: f.write(b'\0'*size))
    @classmethod
    def __Create(cls, path, method):
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f: method(f)
    @classmethod
    def Delete(cls, path):
        if cls.IsExist(path): os.remove(path)
    @classmethod
    def Copy(cls, src, dst): 
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            return shutil.copy(src, dst)
        elif os.path.isdir(src): raise IsADirectoryError()
        else: raise FileNotFoundError()
    @classmethod
    def Move(cls, src, dst):
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            cls.Path = shutil.move(src, dst)
            return cls.Path
        elif os.path.isdir(src): raise IsADirectoryError()
        else: raise FileNotFoundError()
