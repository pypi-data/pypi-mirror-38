import shutil
import time
import unittest
from pathlib import Path

import pkg_resources

import mp3monitoring.data.dynamic as dynamic_data
import mp3monitoring.monitor as monitor
import tests.tools as tools


class MonitorTest(unittest.TestCase):
    """
    Tests for mp3monitoring.monitor.
    """

    @classmethod
    def setUpClass(cls):
        dynamic_data.DISABLE_TQDM = True

    def setUp(self):
        self.tmp_path = Path('./tmp')
        if not self.tmp_path.exists():
            Path.mkdir(self.tmp_path)
            # self.monitor = Monitor(Path('./testdata/'), Path('./target'), False, pause=5)

    def tearDown(self):
        tools.delete_dir_rec(self.tmp_path)

    def test_init(self):
        monitor.Monitor(Path('./testdata/'), Path('./target'), False)
        monitor.Monitor(Path('./testdata/'), Path('./target'), False, pause=10)
        monitor.Monitor(Path('./testdata/'), Path('./target'), False, last_mod_time=456345)
        monitor.Monitor(Path('./testdata/'), Path('./target'), False, pause=3, last_mod_time=922)

    def test_str(self):
        with self.subTest(desc='Directories exists'):
            self.setUp()
            target_dir = Path('./tmp/target')
            Path.mkdir(target_dir)
            moni = monitor.Monitor(self.tmp_path, target_dir, False, pause=3, last_mod_time=922)
            exp_result = "False | {source_dir} | {target_dir} | 3s | Stopped | False | 922".format(
                source_dir=str(self.tmp_path.resolve()), target_dir=str(target_dir.resolve()))

            self.assertEqual(exp_result, str(moni))
            self.tearDown()

        with self.subTest(desc='Directories do not exists'):
            self.setUp()
            source_dir = Path('./nosource')
            target_dir = Path('./notarget')
            moni = monitor.Monitor(source_dir, target_dir, False, pause=3, last_mod_time=922)
            exp_result = "False | nosource | notarget | 3s | Source (nosource) does not exist. | False | 922"

            self.assertEqual(exp_result, str(moni))
            self.tearDown()

    def test_run(self):
        target_dir = Path('./tmp/target')
        Path.mkdir(target_dir)
        mp3_file = pkg_resources.resource_filename('tests', 'test.mp3')
        moni = monitor.Monitor(self.tmp_path, target_dir, False, pause=1)
        files = [self.tmp_path.joinpath(str(i)) for i in range(3)]
        for file in files:
            create_test_file(file)

        with self.subTest(desc='nothing copied'):
            moni.start()
            moni.stop()
            moni.thread.join()

            result = [x for x in target_dir.glob('*') if x.is_file()]
            self.assertEqual([], result)

        with self.subTest(desc='copy one file'):
            for file in files:
                create_test_file(file)
            shutil.copy(str(mp3_file), str(self.tmp_path.joinpath('0_mp3')))
            moni.start()
            moni.stop()
            moni.thread.join()

            result = [x for x in target_dir.glob('*') if x.is_file()]
            self.assertEqual([target_dir.joinpath('0_mp3.mp3')], result)

    def test_get_all_files_after_time(self):
        with self.subTest(desc='empty dir'):
            self.setUp()

            self.assertEqual([], monitor.get_all_files_after_time(self.tmp_path, after_time=0))
            self.tearDown()

        with self.subTest(desc='add new files'):
            self.setUp()

            for i in range(2):
                cur_time = time.time()
                time.sleep(0.01)  # add delay between cur_time and file creation
                test_file = self.tmp_path.joinpath(str(i))
                create_test_file(test_file)

                self.assertEqual([test_file], monitor.get_all_files_after_time(self.tmp_path, after_time=cur_time))
            self.tearDown()

        with self.subTest(desc='modify file'):
            self.setUp()
            create_test_file(self.tmp_path.joinpath('0'))
            test_file = self.tmp_path.joinpath('1')
            create_test_file(test_file)
            time.sleep(0.01)

            cur_time = time.time()
            time.sleep(0.01)  # add delay between cur_time and file creation
            create_test_file(test_file)

            self.assertEqual([test_file], monitor.get_all_files_after_time(self.tmp_path, after_time=cur_time))
            self.tearDown()

        with self.subTest(desc='no changes'):
            self.setUp()
            create_test_file(self.tmp_path.joinpath('0'))
            create_test_file(self.tmp_path.joinpath('1'))
            time.sleep(0.01)

            cur_time = time.time()
            files = monitor.get_all_files_after_time(self.tmp_path, after_time=cur_time)

            self.assertEqual(files, [])

            self.tearDown()

    def test_get_all_mp3(self):
        with self.subTest(desc='no mp3'):
            self.setUp()
            files = [self.tmp_path.joinpath(str(i)) for i in range(3)]
            for file in files:
                create_test_file(file)

            self.assertEqual(set(), monitor.get_all_mp3(files))
            self.tearDown()

        mp3_file = pkg_resources.resource_filename('tests', 'test.mp3')
        with self.subTest(desc='only mp3'):
            self.setUp()
            mp3_files = []
            for i in range(0, 3):
                mp3_files.append(self.tmp_path.joinpath('{id}_mp3'.format(id=i)))
                shutil.copy(str(mp3_file), str(mp3_files[i]))

            self.assertEqual(set(mp3_files), monitor.get_all_mp3(mp3_files))
            self.tearDown()

        with self.subTest(desc='mixed mp3 and non mp3'):
            self.setUp()
            files = [self.tmp_path.joinpath(str(i)) for i in range(3)]
            for file in files:
                create_test_file(file)
            mp3_files = []
            for i in range(0, 3):
                mp3_files.append(self.tmp_path.joinpath('{id}_mp3'.format(id=i)))
                shutil.copy(str(mp3_file), str(mp3_files[i]))

            self.assertEqual(set(mp3_files), monitor.get_all_mp3(files + mp3_files))
            self.tearDown()

    def test_copy_files(self):
        with self.subTest(desc='copy nothing'):
            self.setUp()
            target_dir = Path('./tmp/target')
            Path.mkdir(target_dir)
            monitor.copy_files(set(), target_dir)
            result = [x for x in target_dir.glob('*') if x.is_file()]

            self.assertEqual([], result)
            self.tearDown()

        with self.subTest(desc='no duplicates'):
            self.setUp()
            target_dir = Path('./tmp/target')
            Path.mkdir(target_dir)
            files = [self.tmp_path.joinpath(str(i)) for i in range(2)]
            for file in files:
                create_test_file(file)
            files.append(self.tmp_path.joinpath('2.mp3'))
            create_test_file(files[2])

            monitor.copy_files(files, target_dir)
            result = [x for x in target_dir.glob('*') if x.is_file()]
            result.sort()

            self.assertEqual([target_dir.joinpath('0.mp3'), target_dir.joinpath('1.mp3'), target_dir.joinpath('2.mp3')],
                             result)
            self.tearDown()

        with self.subTest(desc='with duplicates'):
            self.setUp()
            target_dir = Path('./tmp/target')
            Path.mkdir(target_dir)
            files = [self.tmp_path.joinpath(str(i)) for i in range(2)]
            for file in files:
                create_test_file(file)

            monitor.copy_files(files, target_dir)
            monitor.copy_files({files[0]}, target_dir)
            monitor.copy_files({files[0]}, target_dir)
            result = [x for x in target_dir.glob('*') if x.is_file()]
            result.sort()

            self.assertEqual(
                [target_dir.joinpath('0.mp3'), target_dir.joinpath('0_d.mp3'), target_dir.joinpath('0_d_d.mp3'),
                 target_dir.joinpath('1.mp3')], result)
            self.tearDown()


def create_test_file(file: Path):
    with open(file, 'wb') as writer:
        writer.write(str.encode('test'))
