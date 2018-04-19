from functools import wraps

import click
from flask_login import current_user

class HelpMessage(Exception):
	pass


class AuthenticationException(Exception):
    pass


def print_help(ctx, param, value):
	if value:
		raise HelpMessage(ctx.get_help())


def help_option(*param_decls, **attrs):
    """Taken and modified from click decorators to work with Flask"""
    def decorator(f):
        attrs.setdefault('is_flag', True)
        attrs.setdefault('expose_value', False)
        attrs.setdefault('help', 'Show this message and exit.')
        attrs.setdefault('is_eager', True)
        attrs['callback'] = print_help
        return click.decorators.option(*(param_decls or ('--help','-h')), **attrs)(f)
    return decorator


def authenticated(root=False):
    """ Boy that was fun """
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):  
            if not current_user.is_authenticated:
                raise AuthenticationException(f"Must be logged in to run command '{f.__name__}'.")

            if root and not current_user.username == 'root':
                raise AuthenticationException(f"Must be root to run command '{f.__name__}'.")
                
            return f(*args, **kwargs)
        return inner
    return decorator

