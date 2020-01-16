from tapis_cli.utils import seconds

__all__ = ['list, ' 'grant', 'revoke', 'drop']


def list(actor_id, permissive=False, agave=None, **kwargs):
    """Helper to list permissions
    """
    try:
        results = agave.actors.listPermissions(actorId=actor_id)
        return results
    except Exception:
        if permissive:
            return {}
        else:
            raise


def grant(actor_id,
          username,
          permission,
          permissive=False,
          agave=None,
          **kwargs):
    """Helper to grant permission on an Actor
    """
    body = {'username': username, 'permission': permission.upper()}
    try:
        grant_result = agave.actors.updateApplicationPermissions(actorId=actor_id,
                                                               body=body)
        return grant_result
    except Exception:
        if permissive:
            return {}
        else:
            raise


def revoke(actor_id, username, permissive=False, agave=None, **kwargs):
    pass


def drop(actor_id, permissive=False, agave=None, **kwargs):
    pass
