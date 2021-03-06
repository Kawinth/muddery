"""
Battle commands. They only can be used when a character is in a combat.
"""

import json
from evennia.utils import logger
from evennia.server.sessionhandler import SESSIONS
from muddery.worldeditor.services import data_query, data_edit, general_query
from muddery.server.utils.exception import MudderyError, ERR
from muddery.worldeditor.utils.response import success_response
from muddery.server.utils.builder import build_all
from muddery.worldeditor.controllers.base_request_processer import BaseRequestProcesser
from muddery.worldeditor.dao import general_query_mapper
from muddery.server.mappings.event_action_set import EVENT_ACTION_SET
from muddery.server.dao.worlddata import WorldData


class QueryAllTypeclasses(BaseRequestProcesser):
    """
    Query all typeclasses.

    Args:
        None.
    """
    path = "query_all_typeclasses"
    name = ""

    def func(self, args, request):
        data = data_query.query_all_typeclasses()
        return success_response(data)


class QueryFields(BaseRequestProcesser):
    """
    Query all fields of a table.

    Args:
        None.
    """
    path = "query_fields"
    name = ""

    def func(self, args, request):
        if 'table' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "table".')

        table_name = args["table"]

        data = general_query.query_fields(table_name)
        return success_response(data)


class QueryTable(BaseRequestProcesser):
    """
    Query all records of a table.

    Args:
        None.
    """
    path = "query_table"
    name = ""

    def func(self, args, request):
        if 'table' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "table".')

        table_name = args["table"]

        data = general_query.query_table(table_name)
        return success_response(data)


class QueryTypeclassTable(BaseRequestProcesser):
    """
    Query a table of objects of the same typeclass.

    Args:
        typeclass: (string) typeclass's key.
    """
    path = "query_typeclass_table"
    name = ""

    def func(self, args, request):
        if 'typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "typeclass".')

        typeclass_key = args["typeclass"]

        # Query data.
        data = data_query.query_typeclass_table(typeclass_key)
        return success_response(data)


class QueryRecord(BaseRequestProcesser):
    """
    Query a record of a table.

    Args:
        table: (string) table's name.
        record: (string) record's id.
    """
    path = "query_record"
    name = ""

    def func(self, args, request):
        if ('table' not in args) or ('record' not in args):
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        table_name = args["table"]
        record_id = args["record"]

        data = general_query.query_record(table_name, record_id)
        return success_response(data)


class QueryAreas(BaseRequestProcesser):
    """
    Query all available areas.

    Args:
        None.
    """
    path = "query_areas"
    name = ""

    def func(self, args, request):
        data = data_query.query_areas()
        return success_response(data)


class QueryTypeclassProperties(BaseRequestProcesser):
    """
    Query a typeclass's properties.

    Args:
        typeclass: (string) typeclass's key.
    """
    path = "query_typeclass_properties"
    name = ""

    def func(self, args, request):
        if 'typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "typeclass".')

        typeclass = args["typeclass"]

        data = data_query.query_typeclass_properties(typeclass)
        return success_response(data)


class QueryObjectProperties(BaseRequestProcesser):
    """
    Query a typeclass's properties.

    Args:
        typeclass: (string) object's typeclass
        obj_key: (string) object's key.
    """
    path = "query_object_properties"
    name = ""

    def func(self, args, request):
        if 'typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "typeclass".')

        if 'obj_key' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "obj_key".')

        typeclass_key = args["typeclass"]
        obj_key = args["obj_key"]

        data = data_query.query_object_properties(typeclass_key, obj_key)
        return success_response(data)


class QueryObjectLevelProperties(BaseRequestProcesser):
    """
    Query a level of an object's properties.

    Args:
        obj_key: (string) object's key.
        level: (number) level's number
    """
    path = "query_object_level_properties"
    name = ""

    def func(self, args, request):
        if 'obj_key' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "obj_key".')

        if 'level' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "level".')

        obj_key = args["obj_key"]
        level = args["level"]

        data = data_query.query_object_level_properties(obj_key, level)
        return success_response(data)


