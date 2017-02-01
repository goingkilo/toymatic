

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self , item_id):
        if not item_id in self.items:
            self.items.append(item_id)

    def get_items(self):
        return self.items

    def get_item_count(self):
        return len(self.items)

    def remove_item(self, item_id):
        if self.items:
            if item_id in self.items:
                self.items.remove(item_id)
        return item_id



class User1:
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get(self, user_id):
        return User( 'user', '1')