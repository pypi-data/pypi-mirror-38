import base64
import pickle

from numpy_cloud.client.cloud_array import cloudarr


class CloudArrayProxy(object):
    def __init__(self, cloud_arr_id):
        self.cloud_arr_id = cloud_arr_id


def serialize(value):
    return base64.b64encode(pickle.dumps(value))


def deserialize(ser):
    return pickle.loads(base64.b64decode(str(ser)))


def serialize_args(args, kwargs):
    args_cp = []
    if args:
        for arg in args:
            if isinstance(arg, cloudarr):
                args_cp.append(CloudArrayProxy(arg.cloud_arr_id))
            else:
                args_cp.append(arg)
    kwargs_cp = {}
    if kwargs:
        for key, val in kwargs.items():
            if isinstance(arg, cloudarr):
                kwargs_cp[key] = CloudArrayProxy(val.cloud_arr_id)
            else:
                kwargs_cp[key] = val
    args_data = {
        'args': args_cp,
        'kwargs': kwargs_cp,
    }
    return base64.b64encode(pickle.dumps(args_data))


def deserialize_args(ser_args_data, cloud_array_dict):
    print('util deserialize_args', ser_args_data)
    args_data = pickle.loads(base64.b64decode(str(ser_args_data)))
    args = []
    for arg in args_data.get('args', []):
        if isinstance(arg, CloudArrayProxy):
            args.append(cloud_array_dict[arg.cloud_arr_id])
        else:
            args.append(arg)
    kwargs = {}
    for key, val in args_data.get('kwargs', {}).items():
        if isinstance(val, CloudArrayProxy):
            kwargs[key] = cloud_array_dict[val.cloud_arr_id]
        else:
            kwargs[key] = val
    return args, kwargs