class SaveObjectLevelProperties(BaseRequestProcesser):
    """
    Save properties of an object.

    Args:
        obj_key: (string) object's key.
        level: (number) level's number.
        values: (dict) values to save.
    """
    path = "save_object_level_properties"
    name = ""

    def func(self, args, request):
        if 'obj_key' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "obj_key".')

        if 'level' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "level".')

        if 'values' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "values".')

        obj_key = args["obj_key"]
        level = args["level"]
        values = args["values"]

        data_edit.save_object_level_properties(obj_key, level, values)
        return success_response("success")


class DeleteObjectLevelProperties(BaseRequestProcesser):
    """
    Query a level of an object's properties.

    Args:
        obj_key: (string) object's key.
        level: (number) level's number
    """
    path = "delete_object_level_properties"
    name = ""

    def func(self, args, request):
        if 'obj_key' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "obj_key".')

        if 'level' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "level".')

        obj_key = args["obj_key"]
        level = args["level"]

        data_edit.delete_object_level_properties(obj_key, level)
        data = {"level": level}
        return success_response(data)


class QueryEventTriggers(BaseRequestProcesser):
    """
    Query all event triggers of the given typeclass.

    Args:
        typeclass: (string) the object's typeclass.
    """
    path = "query_event_triggers"
    name = ""

    def func(self, args, request):
        if 'typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "typeclass".')

        typeclass = args["typeclass"]

        data = data_query.query_event_triggers(typeclass)
        return success_response(data)


class QueryObjectEvents(BaseRequestProcesser):
    """
    Query all events of the given object.

    Args:
        object: (string) object's key.
    """
    path = "query_object_events"
    name = ""

    def func(self, args, request):
        if 'object' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "object".')

        object_key = args["object"]

        data = data_query.query_object_events(object_key)
        return success_response(data)


class QueryEventActionData(BaseRequestProcesser):
    """
    Query an event action's data.

    Args:
        action: (string) action's type
        event: (string) event's key
    """
    path = "query_event_action_data"
    name = ""

    def func(self, args, request):
        if 'action' not in args or 'event' not in args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        action_type = args["action"]
        event_key = args["event"]

        data = data_query.query_event_action_data(action_type, event_key)
        return success_response(data)


class QueryEventActionForm(BaseRequestProcesser):
    """
    Query the form of the event action.

    Args:
        action: (string) action's type
        event: (string) event's key
    """
    path = "query_event_action_forms"
    name = ""

    def func(self, args, request):
        if 'action' not in args or 'event' not in args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        action_type = args["action"]
        event_key = args["event"]

        data = data_edit.query_event_action_forms(action_type, event_key)
        return success_response(data)


class QueryDialogueSentences(BaseRequestProcesser):
    """
    Query a dialogue's sentences.

    Args:
        key: (string) dialogue's key
    """
    path = "query_dialogue_sentences"
    name = ""

    def func(self, args, request):
        if 'dialogue' not in args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        dialogue_key = args["dialogue"]

        data = data_query.query_dialogue_sentences(dialogue_key)
        return success_response(data)


class QueryForm(BaseRequestProcesser):
    """
    Query a form of a record of a table.

    Args:
        table: (string) table's name
        record: (string, optional) record's id. If it is empty, get a new record.
    """
    path = "query_form"
    name = ""

    def func(self, args, request):
        if 'table' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "table".')

        table_name = args["table"]
        record = args.get('record', None)

        data = data_edit.query_form(table_name, id=record)
        return success_response(data)


class QueryFormFirstRecord(BaseRequestProcesser):
    """
    Query a form of the first record of a table.

    Args:
        table: (string) table's name
    """
    path = "query_form_first_record"
    name = ""

    def func(self, args, request):
        if 'table' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "table".')

        table_name = args["table"]

        try:
            record = general_query_mapper.get_the_first_record(table_name)
            if record:
                record_id = record.id
            else:
                record_id = None
        except Exception as e:
            raise MudderyError(ERR.invalid_form, "Wrong table: %s." % table_name)

        data = data_edit.query_form(table_name, id=record_id)
        return success_response(data)


class SaveForm(BaseRequestProcesser):
    """
    Save a form.

    Args:
        values: (dict) values to save.
        table: (string) table's name.
        record: (string, optional) record's id. If it is empty, add a new record.
    """
    path = "save_form"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if 'values' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "values".')

        if 'table' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "table".')

        values = args["values"]
        table_name = args["table"]
        record_id = args.get('record', None)

        record_id = data_edit.save_form(values, table_name, record_id)
        data = data_edit.query_form(table_name, id=record_id)
        return success_response(data)


