from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict, NewType

from ..v import IGN, GID
from ..enloneexception import PyEnlOneNotImplementedException
from .task import Task, TaskType, TaskID, _fix_task_params, LatLng

OpID = NewType("OpID", int)
Draw = NewType("Draw", str)
Arcs = NewType("Arcs", str)
Bookmark = NewType("Bookmark", str)
Linkplan = NewType("Linkplan", str)
Keyplan = NewType("Keyplan", str)


def _fix_op_params(params):
    if "type" in params:
        params["type"] = params["type"].value
    if "start" in params:
        params["start"] = params["start"].timestamp() * 1000
    if "end" in params:
        params["end"] = params["end"].timestamp() * 1000
    if "agent_draw" in params:
        params["agentDraw"] = params["agent_draw"]
    if "display_order" in params:
        params["displayOrder"] = params["display_order"]
    if "status_tag" in params:
        params["statusTag"] = params["status_tag"]


class OpType(Enum):
    FIELD = "field"
    FIELD_DEFENSE = "field-defense"
    AREA = "area"
    LINKSTAR = "linkstar"
    LINKART = "linkart"
    OTHER = "other"


class Operation:
    """
    A Tasks API operation. Don't create operations manually, get them with
        Tasks.new_operation
        Tasks.get_operations
        Tasks.search_operations
    """
    def __init__(self, proxy, api_result):
        """
        Don't create operations using this contructor, use Tasks.new_operation
        """
        self._proxy = proxy
        self._api_repr = api_result

    def __eq__(self, other):
        return self.id == other.id

    @property
    def id(self) -> int:
        """
        ID of the Operation.
        """
        return OpID(self._api_repr["id"])

    @property
    def name(self) -> Optional[str]:
        """
        Name of the Operation.
        """
        return self._api_repr["name"]

    @name.setter
    def name(self, value: str):
        self._api_repr["name"] = value

    @property
    def owner(self) -> IGN:
        """
        Owner of the operation.
        """
        return GID(self._api_repr["owner"])

    @property
    def start(self) -> datetime:
        """
        When the operations starts.
        """
        return datetime.fromtimestamp(self._api_repr["start"] / 1000)

    @start.setter
    def start(self, value: datetime):
        self._api_repr["start"] = value.timestamp() * 1000

    @property
    def end(self) -> Optional[datetime]:
        """
        When the operations ends.
        """
        if "end" in self._api_repr:
            return datetime.fromtimestamp(self._api_repr["end"] / 1000)
        else:
            return None

    @end.setter
    def end(self, value: datetime):
        self._api_repr["end"] = value.timestamp() * 1000

    @property
    def type(self) -> OpType:
        """
        What kind of operation.
        """
        return OpType(self._api_repr["type"])

    @type.setter
    def type(self, value: OpType):
        self._api_repr["type"] = value.value

    @property
    def agent_draw(self) -> Draw:
        """
        A draw for that operation that is visible to all agents
        with read access.
        """
        if "agentDraw" in self._api_repr:
            return Draw(self._api_repr["agentDraw"])
        else:
            return None

    @agent_draw.setter
    def agent_draw(self, value: Draw):
        self._api_repr["agentDraw"] = value

    @property
    def draw(self) -> Draw:
        """
         The draw for that operation. Only visible to Owner and Operator!
        """
        if "draw" in self._api_repr:
            return Draw(self._api_repr["draw"])
        else:
            return None

    @draw.setter
    def draw(self, value: Draw):
        self._api_repr["draw"] = value

    @property
    def arcs(self) -> Arcs:
        """
         The arcs for this operation. Only visible to Owner and Operator!
         (I guess?)
        """
        if "arcs" in self._api_repr:
            return Arcs(self._api_repr["arcs"])
        else:
            return None

    @property
    def bookmark(self) -> Bookmark:
        """
         The bookmarks for this operation. Only visible to Owner and Operator!
        """
        if "bookmark" in self._api_repr:
            return Bookmark(self._api_repr["bookmark"])
        else:
            return None

    @bookmark.setter
    def bookmark(self, value: Bookmark):
        self._api_repr["boorkmark"] = value

    @property
    def linkplan(self) -> Linkplan:
        """
         The draw for that operation. Only visible to Owner and Operator!
        """
        if "linkplan" in self._api_repr:
            return Linkplan(self._api_repr["linkplan"])
        else:
            return None

    @linkplan.setter
    def linkplan(self, value: Linkplan):
        self._api_repr["linkplan"] = value

    @property
    def keyplan(self) -> Keyplan:
        """
         The keyplan for that operation. Only visible to Owner and Operator!
        """
        if "keyplan" in self._api_repr:
            return Keyplan(self._api_repr["keyplan"])
        else:
            return None

    @keyplan.setter
    def keyplan(self, value: Keyplan):
        self._api_repr["keyplan"] = value

    @property
    def opsbf_settings(self) -> str:
        """
         OPSBF Settings for that operation. Only visible to Owner and Operator!
        """
        if "opsbf_settings" in self._api_repr:
            return self._api_repr["opsbf_settings"]
        else:
            return None

    @opsbf_settings.setter
    def opsbf_settings(self, value):
        self._api_repr["opsbf_settings"] = value

    @property
    def opsbf_save(self) -> str:
        """
         OPSBF Save for that operation. Only visible to Owner and Operator!
        """
        if "opsbf_save" in self._api_repr:
            return self._api_repr["opsbf_save"]
        else:
            return None

    @opsbf_save.setter
    def opsbf_save(self, value):
        self._api_repr["opsbf_save"] = value

    @property
    def other(self) -> Dict:
        """
         More data regarding that operation. A dictionaryself.
         You can store whatever you want. Only visible to
         Owner and Operator!
        """
        if "other" in self._api_repr:
            return self._api_repr["other"]
        else:
            return None

    @other.setter
    def other(self, value: Dict):
        self._api_repr["other"] = value

    @property
    def display_order(self) -> List:
        """
         Array of task IDs as integers to indicate the order the tasks should
         be displayed in clients.
        """
        if "displayOrder" in self._api_repr:
            return self._api_repr["displayOrder"]
        else:
            return None

    @display_order.setter
    def display_order(self, value: List[TaskID]):
        self._api_repr["displayOrder"] = value

    @property
    def glympse(self) -> str:
        """
         The glympse tag for that operation, can be presented on client as a
         link to app: http://glympse.com/!your_group_name
         (always starts with !).
        """
        if "glympse" in self._api_repr:
            return self._api_repr["glympse"]
        else:
            return None

    @glympse.setter
    def glympse(self, value: str):
        self._api_repr["glympse"] = value

    @property
    def status_tag(self) -> str:
        """
         The tag for that operation, to share location in this operation.
        """
        if "statusTag" in self._api_repr:
            return self._api_repr["statusTag"]
        else:
            return None

    @status_tag.setter
    def status_tag(self, value: str):
        self._api_repr["statusTag"] = value

    @property
    def ne(self) -> LatLng:
        """
         Area Management - the Box defining the area.
        """
        if "ne" in self._api_repr:
            return LatLng(self._api_repr["ne"])
        else:
            return None

    @ne.setter
    def ne(self, value: LatLng):
        self._api_repr["ne"] = value

    @property
    def nw(self) -> LatLng:
        """
         Area Management - the Box defining the area.
        """
        if "nw" in self._api_repr:
            return LatLng(self._api_repr["nw"])
        else:
            return None

    @nw.setter
    def nw(self, value: LatLng):
        self._api_repr["nw"] = value

    @property
    def se(self) -> LatLng:
        """
         Area Management - the Box defining the area.
        """
        if "se" in self._api_repr:
            return LatLng(self._api_repr["se"])
        else:
            return None

    @se.setter
    def se(self, value: LatLng):
        self._api_repr["se"] = value

    @property
    def sw(self) -> LatLng:
        """
         Area Management - the Box defining the area.
        """
        if "sw" in self._api_repr:
            return LatLng(self._api_repr["sw"])
        else:
            return None

    @nw.setter
    def nw(self, value: LatLng):
        self._api_repr["nw"] = value

    def _base_url(self):
        return "/op/" + str(self.id)

    def save(self):
        """
        Save all changes to Tasks server.
        """
        self._proxy.put(self._base_url(), self._api_repr)

    def update(self):
        """
        Update data from Tasks servers.
        """
        self._api_repr = self._proxy.get(self._base_url())

    def delete(self):
        """
        Delete this operation.
        Also deletes all tasks, messages and grants.
        """
        self._proxy.delete(self._base_url())

    def new_task(self, name: str, lat: float, lon: float, todo: TaskType,
                 **params) -> Task:
        """
        Add a new task.
        Requires parameters are location and type.
        Aditional initializing parameters can be set in keyword arguments.
        """
        params["name"] = name
        params["lat"] = lat
        params["lon"] = lon
        params["todo"] = todo
        _fix_task_params(params)
        api_res = self._proxy.post(self._base_url() + "/task", params)
        return Task(self._proxy, api_res)

    def bulk_new_task(self, tasks: List[Dict]) -> List[Task]:
        """
        Bulk add new tasks.
        Parameter is a list of dictionaries with the parameters of each task.
        Each one must have al least lat, lon, type and name.
        """
        raise PyEnlOneNotImplementedException

        for task in tasks:
            _fix_task_params(task)
        return [Task(self._proxy, api_res) for api_res
                in self._proxy.post(self._base_url() + "/task", tasks)]

    def get_task(self, id):
        """
        Retrieve specific task.
        """
        return Task(self._proxy,
                    self._proxy.get(self._base_url() + "/task/" + str(id))[0])

    def get_tasks(self, **filters) -> List[Task]:
        """
        Retrieve all task of this operation the user can see.
        Aditional search filters can be queried using the keyword arguments.
        """
        _fix_task_params(filters)
        return [Task(self._proxy, api_res) for api_res
                in self._proxy.get(self._base_url() + "/task")]

    def grant(self, grant: dict):
        """
        Grant permission.
        """
        self._proxy.post(self._base_url() + "/grant", grant)

    def remove_grant(self, grant: dict):
        """
        Remove grant.
        """
        self._proxy.delete(self._base_url() + "/grant", grant)

    def get_grants(self) -> List[dict]:
        """
        Retrieve all grants on this op.
        """
        return self._proxy.get(self._base_url() + "/grant")

    def my_grants(self) -> List[dict]:
        """
        Retrieve all grants applicable to this user.
        """
        return self._proxy.get(self._base_url() + "/permissions")

    def send_message(self, msg: dict):
        """
        Post new message to the op-chat.
        """
        return self._proxy.post(self._base_url() + "/messages", msg)

    def get_message(self, message_id):
        """
        Retrieve a specific message.
        """
        return self._proxy.get(self._base_url()
                               + "/messages/"
                               + str(message_id))

    def edit_message(self, message_id, edit):
        return self._proxy.put(self._base_url()
                               + "/messages/"
                               + str(message_id),
                               edit)

    def get_messages(self, offset=0):
        """
        Retrieve up to 50 messages, add offset to query more
        """
        return self._proxy.get(self._base_url() + "/messages")

    def get_users(self):
        """
        Returns Array of agents with permissions.
        """
        return self._proxy.get(self._base_url() + "/users")

    def sync_rocks_community(self, key):
        """
        For rocks community webhooks.
        """
        return self._proxy.get(self._base_url() + "/syncRocksComm/" + str(key))
