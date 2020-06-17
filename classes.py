class BaseObject:
    # attributes: name, description
    def __init__(self, description):
        self.description = description


class Trait(BaseObject):
    def __init__(self, description, upgrade=None, downgrade=None):
        BaseObject.__init__(self, description)
        self.downgrade = downgrade
        self.upgrade = upgrade


class Item(BaseObject):
    def __init__(self, description, damage, quality, uses=-1):
        BaseObject.__init__(self, description)
        self.damage = damage
        self.quality = quality
        self.uses = uses


class Effect(BaseObject):
    def __init__(self, description, length):
        BaseObject.__init__(self, description)
        self.length = length
