class BaseObject:
    # attributes: name, description
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def print(self):
        return "**" + self.name + "**: " + self.description


class Trait(BaseObject):
    def __init__(self, name, description, upgrade=None, downgrade=None):
        BaseObject.__init__(self, name, description)
        self.downgrade = downgrade
        self.upgrade = upgrade
        self.unlocked = True

    def active(self):
        pass


class Item(BaseObject):
    def __init__(self, name, description, teaser, damage, quality, item_type):
        BaseObject.__init__(self, name, description)
        self.teaser = teaser
        self.damage = damage
        self.quality = quality
        self.type = item_type
        self.last_price = 0

    def print_teaser(self):
        return "**" + self.name + "**: " + self.teaser


class Effect(BaseObject):
    def __init__(self, name, description, length):
        BaseObject.__init__(self, name, description)
        self.length = length
