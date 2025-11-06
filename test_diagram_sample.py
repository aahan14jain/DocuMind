class User:
    """Represents a user in the system."""
    
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def get_name(self):
        return self.name
    
    def update_email(self, new_email: str):
        self.email = new_email


class Admin(User):
    """Admin user with elevated privileges."""
    
    def __init__(self, name: str, email: str, permissions: list):
        super().__init__(name, email)
        self.permissions = permissions
    
    def grant_permission(self, permission: str):
        self.permissions.append(permission)
    
    def revoke_permission(self, permission: str):
        if permission in self.permissions:
            self.permissions.remove(permission)


class Product:
    """Represents a product in the inventory."""
    
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def calculate_total(self):
        return self.price * self.quantity
    
    def update_quantity(self, new_quantity: int):
        self.quantity = new_quantity

