import os, os.path, pathlib, shutil
from Stat import Stat

class File(Stat):
    """
    def __init__(self, path):
        if not os.path.isabs(path): raise ValueError('引数pathは絶対パスにしてください。path=\'{}\''.format(path))
        super().__init__(path)

    def mk(self, path=None):
        if path is None: p = self.Path
        else: p = path
        self.Create(p)
        #if not os.path.isfile(p):
        #    with open(p, 'w') as f: pass
    def mk_dummy(self, size, path=None)
        if path is None: p = self.Path
        else: p = path
        self.CreateDummy(p, size)
        if not os.path.isfile(p):
            with open(p, 'wb') as f:
                f.write(b'\0'*size)

    def rm(self, path=None):
        if path is None: p = self.Path
        else: p = path
        self.Delete(p)
    def cp(self, dst): return self.Copy(self.Path, dst)
    def mv(self, dst):
        self.Path = self.Move(self.Path, dst)
        return self.Path
    def pack(self, dst): return self.Archive(self.Path, dst)
    def unpack(self, src, dst=None): self.UnArchive(src, dst)
    """

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
    def Copy(cls, src, dst):
        if os.path.isfile(src): return shutil.copy(src, dst)
    #def Copy(cls, src, dst): return shutil.copy(src, dst)
    @classmethod
    def Delete(cls, path):
        if cls.IsExist(path): os.remove(path)
    @classmethod
    def Move(cls, src, dst):
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            return shutil.move(src, dst)
    @classmethod
    def Archive(cls, src, dst):
        ext = os.path.splitext(dst)[1][1:]
        archive_exts = [f[0] for f in shutil.get_archive_formats()]
        if ext not in archive_exts : raise Exception('拡張子\'{}\'は不正値です。アーカイブ拡張子は次のいずれかのみ可能です。{}'.format(ext, archive_exts))
        head, tail = os.path.split(src)
        base_name = os.path.join(os.path.dirname(dst), tail)
        root_dir = os.path.join(os.path.dirname(dst), head)
        base_dir = tail
        return shutil.make_archive(base_name, ext, root_dir=root_dir, base_dir=base_dir)
    @classmethod
    def UnArchive(cls, src, dst=None):
        d = dst
        if dst is None: d = os.path.dirname(src)
        shutil.unpack_archive(src, d)
