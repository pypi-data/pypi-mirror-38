import base64
import pickle
import uuid

import numpy as np

from xmlrpc.client import ServerProxy

from .config import SERVER_URL


class cloudarr(np.ndarray):

    def __new__(cls, *args, **kwargs):
        # TODO: This should be an RPC call
        cloud_arr_id = kwargs.get('cloud_arr_id')
        if 'cloud_arr_id' in kwargs:
            del kwargs['cloud_arr_id']
        obj = np.ndarray.__new__(cls, *args, **kwargs)
        obj.cloud_arr_id = cloud_arr_id

        return obj

    def __str__(self):
        return '<cloud array %s>' % self.cloud_arr_id

    def __array__(self, *args, **kwargs):
        raise Exception('xyz')

    def __array_finalize__(self, obj):
        if obj is None:
            return

        try:
            obj.cloud_arr_id
        except AttributeError:
            obj.cloud_arr_id = None
        if obj.cloud_arr_id is None:
            obj.cloud_arr_id = self.random_id()

    def random_id(self):
        return 'c-' + str(uuid.uuid4())

    def save_as(self, cloud_arr_id):
        old_id = self.cloud_arr_id
        new_id = cloud_arr_id
        with ServerProxy(SERVER_URL, allow_none=True) as proxy:
            resp = proxy.save_as(old_id, new_id)
        self.cloud_arr_id = new_id

    @staticmethod
    def load(cloud_arr_id):
        return cloudarr((1,), cloud_arr_id=cloud_arr_id)

    def create_rpc_fn(self, name, access_as, bring_local=False):
        def transient_fn(*args, **kwargs):
            with ServerProxy(SERVER_URL, allow_none=True) as proxy:
                args_data = {'args': args, 'kwargs': kwargs}
                ser_args_data = base64.b64encode(pickle.dumps(args_data))
                # print('client is making RPC')
                resp, is_cloud_array = proxy.rpc_for_arrays(
                    self.cloud_arr_id, name, access_as, bring_local, ser_args_data)
                rval = pickle.loads(base64.b64decode(str(resp)))
                # print('server gave response:', rval, is_cloud_array)
                if is_cloud_array:
                    rval = cloudarr((1,), cloud_arr_id=rval)
                return rval
        return transient_fn

    def __getitem__(self, what):
        fn = self.create_rpc_fn('__getitem__', 'method')
        return fn(what)

    def __setattribute__(self, *args, **kwargs):
        raise Exception('__setattribute__')

    def __getattribute__(self, name):
        if name in ['mean', 'min', 'max', 'reshape', 'item']:
            return self.create_rpc_fn(name, 'method')
        elif name in ['shape', 'size', 'dtype', 'ndim']:
            return self.create_rpc_fn(name, 'attr')()
        elif name in ['__array_finalize__', 'create_rpc_fn', 'cloud_arr_id', 'ndim', 'save_as', 'load']:
            return super().__getattribute__(name)
        else:
            raise Exception('do you really want to make a local access for %s?' % name)
