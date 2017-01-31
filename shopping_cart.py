

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