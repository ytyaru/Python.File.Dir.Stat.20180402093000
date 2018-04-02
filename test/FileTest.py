import sys, os, os.path, pathlib
print(pathlib.Path(__file__).parent.parent / 'src')
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from File import File
from Directory import Directory
import unittest
import time, datetime

class FileTest(unittest.TestCase):
    # ----------------------------
    # クラスメソッド
    # ----------------------------
    def test_IsExist(self):
        self.assertTrue(File.IsExist(__file__))
        # 存在するがファイルでないためFalse
        self.assertTrue(not File.IsExist(os.path.dirname(__file__)))
        self.assertTrue(not File.IsExist('/NotExistDir.txt'))
    
    def test_Create_Delete(self):
        target = '/tmp/work/__TEST__/a.txt'
        self.assertTrue(not File.IsExist(target))
        File.Create(target)
        self.assertTrue(File.IsExist(target))
        self.assertTrue(0 == File.GetSize(target))
        File.Delete(target)
        self.assertTrue(not File.IsExist(target))
        target = '/tmp/work/__TEST__/A/B/C/d.e'
        self.assertTrue(not File.IsExist(target))
        File.Create(target)
        self.assertTrue(File.IsExist(target))
        File.Delete(target)
        self.assertTrue(not File.IsExist(target))
        target = '/tmp/work/__TEST__'
        Directory.Delete(target)
 
    def test_CreateDummy(self):
        target = '/tmp/work/__TEST__/a.txt'
        self.assertTrue(not File.IsExist(target))
        File.CreateDummy(target, 1024)
        self.assertTrue(File.IsExist(target))
        self.assertTrue(1024 == File.GetSize(target))
        File.Delete(target)
        self.assertTrue(not File.IsExist(target))
        target = '/tmp/work/__TEST__/A/B/C/d.e'
        self.assertTrue(not File.IsExist(target))
        File.CreateDummy(target, 4096)
        self.assertTrue(File.IsExist(target))
        self.assertTrue(4096 == File.GetSize(target))
        File.Delete(target)
        self.assertTrue(not File.IsExist(target))
        target = '/tmp/work/__TEST__'
        Directory.Delete(target)

    def test_Copy(self):
        target = '/tmp/work/__TEST__/a.txt'
        self.assertTrue(not File.IsExist(target))
        File.CreateDummy(target, 1024)
        File.Copy(target, '/tmp/work/__TEST__/b.txt')
        self.assertTrue(File.IsExist('/tmp/work/__TEST__/b.txt'))
        self.assertTrue(1024 == File.GetSize('/tmp/work/__TEST__/a.txt'))
        self.assertTrue(1024 == File.GetSize('/tmp/work/__TEST__/b.txt'))

        self.assertTrue(not os.path.exists('/tmp/work/__TEST_2__'))
        File.Copy('/tmp/work/__TEST__', '/tmp/work/__TEST_2__')
        self.assertTrue(not os.path.exists('/tmp/work/__TEST_2__'))
        File.Copy('/tmp/work/__TEST__', '/tmp/work/__TEST_2__/c.txt')
        self.assertTrue(not os.path.exists('/tmp/work/__TEST_2__/c.txt'))
        File.Copy('/tmp/work/__TEST__/a.txt', '/tmp/work/__TEST_2__')
        self.assertTrue(os.path.exists('/tmp/work/__TEST_2__'))
        self.assertTrue(1024 == File.GetSize('/tmp/work/__TEST_2__'))
        
        File.Delete('/tmp/work/__TEST__/a.txt')
        File.Delete('/tmp/work/__TEST__/b.txt')
        File.Delete('/tmp/work/__TEST_2__')
        Directory.Delete('/tmp/work/__TEST__')
    
    def test_Move_single(self):
        target = '/tmp/work/__TEST__/a.txt'
        self.assertTrue(not File.IsExist(target))
        self.assertTrue(not File.IsExist('/tmp/work/__TEST_2__'))
        File.Create(target)
        File.Move(target, '/tmp/work/__TEST_2__/b.txt')
        self.assertTrue(not File.IsExist(target))
        self.assertTrue(File.IsExist('/tmp/work/__TEST_2__/b.txt'))
        Directory.Delete('/tmp/work/__TEST_2__')
        Directory.Delete('/tmp/work/__TEST__')

    def test_Archive(self):
        self.__make_archive()
        os.remove('/tmp/work/__TEST__/A/a.txt' + '.zip')
        Directory.Delete('/tmp/work/__TEST__')

    def __make_archive(self):
        target = '/tmp/work/__TEST__/A/a.txt'
        self.assertTrue(not File.IsExist(target))
        File.Create(target)
        
        File.Archive(target, target + '.zip')
        self.assertTrue(os.path.isfile(target + '.zip'))
    
    def test_UnArchive(self):
        self.__make_archive()
        self.assertTrue(not File.IsExist('/tmp/work/__TEST__'))
        File.Delete('/tmp/work/__TEST__/A/a.txt')
        self.assertTrue(not File.IsExist('/tmp/work/__TEST__/A/a.txt'))
        File.UnArchive('/tmp/work/__TEST__/A/a.txt.zip')
        self.assertTrue(File.IsExist('/tmp/work/__TEST__/A/a.txt'))
        Directory.Delete('/tmp/work/__TEST__')

    """
    """
    """
    # ----------------------------
    # インスタンスメソッド
    # ----------------------------
    def test_init_relative_error(self):
        with self.assertRaises(ValueError) as e:
            d = File('A')
        self.assertEqual('引数pathは絶対パスにしてください。path=\'{}\''.format('A'), e.exception.args[0])

    def test_mk_rm(self):
        target_root = '/tmp/work/__TEST__'
        d = File(target_root)
        self.assertTrue(not File.IsExist(target_root))
        self.assertTrue(d.Stat is None)
        d.mk()
        self.assertEqual(target_root, d.Path)
        self.assertTrue(d.Stat is not None)
        self.assertTrue(File.IsExist(target_root))
        self.assertTrue(not File.IsExist(os.path.join(target_root, 'A')))
        d.mk('A')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(File.IsExist(os.path.join(target_root, 'A')))
        self.assertTrue(not File.IsExist(os.path.join(target_root, 'B/BB/BBB')))
        d.mk('B/BB/BBB')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(File.IsExist(os.path.join(target_root, 'B/BB/BBB')))
        self.assertTrue(not File.IsExist(os.path.join('/tmp/work/__TEST__/C')))
        d.mk('/tmp/work/__TEST__/C')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(File.IsExist(os.path.join('/tmp/work/__TEST__/C')))

        d.rm('B/BB/BBB')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not File.IsExist(os.path.join(target_root, 'B/BB/BBB')))
        self.assertTrue(File.IsExist(os.path.join(target_root, 'B/BB')))
        d.rm('/tmp/work/__TEST__/B/BB')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not File.IsExist(os.path.join('/tmp/work/__TEST__/B/BB')))
        d.rm(target_root)
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not File.IsExist(target_root))
    
    def test_mk_rm_raise(self):
        target_root = '/tmp/work/__TEST__'
        d = File(target_root)
        d = File(target_root)
        self.assertTrue(not File.IsExist(target_root))
        with self.assertRaises(ValueError) as e:
            d.mk('/tmp/work/A')
        self.assertEqual('引数pathは未指定か次のパスの相対パス、または次のパス配下を指定してください。{}'.format(target_root), e.exception.args[0])
        with self.assertRaises(ValueError) as e:
            d.rm('/tmp/work/A')
        self.assertEqual('引数pathは未指定か次のパスの相対パス、または次のパス配下を指定してください。{}'.format(target_root), e.exception.args[0])

    def test_cp_single(self):
        target_root = '/tmp/work/__TEST__'
        d = File(target_root)
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not File.IsExist(target_root))
        d.mk()
        self.assertEqual(target_root, d.Path)
        self.assertTrue(File.IsExist(target_root))
        self.assertTrue(not File.IsExist('/tmp/work/__TEST_2__'))
        res = d.cp('/tmp/work/__TEST_2__')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(File.IsExist('/tmp/work/__TEST_2__'))
        self.assertEqual('/tmp/work/__TEST_2__', res)
        self.assertEqual('/tmp/work/__TEST__', d.Path)
        d.rm()
        self.assertEqual(target_root, d.Path)
        File.Delete('/tmp/work/__TEST__')
        File.Delete('/tmp/work/__TEST_2__')
        self.assertTrue(not File.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(not File.IsExist('/tmp/work/__TEST__'))

    def test_cp_tree(self):
        target_root = '/tmp/work/__TEST__'
        d = File(target_root)
        self.assertEqual(target_root, d.Path)
        self.assertTrue(not File.IsExist(d.Path))
        with self.assertRaises(FileNotFoundError) as e:
            d.cp('/tmp/work/__TEST_2__')
        d.mk()
        self.assertEqual(target_root, d.Path)
        self.assertTrue(File.IsExist(d.Path))
        d.mk('A')
        self.assertEqual(target_root, d.Path)
        pathlib.Path(os.path.join(target_root, 'A/a.txt')).touch()
        self.assertTrue(not File.IsExist('/tmp/work/__TEST_2__'))
        d.cp('/tmp/work/__TEST_2__')
        self.assertEqual(target_root, d.Path)
        self.assertTrue(File.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST_2__/A/a.txt'))
        d.rm()
        self.assertEqual(target_root, d.Path)
        File.Delete('/tmp/work/__TEST_2__')
        self.assertTrue(not File.IsExist('/tmp/work/__TEST__'))
        self.assertTrue(not File.IsExist('/tmp/work/__TEST_2__'))
    
    def test_mv_single(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not File.IsExist(target))
        self.assertTrue(not File.IsExist('/tmp/work/__TEST_2__'))

        d = File(target)
        self.assertEqual(target, d.Path)
        with self.assertRaises(FileNotFoundError) as e:
            d.mv('/tmp/work/__TEST_2__')

        d.mk()
        self.assertEqual(target, d.Path)
        self.assertTrue(File.IsExist(target))
        self.assertTrue(not File.IsExist('/tmp/work/__TEST_2__'))

        d.mv('/tmp/work/__TEST_2__')
        self.assertEqual('/tmp/work/__TEST_2__', d.Path)
        self.assertTrue(not File.IsExist(target))
        self.assertTrue(File.IsExist('/tmp/work/__TEST_2__'))
        File.Delete('/tmp/work/__TEST_2__')
        File.Delete('/tmp/work/__TEST__')

    def test_mv_tree(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not File.IsExist(target))
        self.assertTrue(not File.IsExist('/tmp/work/__TEST_2__'))

        d = File(target)
        self.assertEqual(target, d.Path)
        with self.assertRaises(FileNotFoundError) as e:
            d.mv('/tmp/work/__TEST_2__')

        #d.mk()
        d.mk('A')
        self.assertEqual(target, d.Path)
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        self.assertTrue(File.IsExist('/tmp/work/__TEST__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST__/A/a.txt'))

        d.mv('/tmp/work/__TEST_2__')
        self.assertEqual('/tmp/work/__TEST_2__', d.Path)
        self.assertTrue(not File.IsExist(target))
        self.assertTrue(File.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(File.IsExist('/tmp/work/__TEST_2__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST_2__/A/a.txt'))
        File.Delete('/tmp/work/__TEST_2__')
        File.Delete('/tmp/work/__TEST__')
    
    def test_pack(self):
         self.__make_pack()
         os.remove('/tmp/work/__TEST__' + '.zip')

    def __make_pack(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not File.IsExist(target))

        d = File(target)
        d.mk('A')
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        
        self.assertTrue(not os.path.isfile(target + '.zip'))
        d.pack(target + '.zip')
        self.assertTrue(os.path.isfile(target + '.zip'))
        self.assertEqual(target, d.Path)

        d.rm()
        self.assertTrue(not File.IsExist(target))
        File.Delete(target)
        return d

    def test_unpack(self):
        d = self.__make_pack()
        self.assertTrue(not File.IsExist('/tmp/work/__TEST__'))

        d.unpack('/tmp/work/__TEST__.zip', os.path.dirname(d.Path))
        self.assertTrue(File.IsExist('/tmp/work/__TEST__'))
        self.assertTrue(File.IsExist('/tmp/work/__TEST__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST__/A/a.txt'))
        d.rm()
        
        d.unpack('/tmp/work/__TEST__.zip')
        self.assertTrue(File.IsExist('/tmp/work/__TEST__'))
        self.assertTrue(File.IsExist('/tmp/work/__TEST__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST__/A/a.txt'))
        d.rm()

        d.unpack('/tmp/work/__TEST__.zip', d.Path)
        self.assertTrue(File.IsExist('/tmp/work/__TEST__/__TEST__'))
        self.assertTrue(File.IsExist('/tmp/work/__TEST__/__TEST__/A'))
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
        self.assertTrue(hasattr(File, 'GetSize'))
        print('Dir Size is {}'.format(File.GetSize(target_root)))
        self.assertEqual(1024, File.GetSize(target_root))

        path_b = os.path.join(target_root, 'B')
        File.Create(path_b)
        self.__MakeDummy(os.path.join(path_b, 'b.dummy'), 1024)
        self.assertEqual(2048, File.GetSize(target_root))

        path_c = os.path.join(target_root, 'C')
        File.Create(path_c)
        self.__MakeDummy(os.path.join(path_c, 'c.dummy'), 1024)
        self.assertEqual(3072, File.GetSize(target_root))

        path_bb = os.path.join(target_root, 'B/BB')
        File.Create(path_bb)
        self.__MakeDummy(os.path.join(path_bb, 'bb.dummy'), 1024)
        self.assertEqual(4096, File.GetSize(target_root))

        File.Delete(target_root)
    
    def test_DiskUsage(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(File, 'DiskUsage'))
        res = File.DiskUsage(target_dummy)
        self.assertTrue(hasattr(res, 'total'))
        self.assertTrue(hasattr(res, 'used'))
        self.assertTrue(hasattr(res, 'free'))
        print(File.DiskUsage(target_dummy))
        File.Delete(target_root)

    def test_Mode_Get_Set_Name(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        mode = File.GetMode(target_dummy)
        print(mode)
        print(oct(mode))
        File.SetMode(target_dummy, 0o755)
        self.assertEqual(0o100755, File.GetMode(target_dummy))
        self.assertEqual('-rwxr-xr-x', File.GetModeName(target_dummy))
        File.SetMode(target_dummy, '-rwxrwxrwx')
        self.assertEqual(0o100777, File.GetMode(target_dummy))
        File.SetMode(target_dummy, 0o644)
        self.assertEqual(0o100644, File.GetMode(target_dummy))
        self.assertEqual('-rw-r--r--', File.GetModeName(target_dummy))
        File.Delete(target_root)
    
    def test_SetModeFromName_Error(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        mode_name = 'Invalid-Text'
        with self.assertRaises(ValueError) as e:
            File.SetMode(target_dummy, mode_name )
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
        File.Delete(target_root)

    def test_Modified_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(File.GetModified(target_dummy)))
        self.assertTrue(2 == len(File.GetModified(target_dummy)))
        self.assertTrue(float == type(File.GetModified(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(File.GetModified(target_dummy)[1]))
        #print(type(File.GetModified(target_dummy)[0]))
        #print(type(File.GetModified(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = File.GetModified(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        File.SetModified(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == File.GetModified(target_dummy)[0])
        self.assertTrue(dt1 == File.GetModified(target_dummy)[1])
        self.assertTrue(dt1 != File.GetChangedMeta(target_dummy)[1])
        self.assertTrue(dt1 != File.GetAccessed(target_dummy)[1])
        File.Delete(target_root)

    def test_Accessed_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(File.GetAccessed(target_dummy)))
        self.assertTrue(2 == len(File.GetAccessed(target_dummy)))
        self.assertTrue(float == type(File.GetAccessed(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(File.GetAccessed(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = File.GetAccessed(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        File.SetAccessed(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == File.GetAccessed(target_dummy)[0])
        self.assertTrue(dt1 == File.GetAccessed(target_dummy)[1])
        self.assertTrue(dt1 != File.GetModified(target_dummy)[1])
        self.assertTrue(dt1 != File.GetChangedMeta(target_dummy)[1])
        File.Delete(target_root)

    def test_GetChangedMeta(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(File, 'GetChangedMeta'))
        self.assertTrue(hasattr(File, 'GetCreated'))
        print(File.GetChangedMeta(target_dummy))
        print(File.GetCreated(target_dummy))
        File.Delete(target_root)

    def test_Ids(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(File, 'OwnUserId'))
        self.assertTrue(hasattr(File, 'OwnGroupId'))
        self.assertTrue(hasattr(File, 'HardLinkNum'))
        self.assertTrue(hasattr(File, 'INode'))
        self.assertTrue(hasattr(File, 'DeviceId'))
        print(File.GetOwnUserId(target_dummy))
        print(File.GetOwnGroupId(target_dummy))
        print(File.GetHardLinkNum(target_dummy))
        print(File.GetINode(target_dummy))
        print(File.GetDeviceId(target_dummy))
        File.Delete(target_root)

    # ----------------------------
    # インスタンスメソッド
    # ----------------------------
    def test_Stat(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = File(target_root)
        self.assertEqual(File, type(s))
        self.assertEqual(os.stat_result, type(s.Stat))
        File.Delete(target_root)

    def test_Path(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = File(target_root)
        self.assertEqual('/tmp/work/__TEST__', s.Path)
        File.Delete(target_root)

    def test_Size(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        #s = File(target_root)
        s = File(target_root)
        self.assertEqual(1024, s.Size)

        path_b = os.path.join(target_root, 'B')
        File.Create(path_b)
        self.__MakeDummy(os.path.join(path_b, 'b.dummy'), 1024)
        self.assertEqual(2048, s.Size)

        path_c = os.path.join(target_root, 'C')
        File.Create(path_c)
        self.__MakeDummy(os.path.join(path_c, 'c.dummy'), 1024)
        self.assertEqual(3072, s.Size)

        path_bb = os.path.join(target_root, 'B/BB')
        File.Create(path_bb)
        self.__MakeDummy(os.path.join(path_bb, 'bb.dummy'), 1024)
        self.assertEqual(4096, s.Size)

        File.Delete(target_root)

    def test_Mode(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = File(target_root)
        s.Mode = 0o777
        self.assertEqual(0o40777, s.Mode)
        self.assertEqual('drwxrwxrwx', s.ModeName)
        s.Mode = 0o644
        self.assertEqual(0o40644, s.Mode)
        self.assertEqual('drw-r--r--', s.ModeName)
        s.Mode = '-rwxrwxrwx'
        self.assertEqual(0o40777, s.Mode)
        self.assertEqual('drwxrwxrwx', s.ModeName)
        File.Delete(target_root)

    def test_Modified(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = File(target_root)
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
        File.Delete(target_root)

    def test_Accessed(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = File(target_root)
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
        File.Delete(target_root)

    def test_ChangedMeta(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        s = File(target_root)
        self.assertTrue(hasattr(s, 'ChangedMeta'))
        self.assertTrue(hasattr(s, 'Created'))
        print(s.ChangedMeta)
        print(s.Created)
        File.Delete(target_root)

    def test_Ids_Property(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        s = File(target_root)
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
        File.Delete(target_root)
    """

if __name__ == '__main__':
    unittest.main()
