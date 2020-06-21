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

    def active(self):
        pass


class Item(BaseObject):
    def __init__(self, name, description, teaser, damage, quality, uses=-1, hidden=False):
        BaseObject.__init__(self, name, description)
        self.teaser = teaser
        self.damage = damage
        self.quality = quality
        self.uses = uses
        self.hidden = hidden
        self.last_price = 0

    def print(self):
        # TODO: Add an additional "shitty print" function using the other description. "Useless print" maybe
        if self.hidden:
            return "**Unknown item**: ???"
        else:
            return BaseObject.print(self)

    def print_teaser(self):
        return "**" + self.name + "**: " + self.teaser


class Effect(BaseObject):
    def __init__(self, name, description, length):
        BaseObject.__init__(self, name, description)
        self.length = length
