"""
通过覆盖类的__new__和__init__方法提供单例支持
"""


# class Singleton:
#     """
#     单例装饰器
#     """
#     __slots__ = (
#         "__instance",
#         "__is_instance_initialized",
#         "__old_new_func",
#         "__old_init_func",
#         # "__cls__"
#     )
#
#     def __init__(self):
#         self.__instance = None
#         self.__is_instance_initialized = False
#
#     def __call__(self, cls):
#         print(cls)
#
#         # 存储原有的__new__函数与__init__函数
#         self.__old_new_func = cls.__new__
#         self.__old_init_func = cls.__init__
#
#         def new_new_func(cls1, *args, **kwargs):
#             if self.__instance is None:
#                 self.__instance = self.__old_new_func(cls1, *args, **kwargs)
#
#             return self.__instance
#
#         def new_init_func(self1, *args, **kwargs):
#             if not self.__is_instance_initialized:
#                 self.__old_init_func(self1, *args, **kwargs)
#                 self.__is_instance_initialized = True
#
#         # 替换类函数
#         cls.__new__ = new_new_func
#         cls.__init__ = new_init_func
#
#         return cls


def singleton(cls):
    """
    单例模式的装饰器
    :param cls:
    :return:
    """

    # 存储单例类的实例(实际上一个类只会有一个实例)
    _instance = []

    # 存储原来的__new__和__init__函数
    _old_new = cls.__new__
    _old_init = cls.__init__

    # 重写原来的__new__与__init__函数
    def _new_new(cls1, *args, **kwargs):
        if len(_instance) <= 0:
            _instance.append((_old_new(cls1, *args, **kwargs), False))

        inst, dummy = _instance[0]
        return inst

    def _new_init(self, *args, **kwargs):
        inst, if_inited = _instance[0]
        if if_inited:
            pass
        else:
            _old_init(self, *args, **kwargs)
            _instance[0] = self, True

    # 替换
    cls.__new__ = _new_new
    cls.__init__ = _new_init

    return cls

