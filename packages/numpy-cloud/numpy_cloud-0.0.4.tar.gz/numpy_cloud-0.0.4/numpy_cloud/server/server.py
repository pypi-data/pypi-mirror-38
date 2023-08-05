import base64
import pickle
import numpy as np
import uuid
import sys

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy

from numpy_cloud import util


class CloudArrayServer(object):

    def __init__(self, host, port):
        # self.spec = ("localhost", 9090)
        self.spec = (host, port)
        self.server = SimpleXMLRPCServer(self.spec)
        self.server.register_function(self.stop, 'stop')
        self.server.register_function(self.save_as, 'save_as')
        self.server.register_function(self.rpc_for_module, 'rpc_for_module')
        self.server.register_function(self.rpc_for_arrays, 'rpc_for_arrays') 

        self.stopped = False
        self.arrays = {}

    def serve(self):
        print('serving on:', self.spec)
        while not self.stopped:
            self.server.handle_request()
        self.server.server_close()
        

    def force_stop(self):
        url = 'http://%s:%s' % self.spec
        with ServerProxy(url) as client:
            client.stop()

    def stop(self):
        self.stopped = True
        return 'ok'

    def debug_print(self):
        print('')
        print('---- debug: my arrays ----')
        for key, arr in self.arrays.items():
            print('-', key)
            print(arr)
            print('')
        print('-' * 40)
        print('')

    def random_id(self):
        return 's-' + str(uuid.uuid4())

    def create_cloud_array(self, arr):
        cloud_arr_id = self.random_id()
        self.arrays[cloud_arr_id] = arr
        return cloud_arr_id

    def pack_response(self, rval, bring_local):
        # print('isinstance(rval, np.ndarray)?', isinstance(rval, np.ndarray))
        if isinstance(rval, np.ndarray) and not bring_local:
            rval = self.create_cloud_array(rval)
            is_cloud_array = True
        else:
            is_cloud_array = False

        ser_resp = util.serialize(rval)
        return (ser_resp, is_cloud_array)

    def save_as(self, old_id, new_id):
        arr = self.arrays[old_id]
        self.arrays[new_id] = arr
        del self.arrays[old_id]
        return 'ok'

    def rpc_for_module(self, name, ser_args_data=None):
        # print('name', name)
        # print('server ser_args_data', ser_args_data)
        if ser_args_data:
            args, kwargs = util.deserialize_args(ser_args_data, self.arrays)
        else:
            args = []
            kwargs = {}
        # print('server args_data', args_data)
        # args = args_data.get('args', [])
        # kwargs = args_data.get('kwargs', {})
        # print('args', args)
        # print('kwargs', kwargs)
        cloud_arr_id = self.random_id()
        # print('rpc for module: %s, %s' % (cloud_arr_id, name))
        rval = getattr(np, name)(*args, **kwargs)
        # print('server side rval:', rval)
        return self.pack_response(rval, False)

    def rpc_for_arrays(self, cloud_arr_id, name, access_as, bring_local, ser_args_data=None):
        if ser_args_data:
            args_data = pickle.loads(base64.b64decode(str(ser_args_data)))
        else:
            args_data = {}
        print('SERVER: rpc for array: %s, %s' % (cloud_arr_id, name))
        # print('args data:', args_data)
        # self.debug_print()
        arr = self.arrays[cloud_arr_id]
        # print('execute the ' + name + ' function on this array:', arr)
        attr = getattr(arr, name)
        if access_as == 'attr':
            rval = attr
        elif access_as == 'method':
            args = args_data.get('args', [])
            kwargs = args_data.get('kwargs', {})
            # print('executing %s with %s %s' % (attr, args, kwargs))
            rval = attr(*args, **kwargs)

        # print('packing response', rval, bring_local)
        rval = self.pack_response(rval, bring_local)
        # print('rval', rval)
        return rval


if __name__ == '__main__':
    host = 'localhost'
    port = 9090

    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    server = CloudArrayServer(host, port)
    server.serve()
