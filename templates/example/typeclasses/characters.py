"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from muddery.typeclasses.characters import MudderyCharacter

class Character(MudderyCharacter):
    """
    The Character defaults to implementing some of its hook methods with the
    following standard functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead)
    at_after_move - launches the "look" command
    at_post_puppet(player) -  when Player disconnects from the Character, we
                    store the current location, so the "unconnected" character
                    object does not need to stay on grid but can be given a
                    None-location while offline.
    at_pre_puppet - just before Player re-connects, retrieves the character's
                    old location and puts it back on the grid with a "charname
                    has connected" message echoed to the room

    """
    def at_object_creation(self):
        """
        Called once, when this object is first created. This is the
        normal hook to overload for most object types.
            
        """
        super(Character, self).at_object_creation()

        # add default hp
        self.db.max_hp = 100
        self.db.hp = self.db.max_hp


    def is_hp_full(self):
        """
        """
        return self.db.hp >= self.db.max_hp


    def recover_hp(self):
        """
        """
        self.db.hp = self.db.max_hp
        self.show_status()
        return


    def poison(self):
        """
        """
        self.db.hp /= 2
        self.show_status()
        return