class SaveEventActionForm(BaseRequestProcesser):
    """
    Save an action's form.

    Args:
        action: (string) action's type.
        event: (string) event's key.
        values: (list) a list of action's values.
    """
    path = "save_event_action_forms"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if 'action' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "action".')

        if 'event' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "event".')

        if 'values' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "values".')

        action_type = args["action"]
        event_key = args["event"]
        values = args["values"]

        # Get action's data.
        action = EVENT_ACTION_SET.get(action_type)
        if not action:
            raise MudderyError(ERR.no_table, "Can not find action: %s" % action_type)

        table_name = action.model_name

        # Remove old records.
        data_edit.delete_records(table_name, event_key=event_key)

        # Add new data.
        for value in values:
            data_edit.save_form(value, table_name)

        return success_response("success")


class QueryObjectForm(BaseRequestProcesser):
    """
    Query a record of an object which may include several tables.

    Args:
        base_typeclass: (string) candidate typeclass name
        obj_typeclass: (string, optional) object's typeclass name
        obj_key: (string, optional) object's key. If it is empty, get a new object.
    """
    path = "query_object_form"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if 'base_typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "base_typeclass".')

        base_typeclass = args["base_typeclass"]
        obj_typeclass = args.get('obj_typeclass', None)
        obj_key = args.get('obj_key', None)

        data = data_edit.query_object_form(base_typeclass, obj_typeclass, obj_key)
        return success_response(data)


class QueryMap(BaseRequestProcesser):
    """
    Query the map of an area

    Args:
        area: (string) area's key
    """
    path = "query_map"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if 'area' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "area".')

        area_key = args["area"]

        data = data_query.query_map(area_key)
        return success_response(data)


class SaveObjectForm(BaseRequestProcesser):
    """
    Save a form.

    Args:
        tables: (list) a list of table data.
               [{
                 "table": (string) table's name.
                 "values": (string, optional) record's value.
                }]
        base_typeclass: (string) candidate typeclass name
        obj_typeclass: (string) object's typeclass name
        obj_key: (string) object's key. If it is empty or different from the current object's key, get a new object.
    """
    path = "save_object_form"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if 'tables' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "tables".')

        if 'base_typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "base_typeclass".')

        if 'obj_typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "obj_typeclass".')

        if 'obj_key' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "obj_key".')

        tables = args["tables"]
        base_typeclass = args["base_typeclass"]
        obj_typeclass = args["obj_typeclass"]
        obj_key = args["obj_key"]

        new_key = data_edit.save_object_form(tables, obj_typeclass, obj_key)
        if obj_key != new_key:
            data_edit.update_object_key(obj_typeclass, obj_key, new_key)

        return success_response(new_key)


class AddArea(BaseRequestProcesser):
    """
    Save a new area.

    Args:
        typeclass: (string) the area's typeclass.
        width: (number, optional) the area's width.
        height: (number, optional) the area's height.
    """
    path = "add_area"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if 'typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "typeclass".')

        typeclass = args["typeclass"]
        width = args.get("width", 0)
        height = args.get("height", 0)

        forms = data_edit.query_object_form(typeclass, typeclass, None)
        new_area = []
        for form in forms:
            values = {field["name"]: field["value"] for field in form["fields"] if "value" in field}
            values["width"] = width
            values["height"] = height

            new_area.append({
                "table": form["table"],
                "values": values
            })

        obj_key = data_edit.save_object_form(new_area, typeclass, "")
        data = {"key": obj_key,
                "width": width,
                "height": height}
        return success_response(data)


class AddRoom(BaseRequestProcesser):
    """
    Save a new room.

    Args:
        typeclass: (string) room's typeclass.
        area: (string) room's area.
        position: (string) room's position string.
    """
    path = "add_room"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if 'typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "typeclass".')

        if 'location' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "location".')

        typeclass = args["typeclass"]
        location = args["location"]
        position = args.get("position", None)
        if position:
            position = json.dumps(position)

        forms = data_edit.query_object_form(typeclass, typeclass, None)
        new_room = []
        for form in forms:
            values = {field["name"]: field["value"] for field in form["fields"] if "value" in field}
            values["location"] = location
            values["position"] = position

            new_room.append({
                "table": form["table"],
                "values": values
            })

        obj_key = data_edit.save_object_form(new_room, typeclass, "")
        data = {"key": obj_key}
        return success_response(data)


