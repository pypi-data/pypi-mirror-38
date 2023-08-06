from abc import ABC, abstractmethod


class BaseDBProvider(ABC):
    """
    ABC specifying the API for DB providers.

    Extensible by other external providers.
    """

    @abstractmethod
    def user_has_permission(self, user_id, permission_id):
        """
        Checks if :code:`user` has :code:`permission`.

        Args:
            user_id: User ID to check
            permission_id (str): Permission to check for

        Returns:
            bool: Whether or not the user has the permission
        """
        pass

    @abstractmethod
    def user_has_role(self, user_id, role_id):
        pass

    @abstractmethod
    def create_user(self, user_id):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def add_role(self, role_id):
        pass

    @abstractmethod
    def delete_role(self, role_id):
        pass

    @abstractmethod
    def add_permission(self, permission_id):
        pass

    @abstractmethod
    def delete_permission(self, permission_id):
        pass

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def get_permissions(self):
        pass

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def role_add_permission(self, role_id, permission_id):
        pass

    @abstractmethod
    def role_delete_permission(self, role_id, permission_id):
        pass

    @abstractmethod
    def role_add_role(self, role_id1, role_id2):
        pass
    
    @abstractmethod
    def role_delete_role(self, role_id1, role_id2):
        pass

    @abstractmethod
    def user_add_role(self, user_id, role_id):
        pass

    @abstractmethod
    def user_delete_role(self, user_id, role_id):
        pass

    @abstractmethod
    def user_add_permission(self, user_id, permission_id):
        pass

    @abstractmethod
    def user_delete_permission(self, user_id, permission_id):
        pass

    @abstractmethod
    def permission_add_permission(self, permission_id1, permission_id2):
        pass
    
    @abstractmethod
    def permission_delete_permission(self, permission_id1, permission_id2):
        pass

    @abstractmethod
    def role_get_permissions(self, role_id):
        pass

    @abstractmethod
    def role_get_users(self, role_id):
        pass

    @abstractmethod
    def role_get_roles(self, role_id):
        pass

    @abstractmethod
    def permission_get_users(self, permission_id):
        pass

    @abstractmethod
    def permission_get_permissions(self, permission_id):
        pass

    @abstractmethod
    def permission_get_roles(self, permission_id):
        pass

    @abstractmethod
    def user_get_roles(self, user_id):
        pass

    @abstractmethod
    def user_get_permissions(self, user_id):
        pass
