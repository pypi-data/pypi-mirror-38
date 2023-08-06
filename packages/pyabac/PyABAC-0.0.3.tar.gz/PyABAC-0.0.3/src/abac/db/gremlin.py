"""
The home of the Gremlin implementation of PyABAC.
"""
from . import BaseDBProvider

# import gremlin_python
from gremlin_python.process.graph_traversal import __

# from gremlin_python.process.traversal import P, T, Operator, Direction


class GremlinDBProvider(BaseDBProvider):
    """Main Gremlin provider class.

    Attributes:
        g (gremlin_python.process.graph_traversal.GraphTraversalSource):
            Graph traversal source
    """

    def __init__(self, g):
        self.g = g

    def user_has_permission(self, user_id, permission_id):
        """
        Checks if :code:`user` has :code:`permission`.

        This thing is untested. It *should* work.
        I don't trust it. You shouldn't either. Run while you still can.

        Args:
            user (int): The user to check for the permission. Vertex ID.
            permission (str): Permission to check for
        
        Returns:
            bool: Whether or not the user has the permission
        """
        return permission_id in (
            self.g.V(user_id)
            .repeat(__.out("hasRole"), __.out("hasPermission"))
            .until(
                __.and_(
                    __.outE("hasRole").count().is_(0),
                    __.outE("hasPermission").count().is_(0),
                )
            )
            .path()
            .unfold()
            .dedup()
            .hasLabel("permission")
            .values("name")
        )

    def user_has_role(self, user_id, role_id):
        pass
