
import re
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings


KEY_LENGTH = 255
NAME_LENGTH = 80
TYPECLASS_LENGTH = 80
POSITION_LENGTH = 80
VALUE_LENGTH = 80
CONDITION_LENGTH = 255

re_attribute_key = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


# ------------------------------------------------------------
#
# The game world system's data.
# Users should not modify it manually.
#
# ------------------------------------------------------------
class system_data(models.Model):
    """
    The game world system's data.
    """
    # The automatic index of objects.
    object_index = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "System Data"
        verbose_name_plural = "System Data"


# ------------------------------------------------------------
#
# Game's basic settings.
#
# ------------------------------------------------------------
class game_settings(models.Model):
    """
    Game's basic settings.
    NOTE: Only uses the first record!
    """

    # The name of your game.
    game_name = models.CharField(max_length=NAME_LENGTH, blank=True)

    # The screen shows to players who are not loggin.
    connection_screen = models.TextField(blank=True)

    # In solo mode, a player can not see or affect other players.
    solo_mode = models.BooleanField(blank=True, default=False)

    # Time of global CD.
    global_cd = models.FloatField(blank=True,
                                  default=1.0,
                                  validators=[MinValueValidator(0.0)])

    # The CD of auto casting a skill. It must be bigger than GLOBAL_CD
    # They can not be equal!
    auto_cast_skill_cd = models.FloatField(blank=True,
                                           default=1.5,
                                           validators=[MinValueValidator(0.0)])

    # Allow players to give up quests.
    can_give_up_quests = models.BooleanField(blank=True, default=True)

    # can close dialogue box or not.
    can_close_dialogue = models.BooleanField(blank=True, default=False)

    # Can resume unfinished dialogues automatically.
    auto_resume_dialogues = models.BooleanField(blank=True, default=True)

    # The key of a world room.
    # It is the default home location used for all objects. This is used as a
    # fallback if an object's normal home location is deleted. It is the
    # key of the room. If it is empty, the home will be set to the first
    # room in WORLD_ROOMS.
    default_home_key = models.CharField(max_length=KEY_LENGTH, blank=True)

    # The key of a world room.
    # The start position for new characters. It is the key of the room.
    # If it is empty, the home will be set to the first room in WORLD_ROOMS.
    start_location_key = models.CharField(max_length=KEY_LENGTH, blank=True)

    # The key of a world room.
    # Player's default home. When a player dies, he will be moved to his home.
    default_player_home_key = models.CharField(max_length=KEY_LENGTH, blank=True)

    # The key of a character.
    # Default character of players.
    default_player_character_key = models.CharField(max_length=KEY_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Game Setting"
        verbose_name_plural = "Game Settings"


# ------------------------------------------------------------
# Object's base
# ------------------------------------------------------------
class BaseObjects(models.Model):
    """
    The base model of all objects. All objects data are linked with keys.
    """
    # object's key
    key = models.CharField(max_length=KEY_LENGTH, unique=True, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"

    def __unicode__(self):
        return self.key


class objects(BaseObjects):
    """
    All objects.
    """
    # object's typeclass
    typeclass = models.CharField(max_length=KEY_LENGTH)

    # object's name
    name = models.CharField(max_length=NAME_LENGTH, blank=True)

    # object's description for display
    desc = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"

    def __unicode__(self):
        return self.name + " (" + self.key + ")"


class world_areas(BaseObjects):
    "The game map is composed by areas."

    # area's map background image resource
    background = models.CharField(max_length=KEY_LENGTH, blank=True)

    # area's width
    width = models.PositiveIntegerField(blank=True, default=0)

    # area's height
    height = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "World Area"
        verbose_name_plural = "World Areas"


class world_rooms(BaseObjects):
    "Defines all unique rooms."

    # players can not fight in peaceful romms
    peaceful = models.BooleanField(blank=True, default=False)

    # The key of a world area.
    # The room's location, it must be a area.
    location = models.CharField(max_length=KEY_LENGTH, blank=True, db_index=True)

    # room's position which is used in maps
    position = models.CharField(max_length=POSITION_LENGTH, blank=True)

    # room's icon resource
    icon = models.CharField(max_length=KEY_LENGTH, blank=True)

    # room's background image resource
    background = models.CharField(max_length=KEY_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class world_exits(BaseObjects):
    "Defines all unique exits."

    # the action verb to enter the exit (optional)
    verb = models.CharField(max_length=NAME_LENGTH, blank=True)

    # The key of a world room.
    # The exit's location, it must be a room.
    # Players can see and enter an exit from this room.
    location = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of a world room.
    # The exits's destination.
    destination = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # the condition to show the exit
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Exit"
        verbose_name_plural = "Exits"


class world_objects(BaseObjects):
    "Store all unique objects."

    # The key of a world room.
    # object's location, it must be a room
    location = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # Action's name
    action = models.CharField(max_length=NAME_LENGTH, blank=True)

    # the condition for showing the object
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    # object's icon resource
    icon = models.CharField(max_length=KEY_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "World Object"
        verbose_name_plural = "World Objects"


class common_objects(BaseObjects):
    "Store all common objects."

    # the max number of this object in one pile, must above 1
    max_stack = models.PositiveIntegerField(blank=True, default=1)

    # if can have only one pile of this object
    unique = models.BooleanField(blank=True, default=False)

    # if this object can be removed from the inventory when its number is decreased to zero.
    can_remove = models.BooleanField(blank=True, default=True)

    # if this object can discard
    can_discard = models.BooleanField(blank=True, default=True)

    # object's icon resource
    icon = models.CharField(max_length=KEY_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Common Object"
        verbose_name_plural = "Common Objects"


class foods(BaseObjects):
    "Foods inherit from common objects."

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Food"
        verbose_name_plural = "Foods"


class skill_books(BaseObjects):
    "Skill books inherit from common objects."

    # skill's key
    skill = models.CharField(max_length=KEY_LENGTH)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Skill Book"
        verbose_name_plural = "Skill Books"


class equipments(BaseObjects):
    "equipments inherit from common objects."

    # The key of an equipment position.
    # equipment's position
    position = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of an equipment type.
    # equipment's type
    type = models.CharField(max_length=KEY_LENGTH)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"


class characters(BaseObjects):
    "Store common characters."

    # Character's level.
    level = models.PositiveIntegerField(blank=True, default=1)

    # Reborn time. The time of reborn after this character was killed. 0 means never reborn.
    reborn_time = models.PositiveIntegerField(blank=True, default=0)

    # Friendly of this character.
    friendly = models.IntegerField(blank=True, default=0)

    # Character's icon resource.
    icon = models.CharField(max_length=KEY_LENGTH, blank=True)

    # Clone another character's custom properties if this character's data is empty.
    clone = models.CharField(max_length=KEY_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Common Character List"
        verbose_name_plural = "Common Character List"


class base_npcs(BaseObjects):
    "The base of all NPCs."

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Base NPC"
        verbose_name_plural = "Base NPCs"


class common_npcs(BaseObjects):
    "Common NPCs."

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Common NPC"
        verbose_name_plural = "Common NPCs"


class world_npcs(BaseObjects):
    "Store all NPCs."

    # NPC's location, it must be a room.
    location = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # the condition for showing the NPC
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "World NPC"
        verbose_name_plural = "World NPCs"


class player_characters(BaseObjects):
    "Player's character."

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Player Character"
        verbose_name_plural = "Player Characters"


class shops(BaseObjects):
    "Store all shops."

    # the verb to open the shop
    verb = models.CharField(max_length=NAME_LENGTH, blank=True)

    # condition of the shop
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    # shop's icon resource
    icon = models.CharField(max_length=KEY_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Shop"
        verbose_name_plural = "Shops"


class shop_goods(BaseObjects):
    "All goods that sold in shops."

    # shop's key
    shop = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # the key of objects to sell
    goods = models.CharField(max_length=KEY_LENGTH)

    # goods level
    level = models.PositiveIntegerField(blank=True, default=0)

    # number of shop goods
    number = models.PositiveIntegerField(blank=True, default=1)

    # the price of the goods
    price = models.PositiveIntegerField(blank=True, default=1)

    # the unit of the goods price
    unit = models.CharField(max_length=KEY_LENGTH)

    # visible condition of the goods
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Shop Object"
        verbose_name_plural = "Shop Objects"


class skills(BaseObjects):
    "Store all skills."

    # skill's message when casting
    message = models.TextField(blank=True)

    # skill's cd
    cd = models.FloatField(blank=True, default=0)

    # if it is a passive skill
    passive = models.BooleanField(blank=True, default=False)

    # skill function's name
    function = models.CharField(max_length=KEY_LENGTH, blank=True)

    # skill's icon resource
    icon = models.CharField(max_length=KEY_LENGTH, blank=True)

    # skill's main type, used in autocasting skills.
    main_type = models.CharField(max_length=KEY_LENGTH, blank=True)

    # skill's sub type, used in autocasting skills.
    sub_type = models.CharField(max_length=KEY_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


class quests(BaseObjects):
    "Store all quests."

    # the condition to accept this quest.
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    # will do this action after a quest completed
    action = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Quest"
        verbose_name_plural = "Quests"


# ------------------------------------------------------------
#
# exit lock's additional data
#
# ------------------------------------------------------------
class exit_locks(BaseObjects):
    "Locked exit's additional data"

    # condition of the lock
    unlock_condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    # action to unlock the exit (optional)
    unlock_verb = models.CharField(max_length=NAME_LENGTH, blank=True)

    # description when locked
    locked_desc = models.TextField(blank=True)

    # if the exit can be unlocked automatically
    auto_unlock = models.BooleanField(blank=True, default=False)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Exit Lock"
        verbose_name_plural = "Exit Locks"


# ------------------------------------------------------------
#
# object creator's additional data
#
# ------------------------------------------------------------
class object_creators(BaseObjects):
    "Players can get new objects from an object_creator."

    # related object's key
    relation = models.CharField(max_length=KEY_LENGTH, db_index=True, blank=True)

    # loot's verb
    loot_verb = models.CharField(max_length=NAME_LENGTH, blank=True)

    # loot's condition
    loot_condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Object Creator"
        verbose_name_plural = "Object Creators"


# ------------------------------------------------------------
#
# store objects loot list
#
# ------------------------------------------------------------
class loot_list(models.Model):
    "Loot list. It is used in object_creators and mods."

    # the provider of the object
    provider = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # the key of dropped object
    object = models.CharField(max_length=KEY_LENGTH)

    # number of dropped object
    number = models.PositiveIntegerField(blank=True, default=0)

    # odds of drop, from 0.0 to 1.0
    odds = models.FloatField(blank=True, default=0)

    # The key of a quest.
    # if it is not empty, the player must have this quest, or will not drop
    quest = models.CharField(max_length=KEY_LENGTH, blank=True)

    # condition of the drop
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Loot List"
        verbose_name_plural = "Loot Lists"
        unique_together = ("provider", "object")


# ------------------------------------------------------------
#
# object creator's loot list
#
# ------------------------------------------------------------
class creator_loot_list(loot_list):
    "Store character's loot list."

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Object Creator's Loot List"
        verbose_name_plural = "Object Creator's Loot Lists"
        unique_together = ("provider", "object")


# ------------------------------------------------------------
#
# character's loot list
#
# ------------------------------------------------------------
class character_loot_list(loot_list):
    "Store character's loot list."

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Character's Loot List"
        verbose_name_plural = "Character's Loot Lists"
        unique_together = ("provider", "object")


# ------------------------------------------------------------
#
# quest's rewards
#
# ------------------------------------------------------------
class quest_reward_list(loot_list):
    "Quest reward's list."

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Quest's reward List"
        verbose_name_plural = "Quest's reward Lists"
        unique_together = ("provider", "object")


# ------------------------------------------------------------
#
# store all equip_types
#
# ------------------------------------------------------------
class equipment_types(models.Model):
    "Store all equip types."

    # equipment type's key
    key = models.CharField(max_length=KEY_LENGTH, unique=True)

    # type's name
    name = models.CharField(max_length=NAME_LENGTH, unique=True)

    # type's description
    desc = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Equipment's Type"
        verbose_name_plural = "Equipment's Types"

    def __unicode__(self):
        return self.name


# ------------------------------------------------------------
#
# store all available equipment potisions
#
# ------------------------------------------------------------
class equipment_positions(models.Model):
    "Store all equip types."

    # position's key
    key = models.CharField(max_length=KEY_LENGTH, unique=True)

    # position's name for display
    name = models.CharField(max_length=NAME_LENGTH, unique=True)

    # position's description
    desc = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Equipment's Position"
        verbose_name_plural = "Equipment's Positions"

    def __unicode__(self):
        return self.name


# ------------------------------------------------------------
#
# Object's custom properties.
#
# ------------------------------------------------------------
class properties_dict(models.Model):
    """
    Object's custom properties.
    """
    # The key of a typeclass.
    typeclass = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of the property.
    property = models.CharField(max_length=KEY_LENGTH)

    # The name of the property.
    name = models.CharField(max_length=NAME_LENGTH)

    # Whether this property will be changed or not.
    mutable = models.BooleanField(blank=True, default=False)

    # Default value.
    default = models.CharField(max_length=VALUE_LENGTH, blank=True)

    # The description of the property.
    desc = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Properties Dict"
        verbose_name_plural = "Properties Dict"
        unique_together = ("typeclass", "property")


# ------------------------------------------------------------
#
# Object's custom properties
#
# ------------------------------------------------------------
class object_properties(models.Model):
    "Store object's custom properties."
    # The key of an object.
    object = models.CharField(max_length=KEY_LENGTH)

    # The level of the object.
    level = models.PositiveIntegerField(blank=True, default=0)

    # The key of the property.
    property = models.CharField(max_length=KEY_LENGTH)

    # The value of the property.
    value = models.CharField(max_length=VALUE_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Object's Property"
        verbose_name_plural = "Object's Properties"
        unique_together = ("object", "level", "property")
        index_together = [("object", "level")]


# ------------------------------------------------------------
#
# character's default objects
#
# ------------------------------------------------------------
class default_objects(models.Model):
    "character's default objects"

    # Character's key.
    character = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of an object.
    # Object's key.
    object = models.CharField(max_length=KEY_LENGTH)

    # Object's level.
    level = models.PositiveIntegerField(blank=True, default=0)

    # Object's number
    number = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Character's Default Object"
        verbose_name_plural = "Character's Default Objects"
        unique_together = ("character", "object")


# ------------------------------------------------------------
#
# store npc's shop
#
# ------------------------------------------------------------
class npc_shops(models.Model):
    "Store npc's shops."

    # The key of an NPC.
    # NPC's key
    npc = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of a shop.
    # shop's key
    shop = models.CharField(max_length=KEY_LENGTH, db_index=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "NPC Shop"
        verbose_name_plural = "NPC Shops"
        unique_together = ("npc", "shop")


# ------------------------------------------------------------
#
# skill types
#
# ------------------------------------------------------------
class skill_types(models.Model):
    """
    Skill's type, used in skill's main_type and sub_type. The type discribes the usage of a
    skill, which is useful in auto casting skills.
    """
    # type's key
    key = models.CharField(max_length=KEY_LENGTH, unique=True, blank=True)

    # the readable name of the skill type
    name = models.CharField(max_length=NAME_LENGTH, unique=True)

    # skill type's description
    desc = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Skill's Type"
        verbose_name_plural = "Skill's Types"

    def __unicode__(self):
        return self.name + " (" + self.key + ")"


# ------------------------------------------------------------
#
# character's default skills
#
# ------------------------------------------------------------
class default_skills(models.Model):
    "character's default skills"

    # character's key
    character = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of a skill.
    # skill's key
    skill = models.CharField(max_length=KEY_LENGTH)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Character's Skill"
        verbose_name_plural = "Character's Skills"
        unique_together = ("character", "skill")


# ------------------------------------------------------------
#
# store quest objectives
#
# ------------------------------------------------------------
class quest_objectives(models.Model):
    "Store all quest objectives."

    # The key of a quest.
    # quest's key
    quest = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # objective's ordinal
    ordinal = models.IntegerField(blank=True, default=0)

    # The key of an objetive type.
    # objective's type
    type = models.CharField(max_length=KEY_LENGTH)

    # relative object's key
    object = models.CharField(max_length=KEY_LENGTH, blank=True)

    # objective's number
    number = models.IntegerField(blank=True, default=0)

    # objective's discription for display
    desc = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Quest Objective"
        verbose_name_plural = "Quest Objectives"
        unique_together = ("quest", "ordinal")


# ------------------------------------------------------------
#
# store quest dependencies
#
# ------------------------------------------------------------
class quest_dependencies(models.Model):
    "Store quest dependency."

    # The key of a quest.
    # quest's key
    quest = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of a quest.
    # quest that dependends on
    dependency = models.CharField(max_length=KEY_LENGTH)

    # The key of a quest dependency type.
    # dependency's type
    type = models.CharField(max_length=KEY_LENGTH)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Quest Dependency"
        verbose_name_plural = "Quest Dependency"


# ------------------------------------------------------------
#
# store event data
#
# ------------------------------------------------------------
class event_data(models.Model):
    "Store event data."

    # event's key
    key = models.CharField(max_length=KEY_LENGTH, unique=True, blank=True)

    # trigger's relative object's key
    trigger_obj = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The type of the event trigger.
    # event's trigger
    trigger_type = models.CharField(max_length=KEY_LENGTH)

    # The type of an event action.
    # event's action
    action = models.CharField(max_length=KEY_LENGTH)

    # The odds of this event.
    odds = models.FloatField(blank=True, default=1.0)

    # the condition to enable this event
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __unicode__(self):
        return self.key


# ------------------------------------------------------------
#
# store all dialogues
#
# ------------------------------------------------------------
class dialogues(models.Model):
    "Store all dialogues."

    # dialogue's key
    key = models.CharField(max_length=KEY_LENGTH, unique=True, blank=True)

    # dialogue's name
    name = models.CharField(max_length=NAME_LENGTH, default="")

    # condition to show this dialogue
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Dialogue"
        verbose_name_plural = "Dialogues"

    def __unicode__(self):
        return self.name + " (" + self.key + ")"


# ------------------------------------------------------------
#
# store dialogue quest dependencies
#
# ------------------------------------------------------------
class dialogue_quest_dependencies(models.Model):
    "Store dialogue quest dependencies."

    # The key of a dialogue.
    # dialogue's key
    dialogue = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of a quest.
    # related quest's key
    dependency = models.CharField(max_length=KEY_LENGTH)

    # The key of a quest dependency type.
    # dependency's type
    type = models.CharField(max_length=KEY_LENGTH)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Dialogue Quest Dependency"
        verbose_name_plural = "Dialogue Quest Dependencies"


# ------------------------------------------------------------
#
# store dialogue relations
#
# ------------------------------------------------------------
class dialogue_relations(models.Model):
    "Store dialogue relations."

    # The key of a dialogue.
    # dialogue's key
    dialogue = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of a dialogue.
    # next dialogue's key
    next_dlg = models.CharField(max_length=KEY_LENGTH, db_index=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Dialogue Relation"
        verbose_name_plural = "Dialogue Relations"


# ------------------------------------------------------------
#
# store dialogue sentences
#
# ------------------------------------------------------------
class dialogue_sentences(models.Model):
    "Store dialogue sentences."

    # sentence's key
    key = models.CharField(max_length=KEY_LENGTH, unique=True, blank=True)

    # The key of a dialogue.
    # dialogue's key
    dialogue = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # sentence's ordinal
    ordinal = models.IntegerField()

    # sentence's speaker
    speaker = models.CharField(max_length=NAME_LENGTH, blank=True)

    # speaker's icon resource
    icon = models.CharField(max_length=KEY_LENGTH, blank=True)

    # sentence's content
    content = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Dialogue Sentence"
        verbose_name_plural = "Dialogue Sentences"


# ------------------------------------------------------------
#
# store npc's dialogue
#
# ------------------------------------------------------------
class npc_dialogues(models.Model):
    "Store npc's dialogues."

    # The key of an NPC.
    # NPC's key
    npc = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # The key of a dialogue.
    # dialogue's key
    dialogue = models.CharField(max_length=KEY_LENGTH, db_index=True)

    # if it is a default dialogue
    default = models.BooleanField(blank=True, default=False)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "NPC Dialogue"
        verbose_name_plural = "NPC Dialogues"


# ------------------------------------------------------------
#
# event's data
#
# ------------------------------------------------------------
class BaseEventActionData(models.Model):
    # The key of an event.
    event_key = models.CharField(max_length=KEY_LENGTH, db_index=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"


# ------------------------------------------------------------
#
# action to attack a target
#
# ------------------------------------------------------------
class action_attack(BaseEventActionData):
    "action attack's data"

    # The key of a common character.
    # mob's key
    mob = models.CharField(max_length=KEY_LENGTH)

    # mob's level
    # Set the level of the mob. If it is 0, use the default level of the mob.
    level = models.IntegerField(blank=True, default=0)

    # event's odds ([0.0, 1.0])
    odds = models.FloatField(blank=True, default=0)

    # combat's description
    desc = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Event Mob"
        verbose_name_plural = "Event Mobs"


# ------------------------------------------------------------
#
# action to begin a dialogue
#
# ------------------------------------------------------------
class action_dialogue(BaseEventActionData):
    "Store all event dialogues."

    # The key of a dialogue.
    # dialogue's key
    dialogue = models.CharField(max_length=KEY_LENGTH)

    # The key of an NPC.
    # NPC's key
    npc = models.CharField(max_length=KEY_LENGTH, blank=True)

    # event's odds
    odds = models.FloatField(blank=True, default=0)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Event Dialogues"
        verbose_name_plural = "Event Dialogues"


# ------------------------------------------------------------
#
# action to learn a skill
#
# ------------------------------------------------------------
class action_learn_skill(BaseEventActionData):
    "Store all actions to learn skills."

    # The key of a skill.
    # skill's key
    skill = models.CharField(max_length=KEY_LENGTH)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Action Learn Skill"
        verbose_name_plural = "Action Learn Skills"


# ------------------------------------------------------------
#
# action to accept a quest
#
# ------------------------------------------------------------
class action_accept_quest(BaseEventActionData):
    "Store all actions to accept quests."

    # The key of a quest.
    # quest's key
    quest = models.CharField(max_length=KEY_LENGTH)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Action Accept Quest"
        verbose_name_plural = "Action Accept Quests"


# ------------------------------------------------------------
#
# action to turn in a quest
#
# ------------------------------------------------------------
class action_turn_in_quest(BaseEventActionData):
    "Store all actions to turn in a quest."

    # The key of a quest.
    # quest's key
    quest = models.CharField(max_length=KEY_LENGTH)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Action Turn in Quest"
        verbose_name_plural = "Action Turn in Quests"


# ------------------------------------------------------------
#
# action to close an event
#
# ------------------------------------------------------------
class action_close_event(BaseEventActionData):
    "Store all event closes."

    # The key of an event to close.
    event = models.CharField(max_length=KEY_LENGTH)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Event Close"
        verbose_name_plural = "Event Closes"


# ------------------------------------------------------------
#
# action to send a message to the character
#
# ------------------------------------------------------------
class action_message(BaseEventActionData):
    """
    The Action to send a message to the character.
    """
    # Messages.
    message = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Event Message"
        verbose_name_plural = "Event Messages"


# ------------------------------------------------------------
#
# action to trigger other actions at interval.
#
# ------------------------------------------------------------
class action_room_interval(BaseEventActionData):
    """
    The action to trigger other actions at interval.
    """
    # Repeat interval in seconds.
    interval = models.PositiveIntegerField(blank=True, default=0)

    # Can trigger events when the character is offline.
    offline = models.BooleanField(blank=True, default=False)

    # The event action.
    action = models.CharField(max_length=KEY_LENGTH)

    # This message will be sent to the character when the interval begins.
    begin_message = models.TextField(blank=True)

    # This message will be sent to the character when the interval ends.
    end_message = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Event Room Interval"
        verbose_name_plural = "Event Room Intervals"


# ------------------------------------------------------------
#
# action to add objects to characters
#
# ------------------------------------------------------------
class action_get_objects(BaseEventActionData):
    """
    The Action to add objects to characters
    """
    # The object's key.
    object = models.CharField(max_length=KEY_LENGTH)

    # The object's number.
    number = models.PositiveIntegerField(blank=True, default=0)

    # The odds to get these objects. ([0.0, 1.0])
    odds = models.FloatField(blank=True, default=0)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Event Get Object"
        verbose_name_plural = "Event Get Objects"


# ------------------------------------------------------------
#
# condition descriptions
#
# ------------------------------------------------------------
class condition_desc(models.Model):
    "Object descriptions in different conditions."

    # The key of an object.
    key = models.CharField(max_length=KEY_LENGTH)

    # condition
    condition = models.CharField(max_length=CONDITION_LENGTH, blank=True)

    # exit's description for display
    desc = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Condition Description"
        verbose_name_plural = "Condition Descriptions"
        unique_together = ("key", "condition")


# ------------------------------------------------------------
#
# localized strings
#
# ------------------------------------------------------------
class localized_strings(models.Model):
    "Store all localized strings."

    # is system data or not
    system_data = models.BooleanField(blank=True, default=False)

    # word's category
    category = models.CharField(max_length=KEY_LENGTH, blank=True)

    # the origin words
    origin = models.TextField()

    # translated worlds
    local = models.TextField(blank=True)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Localized String"
        verbose_name_plural = "Localized Strings"
        unique_together = ("category", "origin")


# ------------------------------------------------------------
#
# set image resources
#
# ------------------------------------------------------------
class image_resources(models.Model):
    "Store resource's information."

    # image's path
    resource = models.CharField(max_length=KEY_LENGTH, unique=True)

    # image's type
    type = models.CharField(max_length=KEY_LENGTH)

    # resource'e width
    image_width = models.PositiveIntegerField(blank=True, default=0)

    # resource'e height
    image_height = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        "Define Django meta options"
        abstract = True
        app_label = "worlddata"
        verbose_name = "Image Resource"
        verbose_name_plural = "Image Resources"

    def __unicode__(self):
        return self.resource
