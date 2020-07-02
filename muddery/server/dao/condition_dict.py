"""
Query and deal common tables.
"""

from muddery.server.dao.base_query import BaseQuery


class ConditionDict(BaseQuery):
    """
    Descriptions of different conditions.
    """
    table_name = "condition_dict"
