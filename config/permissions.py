PERMISSIONS = {
    'commercial': ['read_employees', 'create_customers', 'read_customers', 'update_customers', 
                   'read_contracts', 'update_contracts', 'create_events', 'read_events'],
    'management': ['create_employees', 'read_employees', 'update_employees', 'delete_employees', 
                   'create_contracts', 'read_contracts', 'update_contracts', 'read_events', 'update_events'],
    'support': ['read_employees', 'read_customers', 'read_contracts', 'read_events', 'update_events']
}

def has_permission(user, permission):
    """
    Check if a user has a specific permission.

    Args:
        user (User): The user to check the permission for.
        permission (str): The permission to check.

    Returns:
        bool: True if the user has the permission, False otherwise.
    """
    return permission in PERMISSIONS.get(user.department.name, [])
