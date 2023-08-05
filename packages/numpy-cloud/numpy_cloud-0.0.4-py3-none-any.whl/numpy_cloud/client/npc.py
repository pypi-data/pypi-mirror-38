import pickle
import base64

from xmlrpc.client import ServerProxy

from numpy_cloud import util
from numpy_cloud.client.config import SERVER_URL
from numpy_cloud.client.cloud_array import cloudarr


def create(fn_name):
    def rpc(*args, **kwargs):

        # print('called RPC %s with args:' % fn_name)
        # print(args)
        # print(kwargs)

        args_data = {'args': args,'kwargs': kwargs}
        # print('client args_data', args_data)
        ser_args_data = util.serialize_args(args, kwargs)
        # ser_args_data = base64.b64encode(pickle.dumps(args_data))
        # print('ser_args_data', ser_args_data)
        with ServerProxy(SERVER_URL, allow_none=True) as client:
            ser_resp, is_cloud_array = client.rpc_for_module(fn_name, ser_args_data)
            resp = util.deserialize(ser_resp)
            if is_cloud_array:
                rval = cloudarr((1,), cloud_arr_id=resp)
            else:
                rval = resp
            return rval

            # print('got cloud_arr_id', cloud_arr_id)
            # ser_resp, is_cloud_array = cloudarr((1,), cloud_arr_id=cloud_arr_id)
            # return arr
    return rpc


exec('%s = create("%s")' % ('arange', 'arange'))
exec('%s = create("%s")' % ('zeros', 'zeros'))
exec('%s = create("%s")' % ('ones', 'ones'))
exec('%s = create("%s")' % ('median', 'median'))
exec('%s = create("%s")' % ('isfinite', 'isfinite'))
