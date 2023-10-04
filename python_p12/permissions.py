from typing import List, Type

import click


class Permission:
    @staticmethod
    def check(ctx) -> bool:
        raise NotImplementedError()


class IsAuthenticated(Permission):
    @staticmethod
    def check(ctx) -> bool:
        return ctx.obj.get('user') is not None


def permission(permissions: List[Type[Permission]]):
    def decorator(func):
        def wrapper(ctx, *args, **kwargs):
            for p in permissions:
                if not p.check(ctx):
                    raise click.ClickException('Unauthorized')
            return func(ctx, *args, **kwargs)
        return wrapper
    return decorator
