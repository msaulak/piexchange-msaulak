import logging
import os

logger = logging.getLogger('pi.exchange.emailsender')


def log_and_call(func):
    argnames = tuple([a for a in func.__code__.co_varnames[:func.__code__.co_argcount] if a != 'self'])

    fname = func.__name__

    def inner_func(*args, **kwargs):
        args = tuple(list(args))

        log_list = [fname + ': ' + ', '.join('% s = % r' % entry for entry in zip(argnames, args[:len(argnames)])),
                    f'args = {list(args[len(argnames):])}', f'kwargs = {kwargs}']

        logger.info(' | '.join(log_list))

        return func(*args, **kwargs)

    return inner_func


def object_to_str(o: object) -> str:
    """Convert an object to a printable string
    Args:
        o: object

    Returns:
        str: string representation of the object
    """
    ret_str_list = []
    for k, v in vars(o).items():
        if not k.startswith('_') and k != 'method_calls':
            ret_str_list.append(f'{k} : {v}')

    return ' | '.join(ret_str_list)


def get_parent_dir(starting_location: str, levels_up: int = 1) -> str:
    """Returns path of parent directory from the starting location. Default return value
    is the immediate parent. User can pass in how many levels up they want to ho.
    Args:
        starting_location (str): Path from where to start
        levels_up (int): how many levels to go up.

    Returns:
        str: path to the parent.
    """
    if levels_up == 0:
        return starting_location

    return get_parent_dir(os.path.dirname(starting_location), levels_up - 1)
