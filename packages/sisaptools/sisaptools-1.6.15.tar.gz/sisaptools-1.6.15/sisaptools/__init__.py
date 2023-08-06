# -*- coding: utf8 -*-

"""
Utilitats compartides pels diferents processos.
Quan s'importa per primera vegada executa les següents accions:
    copyreg per permetre multiprocessing amb mètodes de classes
    elimina els warnings del client de MariaDB
"""

import copyreg
import types
import multiprocessing
import multiprocessing.pool
import os
import MySQLdb
import warnings

from .constants import IS_PYTHON_3
from .database import Database
from .mail import Mail
from .redis import Redis
from .ssh import SSH, SFTP
from .textfile import TextFile


if IS_PYTHON_3:
    """
    Modificació de Pool per utilitzar processos non-daemonic
    i així poder tenir fills.
    https://stackoverflow.com/questions/6974695/python-process-pool-non-daemonic
    """
    class NoDaemonProcess(multiprocessing.Process):

        @property
        def daemon(self):
            return False

        @daemon.setter
        def daemon(self, value):
            pass

    class NoDaemonContext(type(multiprocessing.get_context())):

        Process = NoDaemonProcess

    class NoDaemonPool(multiprocessing.pool.Pool):

        def __init__(self, *args, **kwargs):
            kwargs['context'] = NoDaemonContext()
            super(NoDaemonPool, self).__init__(*args, **kwargs)
else:
    class NoDaemonProcess(multiprocessing.Process):

        def _get_daemon(self):
            return False

        def _set_daemon(self, value):
            pass

        daemon = property(_get_daemon, _set_daemon)

    class NoDaemonPool(multiprocessing.pool.Pool):

        Process = NoDaemonProcess


def years_between(inici, final):
    """Calcula els anys entre dues dates."""
    residu = (final.month, final.day) < (inici.month, inici.day)
    return final.year - inici.year - residu


def _pickle_method(method):
    """copyreg."""
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)


def _unpickle_method(func_name, obj, cls):
    """copyreg."""
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)


copyreg.pickle(types.MethodType, _pickle_method, _unpickle_method)
warnings.filterwarnings('ignore', category=MySQLdb.Warning)
