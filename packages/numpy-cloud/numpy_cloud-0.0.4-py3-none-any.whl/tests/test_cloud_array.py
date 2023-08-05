import threading
import unittest
import numpy as np

import proto1.client.numpy_cloud as npc

from proto1.client.cloud_array import cloudarr
from proto1.server.server import CloudArrayServer


class TestCloudArray(unittest.TestCase):

    modules = [np, npc]

    def setUp(self):
        print('setup')
        self.server = CloudArrayServer('localhost', 9090)
        self.t = threading.Thread(target=self.server.serve)
        self.t.start()

    def tearDown(self):
        print('teardown')
        self.server.force_stop()
        print('force stopped')
        self.t.join()
        print('joined')

    def assertAllSame(self, results):
        print('checking if all these are the same:', results)
        r = results[0]
        for r2 in results[1:]:
            self.assertEqual(r, r2)

    def assertAllSameArrays(self, results):
        print('checking if all these are the same array:', results)
        r = results[0]

        print('RESULTS:')
        print(results)
        for x in results:
            print('-->', x)

        print('comparing')
        for r2 in results[1:]:
            x1 = np.asarray(r)
            print('x1', x1)

            x2 = r2[:]
            # TODO!! Figure out why these two are not working as expected:
            # x2 = np.asarray(r2)
            # x2 = np.asanyarray(r2)
            print('x2', x2)

            self.assertTrue(np.array_equal(x1, x2))

    def test_mean(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.mean())
        self.assertAllSame(result)

    def test_mean_axis(self):
        result = []
        for np_module in self.modules:
            print('==== test mean axis %s ====' % np_module)
            arr = np_module.arange(15).reshape(5, 3)
            v = arr.mean(axis=1)
            print('---- got a response ----')
            result.append(v)
        self.assertAllSameArrays(result)

    def test_median(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            print('got arr, now lets call median')
            result.append(np_module.median(arr))
        self.assertAllSame(result)

    def test_min(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.min())
        self.assertAllSame(result)

    def test_max(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.max())
        self.assertAllSame(result)

    def test_arange(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(2, 15, 2, dtype=np.uint8)
            mean = arr.mean()
            result.append(mean)
        self.assertAllSame(result)

    def test_reshape(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            print('arange done')
            arr = arr.reshape(5, 3)
            print('reshape done')
            print('arr', arr)
            result.append(arr)
        self.assertAllSameArrays(result)

    def test_zeros(self):
        result = []
        for np_module in self.modules:
            arr = np_module.zeros((10, 10), dtype=np.uint8)
            mean = arr.mean()
            result.append(mean)
        self.assertAllSame(result)

    def test_ones(self):
        result = []
        for np_module in self.modules:
            arr = np_module.ones((10, 10), dtype=np.uint8)
            mean = arr.mean()
            result.append(mean)
        self.assertAllSame(result)

    def test_create_constructor(self):
        carr = cloudarr((2,3), cloud_arr_id='abc123')
        print(carr.cloud_arr_id)

    def test_to_string(self):
        result = []
        arr = npc.arange(15).reshape(3, 5)
        print(arr)
        local_arr = np.asarray(arr)
        print(local_arr)
        # self.assertAllSame(result)

    def test_asarray(self):
        result = []
        arr = npc.arange(15, dtype=np.uint8).reshape(3, 5)
        np_arr = np.arange(10)
        arr.__array_interface__ = np_arr.__array_interface__
        print(np_arr.__array_interface__)
        as_arr = np.asarray(arr)
        print(as_arr)
        return

        # buff = {'data':res.data, 'shape':(4,3), 'typestr':'<i4'}
        # arr.__array_interface__ = buff
        # # as_arr = np.asarray(arr)
        # print('--')
        # print(as_arr)