class DeleteObjects(BaseRequestProcesser):
    """
    Delete a list of objects

    Args:
        objects: (list) a list of exit keys.
    """
    path = "delete_objects"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if "objects" not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "objects".')

        objects = args["objects"]

        for object_key in objects:
            data_edit.delete_object(object_key)

        return success_response("success")


class AddExit(BaseRequestProcesser):
    """
    Save a new exit.

    Args:
        typeclass: (string) the exit's typeclass.
        location: (string) exit's location.
        destination: (string) exit's destination.
    """
    path = "add_exit"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if 'typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "typeclass".')

        if 'location' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "location".')

        if 'destination' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "destination".')

        typeclass = args["typeclass"]
        location = args["location"]
        destination = args["destination"]

        forms = data_edit.query_object_form(typeclass, typeclass, None)
        new_exit = []
        for form in forms:
            values = {field["name"]: field["value"] for field in form["fields"] if "value" in field}
            values["location"] = location
            values["destination"] = destination

            new_exit.append({
                "table": form["table"],
                "values": values
            })

        obj_key = data_edit.save_object_form(new_exit, typeclass, "")
        data = {"key": obj_key}
        return success_response(data)


class SaveMap(BaseRequestProcesser):
    """
    Save a map.

    Args:
        area: (dict) area's data
              {
                   "key": (string) area's key
                   "background": (string) area's background
                   "width": (number) area's width
                   "height": (number) area's height
              }
        rooms: (dict) rooms positions.
                {
                    "key": (string) room's key
                    "position": (list) room's position
                }
    """
    path = "save_map_positions"
    name = ""

    def func(self, args, request):
        if not args:
            raise MudderyError(ERR.missing_args, 'Missing arguments.')

        if 'area' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "area".')

        if 'rooms' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "rooms".')

        area = args["area"]
        rooms = args["rooms"]

        data = data_edit.save_map_positions(area, rooms)
        return success_response(data)


class DeleteRecord(BaseRequestProcesser):
    """
    Delete a record.

    Args:
        table: (string) table's name.
        record: (string) record's id.
    """
    path = "delete_record"
    name = ""

    def func(self, args, request):
        if 'table' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "table".')

        if 'record' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "record".')

        table_name = args["table"]
        record_id = args["record"]

        data_edit.delete_record(table_name, record_id)
        data = {"record": record_id}
        return success_response(data)


class DeleteObject(BaseRequestProcesser):
    """
    Delete an object.

    Args:
        obj_key: (string) object's key.
        base_typeclass: (string, optional) object's base typeclass. Delete all records in all tables under this typeclass.
                        If its empty, get the typeclass of the object.
    """
    path = "delete_object"
    name = ""

    def func(self, args, request):
        if 'obj_key' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "obj_key".')

        if 'base_typeclass' not in args:
            raise MudderyError(ERR.missing_args, 'Missing the argument: "base_typeclass".')

        obj_key = args["obj_key"]
        base_typeclass = args.get("base_typeclass", None)

        data_edit.delete_object(obj_key, base_typeclass)
        data = {"obj_key": obj_key}
        return success_response(data)


class QueryTables(BaseRequestProcesser):
    """
    Query all tables' names.

    Args:
        None
    """
    path = "query_tables"
    name = ""

    def func(self, args, request):
        data = general_query.query_tables()
        return success_response(data)


class ApplyChanges(BaseRequestProcesser):
    """
    Query all tables' names.

    Args:
        None.
    """
    path = "apply_changes"
    name = ""

    def func(self, args, request):
        try:
            # reload system data
            # import_syetem_data()

            # reload localized strings
            # LOCALIZED_STRINGS_HANDLER.reload()

            # reload data
            WorldData.reload()

            # rebuild the world
            build_all()

            # restart the server
            SESSIONS.announce_all("Server restarting ...")
            SESSIONS.portal_restart_server()
        except Exception as e:
            message = "Can not build the world: %s" % e
            logger.log_tracemsg(message)
            raise MudderyError(ERR.build_world_error, message)

        return success_response("success")
