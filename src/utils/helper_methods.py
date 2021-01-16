import logging
from functools import wraps

logger = logging.getLogger('pi.exchange.emailsender')


def log_and_call(func):

    argnames = tuple([a for a in func.__code__.co_varnames[:func.__code__.co_argcount] if a != 'self'])

    fname = func.__name__

    def inner_func(*args, **kwargs):
        args = tuple(list(args)[1:])

        log_list = [fname + ': ' + ', '.join('% s = % r' % entry for entry in zip(argnames, args[:len(argnames)]))]
        log_list.append(f'args = {list(args[len(argnames):])}')
        log_list.append(f'kwargs = {kwargs}')

        logger.info(' | '.join(log_list))

    return inner_func