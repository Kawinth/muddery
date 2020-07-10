"""
Query and deal common tables.
"""

from muddery.server.dao.base_query import BaseQuery
from muddery.server.dao.worlddata import WorldData


class GameSettings(BaseQuery):
    """
    Game setting data.
    """
    table_name = "game_settings"

    @classmethod
    def get_fields(cls):
        """
        Get table fields.
        """
        return WorldData.get_fields(cls.table_name)
