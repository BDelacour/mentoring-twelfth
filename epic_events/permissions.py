from typing import List, Type

import click

from epic_events.models.role import Roles


class Permission:
    def check(self, ctx) -> bool:
        raise NotImplementedError()


class IsAuthenticated(Permission):
    def check(self, ctx) -> bool:
        return ctx.obj.get('user') is not None


class IsRolePerson(Permission):
    def __init__(self, role: Roles) -> None:
        self.role = role

    def check(self, ctx) -> bool:
        user = ctx.obj.get('user')
        return user.role == self.role.name


def permission(permissions: List[Permission]):
    def decorator(func):
        def wrapper(ctx, *args, **kwargs):
            for p in permissions:
                if not p.check(ctx):
                    raise click.ClickException('Unauthorized')
            return func(ctx, *args, **kwargs)

        return wrapper

    return decorator
