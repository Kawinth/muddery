"""
Combat handler.

The life of a combat:
1. create: create a combat.
2. set_combat: set teams in the combat and the end time if available, then calls the start_combat.
3. start_combat: start the combat. Characters in the combat are allowed to use skills.
4. prepare_skill: characters call the prepare_skill to use skills in the combat. It casts a skill and check if the
   combat is finished.
5. can_finish: Check if the combat is finished. A combat finishes when only one or zero team has alive characters, or
   the combat is timeout. If a combat can finish calls the finish method.
6. finish: send combat results to all characters.
7. leave_combat: characters notify the combat that it has left.
8. stop: if all characters left, remove the combat.
"""

from enum import Enum
from twisted.internet import reactor
from django.conf import settings
from evennia import DefaultScript
from muddery.server.utils import defines


class CStatus(Enum):
    """
    Character's combat status.
    """
    JOINED = 1
    ACTIVE = 2
    FINISHED = 3
    ESCAPED = 4
    LEFT = 5


class BaseCombatHandler(DefaultScript):
    """
    This implements the combat handler.
    """
    # standard Script hooks
    def at_script_creation(self):
        "Called when script is first created"
        self.desc = "handles combat"
        self.interval = 0  # keep running until the battle ends
        self.persistent = False

        """
        store all combatants
        {
            "status": character's status
            "char": character's object
        }
        """
        self.characters = {}

        # if battle is finished
        self.finished = False
        self.winners = {}
        self.losers = {}

        self.timeout = 0
        self.timer = None

    def at_server_shutdown(self):
        """
        This hook is called whenever the server is shutting down fully
        (i.e. not for a restart).
        """
        self.stop()

    def at_stop(self):
        "Called just before the script is stopped/destroyed."
        if self.timer and self.timer.active():
            self.timer.cancel()

    def at_timeout(self):
        """
        Combat timeout.

        Returns:
            None.
        """
        if self.finished:
            return

        self.set_combat_draw()

    def set_combat(self, teams, desc, timeout):
        """
        Add combatant to handler

        Args:
            teams: (dict) {<team id>: [<characters>]}
            desc: (string) combat's description
            timeout: (int) Total combat time in seconds. Zero means no limit.
        """
        self.desc = desc
        self.timeout = timeout

        # Add teams.
        for team in teams:
            for character in teams[team]:
                character.set_team(team)

                self.characters[character.dbref] = {
                    "char": character,
                    "status":  CStatus.JOINED,
                }

        # Set combat to characters.
        for char in self.characters.values():
            character = char["char"]

            # add the combat handler
            character.ndb.combat_handler = self

            # Change the command set.
            character.cmdset.add(settings.CMDSET_COMBAT)

            if character.has_account:
                self.show_combat(character)

        self.start_combat()

        if self.timeout:
            self.timer = reactor.callLater(self.timeout, self.at_timeout)

    def start_combat(self):
        """
        Start a combat, make all NPCs to cast skills automatically.
        """
        for char in self.characters.values():
            char["status"] = CStatus.ACTIVE

    def show_combat(self, character):
        """
        Show combat information to a character.
        Args:
            character: (object) character

        Returns:
            None
        """
        # Show combat information to the player.
        character.msg({"joined_combat": True})

        # send messages in order
        character.msg({"combat_info": self.get_appearance()})

    def prepare_skill(self, skill_key, caller, target):
        """
        Cast a skill.
        """
        if self.finished:
            return

        if caller:
            caller.cast_skill(skill_key, target)

            if self.can_finish():
                # if there is only one team left, kill this handler
                self.finish()

    def can_finish(self):
        """
        Check if can finish this combat. The combat finishes when a team's members
        are all dead.

        Return True or False
        """
        if not len(self.characters):
            return False

        teams = set()
        for char in self.characters.values():
            if char["status"] == CStatus.ACTIVE:
                character = char["char"]
                if character.is_alive():
                    teams.add(character.get_team())
                    if len(teams) > 1:
                        # More than one team has alive characters.
                        return False

        return True

    def finish(self):
        """
        Finish a combat. Send results to players, and kill all failed characters.
        """
        self.finished = True

        if self.timer and self.timer.active():
            self.timer.cancel()

        # get winners and losers
        winner_team = None
        for char in self.characters.values():
            if char["status"] == CStatus.ACTIVE:
                character = char["char"]
                if character.is_alive():
                    winner_team = character.get_team()
                    break

        self.winners = {dbref: char["char"] for dbref, char in self.characters.items()
                        if char["status"] == CStatus.ACTIVE and char["char"].get_team() == winner_team}
        self.losers = {dbref: char["char"] for dbref, char in self.characters.items()
                       if char["status"] == CStatus.ACTIVE and char["char"].get_team() != winner_team}

        for char in self.characters.values():
            char["status"] = CStatus.FINISHED

        self.set_combat_results(self.winners, self.losers)

    def escape_combat(self, caller):
        """
        Character escaped.

        Args:
            caller: (object) the caller of the escape skill.

        Returns:
            None
        """
        if caller and caller.dbref in self.characters:
            self.characters[caller.dbref]["status"] = CStatus.ESCAPED
            caller.combat_result(defines.COMBAT_ESCAPED)

            if self.can_finish():
                # if there is only one team left, kill this handler
                self.finish()

    def leave_combat(self, character):
        """
        Remove combatant from handler.

        :param character: character object
        """
        if character.dbref in self.characters:
            if self.characters[character.dbref]["status"] == CStatus.LEFT:
                return
            self.characters[character.dbref]["status"] = CStatus.LEFT

        all_player_left = True
        for char in self.characters.values():
            if char["status"] != CStatus.LEFT and\
               char["char"].is_typeclass(settings.BASE_PLAYER_CHARACTER_TYPECLASS, exact=False):
                all_player_left = False
                break

        if all_player_left:
            # There is no player character in combat.
            for char in self.characters.values():
                if char["status"] != CStatus.LEFT:
                    char["status"] = CStatus.LEFT
                    char["char"].leave_combat()

            self.stop()

    def msg_all(self, message):
        "Send message to all combatants"
        for char in self.characters.values():
            char["char"].msg(message)

    def set_combat_draw(self):
        """
        Called when the combat ended in a draw.

        Returns:
            None.
        """
        for char in self.characters.values():
            char["char"].combat_result(defines.COMBAT_DRAW)

    def set_combat_results(self, winners, losers):
        """
        Called when the character wins the combat.

        Args:
            winners: (List) all combat winners.
            losers: (List) all combat losers.

        Returns:
            None
        """
        for character in winners.values():
            character.combat_result(defines.COMBAT_WIN, losers.values())

        for character in losers.values():
            character.combat_result(defines.COMBAT_LOSE, winners.values())

    def get_appearance(self):
        """
        Get the combat appearance.
        """
        appearance = {"desc": self.desc,
                      "timeout": self.timeout,
                      "characters": []}
        
        for char in self.characters.values():
            character = char["char"]
            info = character.get_appearance(self)
            info["team"] = character.get_team()

            appearance["characters"].append(info)

        return appearance

    def get_combat_characters(self):
        """
        Get all characters in combat.
        """
        return self.characters.values()

    def is_finished(self):
        """
        :return: combat finished or not.
        """
        return self.finished

    def get_combat_result(self, character):
        """
        Get a character's combat result.

        :param character: character object
        :return:
        """
        if not self.finished:
            return

        if character.dbref not in self.characters:
            return

        if self.characters[character.dbref]:
            status = self.characters[character.dbref]["status"]

            if status == CStatus.ESCAPED:
                return defines.COMBAT_ESCAPED, None
            elif status == CStatus.FINISHED or status == CStatus.LEFT:
                if character.dbref in self.winners:
                    return defines.COMBAT_WIN, self.losers.values()
                elif character.dbref in self.losers:
                    return defines.COMBAT_LOSE, self.winners.values()
                else:
                    return defines.COMBAT_DRAW, None
            else:
                return defines.COMBAT_DRAW, None
