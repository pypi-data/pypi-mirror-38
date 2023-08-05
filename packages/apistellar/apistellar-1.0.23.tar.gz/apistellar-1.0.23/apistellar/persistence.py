import inspect
import asyncio

from functools import wraps
from types import FunctionType


class SelfClassProxy(object):
    """
    为cls或self设置一个代理层，用于存储store
    """
    def __init__(self, self_or_class, store):
        object.__setattr__(self, "self_or_class", self_or_class)
        object.__setattr__(self, "store", store)

    def __getattribute__(self, item):
        if item == "store":
            return super(SelfClassProxy, self).__getattribute__(item)
        else:
            return getattr(super(SelfClassProxy, self).__getattribute__(
                "self_or_class"), item)

    def __setattr__(self, key, value):
        self_or_class = super(SelfClassProxy, self).__getattribute__(
            "self_or_class")
        setattr(self_or_class, key, value)

    def __delattr__(self, item):
        self_or_class = super(SelfClassProxy, self).__getattribute__(
            "self_or_class")
        delattr(self_or_class, item)

    def __call__(self, *args, **kwargs):
        return super(SelfClassProxy, self).__getattribute__(
            "self_or_class")(*args, **kwargs)

    def __iter__(self):
        return iter(super(SelfClassProxy, self).__getattribute__("self_or_class"))

    def __getitem__(self, item):
        return super(SelfClassProxy, self).__getattribute__(
            "self_or_class").__getitem__(item)

    def __setitem__(self, key, value):
        return super(SelfClassProxy, self).__getattribute__(
            "self_or_class").__setitem__(key, value)

    def __delitem__(self, key):
        return super(SelfClassProxy, self).__getattribute__(
            "self_or_class").__delitem__(key)


def conn_manager(func):
    """
    返回连接管理下的方法
    :param func:
    :return:
    """

    if getattr(func, "conn_ignore", False):
        return func

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def inner(self_or_cls, *args, **kwargs):
            callargs = get_callargs(func, self_or_cls, *args, **kwargs)
            callargs.pop("cls", None)
            with self_or_cls.get_store(**callargs) as store:
                return await func(SelfClassProxy(self_or_cls, store), *args, **kwargs)
    else:
        @wraps(func)
        def inner(self_or_cls, *args, **kwargs):
            callargs = get_callargs(func, self_or_cls, *args, **kwargs)
            callargs.pop("cls", None)
            with self_or_cls.get_store(**callargs) as store:
                return func(SelfClassProxy(self_or_cls, store), *args, **kwargs)
    return inner


def conn_ignore(func):
    """
    使用了持久化元类时，使方法忽略使用连接管理，该装饰器必须紧靠方法
    :param func:
    :return:
    """
    func.conn_ignore = True
    return func


class DriverMixin(object):
    """
    配合conn_manager用来控制数据库访问。
    """
    store = None

    @classmethod
    def get_store(cls, **callargs):
        return NotImplemented


class PersistentMeta(type):
    """
    为实例方法和类方法增加conn_manager装饰器
    """
    def __new__(mcs, name, bases, attrs):
        for attr_name in attrs.keys():
            func = attrs[attr_name]
            # 去掉魔术方法和私有方法
            if isinstance(func, FunctionType) and not func.__name__.startswith(
                    "__"):
                attrs[attr_name] = conn_manager(func)
            if isinstance(func, classmethod):
                func = func.__func__
                if not func.__name__.startswith("__"):
                    attrs[attr_name] = classmethod(conn_manager(func))

        return super(PersistentMeta, mcs).__new__(mcs, name, bases, attrs)


def get_callargs(func, *args, **kwargs):
    """
    找到层层装饰器下最里层的函数的callargs
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    for closure in func.__closure__ or []:
        if isinstance(closure.cell_contents, FunctionType):
            func = closure.cell_contents
            return get_callargs(func, *args, **kwargs)

    else:
        return inspect.getcallargs(func, *args, **kwargs)
