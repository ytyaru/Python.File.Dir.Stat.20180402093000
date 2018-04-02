import sys, os, os.path, pathlib
print(pathlib.Path(__file__).parent.parent / 'src')
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from Directory import Directory
import unittest
import time, datetime

class DirectoryTest(unittest.TestCase):
    # ----------------------------
    # クラスメソッド
    # ----------------------------
    def test_IsExist(self):
        self.assertTrue(Directory.IsExist(os.getcwd()))
        self.assertTrue(not Directory.IsExist('/NotExistDir'))

    def test_Create_Delete(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        self.assertTrue(Directory.IsExist(target))
        Directory.Delete(target)
        self.assertTrue(not Directory.IsExist(target))
        target = '/tmp/work/__TEST__/A/B/C'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        self.assertTrue(Directory.IsExist(target))
        Directory.Delete(target)
        self.assertTrue(not Directory.IsExist(target))
        target = '/tmp/work/__TEST__'
        Directory.Delete(target)

    def test_Copy_single(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        Directory.Copy(target, '/tmp/work/__TEST_2__')
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Delete(target)
        Directory.Delete('/tmp/work/__TEST_2__')

    def test_Copy_tree(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        Directory.Create(os.path.join(target, 'A'))
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Copy(target, '/tmp/work/__TEST_2__')
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST_2__/A/a.txt'))
        Directory.Delete(target)
        Directory.Delete('/tmp/work/__TEST_2__')
    
    def test_Move_single(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Create(target)
        Directory.Move(target, '/tmp/work/__TEST_2__')
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Delete('/tmp/work/__TEST_2__')

    def test_Move_tree(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Create(target)
        Directory.Create(os.path.join(target, 'A'))
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        
        Directory.Move(target, '/tmp/work/__TEST_2__')
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST_2__/A/a.txt'))
        Directory.Delete('/tmp/work/__TEST_2__')

    def test_Archive(self):
         self.__make_archive()
         os.remove('/tmp/work/__TEST__' + '.zip')

    def __make_archive(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        Directory.Create(os.path.join(target, 'A'))
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        
        Directory.Archive(target, target + '.zip')
        self.assertTrue(os.path.isfile(target + '.zip'))
        Directory.Delete(target)

    def test_UnArchive(self):
        self.__make_archive()
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST__'))
        Directory.UnArchive('/tmp/work/__TEST__.zip')
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__'))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST__/A/a.txt'))
        Directory.Delete('/tmp/work/__TEST__')
        os.remove('/tmp/work/__TEST__.zip')
    # ----------------------------
    # インスタンスメソッド
    # ----------------------------
    def test_init_relative_error(self):
        with self.assertRaises(ValueError) as e:
            d = Directory('A')
        self.assertEqual('引数pathは絶対パスにしてください。path=\'{}\''.format('A'), e.exception.args[0])

    def test_mk_rm(self):
        target_root = '/tmp/work/__TEST__'
        d = Directory(target_root)
        self.assertTrue(not Directory.IsExist(target_root))
        self.assertTrue(d.Stat is None)
        d.mk()
        self.assertEqual(target_root, d.Path)
        self.assertTrue(d.Stat is not None)
        self.assertTrue(Directory.IsExist(target_root))
        self.assertTrue(not Directory.IsExist(os.path.join(target_root, 'A')))
        d.mk('A')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(Directory.IsExist(os.path.join(target_root, 'A')))
        self.assertTrue(not Directory.IsExist(os.path.join(target_root, 'B/BB/BBB')))
        d.mk('B/BB/BBB')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(Directory.IsExist(os.path.join(target_root, 'B/BB/BBB')))
        self.assertTrue(not Directory.IsExist(os.path.join('/tmp/work/__TEST__/C')))
        d.mk('/tmp/work/__TEST__/C')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(Directory.IsExist(os.path.join('/tmp/work/__TEST__/C')))

        d.rm('B/BB/BBB')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not Directory.IsExist(os.path.join(target_root, 'B/BB/BBB')))
        self.assertTrue(Directory.IsExist(os.path.join(target_root, 'B/BB')))
        d.rm('/tmp/work/__TEST__/B/BB')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not Directory.IsExist(os.path.join('/tmp/work/__TEST__/B/BB')))
        d.rm(target_root)
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not Directory.IsExist(target_root))
    
    def test_mk_rm_raise(self):
        target_root = '/tmp/work/__TEST__'
        d = Directory(target_root)
        d = Directory(target_root)
        self.assertTrue(not Directory.IsExist(target_root))
        with self.assertRaises(ValueError) as e:
            d.mk('/tmp/work/A')
        self.assertEqual('引数pathは未指定か次のパスの相対パス、または次のパス配下を指定してください。{}'.format(target_root), e.exception.args[0])
        with self.assertRaises(ValueError) as e:
            d.rm('/tmp/work/A')
        self.assertEqual('引数pathは未指定か次のパスの相対パス、または次のパス配下を指定してください。{}'.format(target_root), e.exception.args[0])

    def test_cp_single(self):
        target_root = '/tmp/work/__TEST__'
        d = Directory(target_root)
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not Directory.IsExist(target_root))
        d.mk()
        self.assertEqual(target_root, d.Path)
        self.assertTrue(Directory.IsExist(target_root))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
        res = d.cp('/tmp/work/__TEST_2__')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        self.assertEqual('/tmp/work/__TEST_2__', res)
        self.assertEqual('/tmp/work/__TEST__', d.Path)
        d.rm()
        self.assertEqual(target_root, d.Path)
        Directory.Delete('/tmp/work/__TEST__')
        Directory.Delete('/tmp/work/__TEST_2__')
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST__'))

    def test_cp_tree(self):
        target_root = '/tmp/work/__TEST__'
        d = Directory(target_root)
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not Directory.IsExist(d.Path))
        with self.assertRaises(FileNotFoundError) as e:
            d.cp('/tmp/work/__TEST_2__')
        d.mk()
        self.assertEqual(target_root, d.Path)
        self.assertTrue(Directory.IsExist(d.Path))
        d.mk('A')
        self.assertEqual(target_root, d.Path)
        pathlib.Path(os.path.join(target_root, 'A/a.txt')).touch()
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
        d.cp('/tmp/work/__TEST_2__')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST_2__/A/a.txt'))
        d.rm()
        self.assertEqual(target_root, d.Path)
        Directory.Delete('/tmp/work/__TEST_2__')
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST__'))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
    
    def test_mv_single(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))

        d = Directory(target)
        self.assertEqual(target, d.Path)
        with self.assertRaises(FileNotFoundError) as e:
            d.mv('/tmp/work/__TEST_2__')

        d.mk()
        self.assertEqual(target, d.Path)
        self.assertTrue(Directory.IsExist(target))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))

        d.mv('/tmp/work/__TEST_2__')
        self.assertEqual('/tmp/work/__TEST_2__', d.Path)
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Delete('/tmp/work/__TEST_2__')
        Directory.Delete('/tmp/work/__TEST__')

    def test_mv_tree(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))

        d = Directory(target)
        self.assertEqual(target, d.Path)
        with self.assertRaises(FileNotFoundError) as e:
            d.mv('/tmp/work/__TEST_2__')

        #d.mk()
        d.mk('A')
        self.assertEqual(target, d.Path)
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST__/A/a.txt'))

        d.mv('/tmp/work/__TEST_2__')
        self.assertEqual('/tmp/work/__TEST_2__', d.Path)
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST_2__/A/a.txt'))
        Directory.Delete('/tmp/work/__TEST_2__')
        Directory.Delete('/tmp/work/__TEST__')
    
    def test_pack(self):
         self.__make_pack()
         os.remove('/tmp/work/__TEST__' + '.zip')

    def __make_pack(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))

        d = Directory(target)
        d.mk('A')
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        
        self.assertTrue(not os.path.isfile(target + '.zip'))
        d.pack(target + '.zip')
        self.assertTrue(os.path.isfile(target + '.zip'))
        self.assertEqual(target, d.Path)

        d.rm()
        self.assertTrue(not Directory.IsExist(target))
        Directory.Delete(target)
        return d

    def test_unpack(self):
        d = self.__make_pack()
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST__'))

        d.unpack('/tmp/work/__TEST__.zip', os.path.dirname(d.Path))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__'))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST__/A/a.txt'))
        d.rm()
        
        d.unpack('/tmp/work/__TEST__.zip')
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__'))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST__/A/a.txt'))
        d.rm()

        d.unpack('/tmp/work/__TEST__.zip', d.Path)
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__/__TEST__'))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__/__TEST__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST__/__TEST__/A/a.txt'))
        d.rm()

        os.remove('/tmp/work/__TEST__.zip')
    # ----------------------------
    # Stat
    # ----------------------------
    def __MakeDummy(self, path, size):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.isfile(path): os.remove(path) # メタデータ初期化
        with open(path, 'wb') as f:
            f.write(b'\0'*size)
    # ----------------------------
    # クラスメソッド
    # ----------------------------
    def test_GetSize(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Directory, 'GetSize'))
        print('Dir Size is {}'.format(Directory.GetSize(target_root)))
        self.assertEqual(1024, Directory.GetSize(target_root))

        path_b = os.path.join(target_root, 'B')
        Directory.Create(path_b)
        self.__MakeDummy(os.path.join(path_b, 'b.dummy'), 1024)
        self.assertEqual(2048, Directory.GetSize(target_root))

        path_c = os.path.join(target_root, 'C')
        Directory.Create(path_c)
        self.__MakeDummy(os.path.join(path_c, 'c.dummy'), 1024)
        self.assertEqual(3072, Directory.GetSize(target_root))

        path_bb = os.path.join(target_root, 'B/BB')
        Directory.Create(path_bb)
        self.__MakeDummy(os.path.join(path_bb, 'bb.dummy'), 1024)
        self.assertEqual(4096, Directory.GetSize(target_root))

        Directory.Delete(target_root)
    
    def test_DiskUsage(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Directory, 'DiskUsage'))
        res = Directory.DiskUsage(target_dummy)
        self.assertTrue(hasattr(res, 'total'))
        self.assertTrue(hasattr(res, 'used'))
        self.assertTrue(hasattr(res, 'free'))
        print(Directory.DiskUsage(target_dummy))
        Directory.Delete(target_root)

    def test_Mode_Get_Set_Name(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        mode = Directory.GetMode(target_dummy)
        print(mode)
        print(oct(mode))
        Directory.SetMode(target_dummy, 0o755)
        self.assertEqual(0o100755, Directory.GetMode(target_dummy))
        self.assertEqual('-rwxr-xr-x', Directory.GetModeName(target_dummy))
        Directory.SetMode(target_dummy, '-rwxrwxrwx')
        self.assertEqual(0o100777, Directory.GetMode(target_dummy))
        Directory.SetMode(target_dummy, 0o644)
        self.assertEqual(0o100644, Directory.GetMode(target_dummy))
        self.assertEqual('-rw-r--r--', Directory.GetModeName(target_dummy))
        Directory.Delete(target_root)
    
    def test_SetModeFromName_Error(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        mode_name = 'Invalid-Text'
        with self.assertRaises(ValueError) as e:
            Directory.SetMode(target_dummy, mode_name )
        mode_names = [
            '---',
            '--x',
            '-w-',
            '-wx',
            'r--',
            'r-x',
            'rw-',
            'rwx'
        ]
        self.assertEqual('引数mode_nameが不正値です。\'{}\'。\'-rwxrwxrwx\'の書式で入力してください。owner, group, other, の順に次のパターンのいずれかを指定します。pattern={}。r,w,xはそれぞれ、読込、書込、実行の権限です。-は権限なしを意味します。'.format(mode_name, mode_names), e.exception.args[0])
        Directory.Delete(target_root)

    def test_Modified_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(Directory.GetModified(target_dummy)))
        self.assertTrue(2 == len(Directory.GetModified(target_dummy)))
        self.assertTrue(float == type(Directory.GetModified(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(Directory.GetModified(target_dummy)[1]))
        #print(type(Directory.GetModified(target_dummy)[0]))
        #print(type(Directory.GetModified(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = Directory.GetModified(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        Directory.SetModified(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == Directory.GetModified(target_dummy)[0])
        self.assertTrue(dt1 == Directory.GetModified(target_dummy)[1])
        self.assertTrue(dt1 != Directory.GetChangedMeta(target_dummy)[1])
        self.assertTrue(dt1 != Directory.GetAccessed(target_dummy)[1])
        Directory.Delete(target_root)

    def test_Accessed_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(Directory.GetAccessed(target_dummy)))
        self.assertTrue(2 == len(Directory.GetAccessed(target_dummy)))
        self.assertTrue(float == type(Directory.GetAccessed(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(Directory.GetAccessed(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = Directory.GetAccessed(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        Directory.SetAccessed(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == Directory.GetAccessed(target_dummy)[0])
        self.assertTrue(dt1 == Directory.GetAccessed(target_dummy)[1])
        self.assertTrue(dt1 != Directory.GetModified(target_dummy)[1])
        self.assertTrue(dt1 != Directory.GetChangedMeta(target_dummy)[1])
        Directory.Delete(target_root)

    def test_GetChangedMeta(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Directory, 'GetChangedMeta'))
        self.assertTrue(hasattr(Directory, 'GetCreated'))
        print(Directory.GetChangedMeta(target_dummy))
        print(Directory.GetCreated(target_dummy))
        Directory.Delete(target_root)

    def test_Ids(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Directory, 'OwnUserId'))
        self.assertTrue(hasattr(Directory, 'OwnGroupId'))
        self.assertTrue(hasattr(Directory, 'HardLinkNum'))
        self.assertTrue(hasattr(Directory, 'INode'))
        self.assertTrue(hasattr(Directory, 'DeviceId'))
        print(Directory.GetOwnUserId(target_dummy))
        print(Directory.GetOwnGroupId(target_dummy))
        print(Directory.GetHardLinkNum(target_dummy))
        print(Directory.GetINode(target_dummy))
        print(Directory.GetDeviceId(target_dummy))
        Directory.Delete(target_root)

    # ----------------------------
    # インスタンスメソッド
    # ----------------------------
    def test_Stat(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        self.assertEqual(Directory, type(s))
        self.assertEqual(os.stat_result, type(s.Stat))
        Directory.Delete(target_root)

    def test_Path(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        self.assertEqual('/tmp/work/__TEST__', s.Path)
        Directory.Delete(target_root)

    def test_Size(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        #s = Directory(target_root)
        s = Directory(target_root)
        self.assertEqual(1024, s.Size)

        path_b = os.path.join(target_root, 'B')
        Directory.Create(path_b)
        self.__MakeDummy(os.path.join(path_b, 'b.dummy'), 1024)
        self.assertEqual(2048, s.Size)

        path_c = os.path.join(target_root, 'C')
        Directory.Create(path_c)
        self.__MakeDummy(os.path.join(path_c, 'c.dummy'), 1024)
        self.assertEqual(3072, s.Size)

        path_bb = os.path.join(target_root, 'B/BB')
        Directory.Create(path_bb)
        self.__MakeDummy(os.path.join(path_bb, 'bb.dummy'), 1024)
        self.assertEqual(4096, s.Size)

        Directory.Delete(target_root)

    def test_Mode(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        s.Mode = 0o777
        self.assertEqual(0o40777, s.Mode)
        self.assertEqual('drwxrwxrwx', s.ModeName)
        s.Mode = 0o644
        self.assertEqual(0o40644, s.Mode)
        self.assertEqual('drw-r--r--', s.ModeName)
        s.Mode = '-rwxrwxrwx'
        self.assertEqual(0o40777, s.Mode)
        self.assertEqual('drwxrwxrwx', s.ModeName)
        Directory.Delete(target_root)

    def test_Modified(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        self.assertTrue(tuple == type(s.Modified))
        self.assertTrue(2 == len(s.Modified))
        self.assertTrue(float == type(s.Modified[0]))
        self.assertTrue(datetime.datetime == type(s.Modified[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = s.Modified
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        s.Modified = dt1
        self.assertTrue(int(time.mktime(dt1.timetuple())) == s.Modified[0])
        self.assertTrue(dt1 == s.Modified[1])
        self.assertTrue(dt1 != s.Accessed[1])
        self.assertTrue(dt1 != s.Created[1])
        self.assertTrue(dt1 != s.ChangedMeta[1])
        Directory.Delete(target_root)

    def test_Accessed(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        self.assertTrue(tuple == type(s.Accessed))
        self.assertTrue(2 == len(s.Accessed))
        self.assertTrue(float == type(s.Accessed[0]))
        self.assertTrue(datetime.datetime == type(s.Accessed[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = s.Accessed
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        s.Accessed = dt1
        self.assertTrue(int(time.mktime(dt1.timetuple())) == s.Accessed[0])
        self.assertTrue(dt1 == s.Accessed[1])
        self.assertTrue(dt1 != s.Modified[1])
        self.assertTrue(dt1 != s.Created[1])
        self.assertTrue(dt1 != s.ChangedMeta[1])
        Directory.Delete(target_root)

    def test_ChangedMeta(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        s = Directory(target_root)
        self.assertTrue(hasattr(s, 'ChangedMeta'))
        self.assertTrue(hasattr(s, 'Created'))
        print(s.ChangedMeta)
        print(s.Created)
        Directory.Delete(target_root)

    def test_Ids_Property(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        s = Directory(target_root)
        self.assertTrue(hasattr(s, 'OwnUserId'))
        self.assertTrue(hasattr(s, 'OwnGroupId'))
        self.assertTrue(hasattr(s, 'HardLinkNum'))
        self.assertTrue(hasattr(s, 'INode'))
        self.assertTrue(hasattr(s, 'DeviceId'))
        print(s.OwnUserId)
        print(s.OwnGroupId)
        print(s.HardLinkNum)
        print(s.INode)
        print(s.DeviceId)
        Directory.Delete(target_root)


if __name__ == '__main__':
    unittest.main()
