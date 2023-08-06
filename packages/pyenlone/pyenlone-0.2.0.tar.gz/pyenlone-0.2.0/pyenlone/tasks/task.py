from datetime import datetime
from enum import Enum
from typing import Optional, List, NewType, Union

from ..v import GID

OpID = NewType("OpID", int)
TaskID = NewType("TaskID", int)
PortalID = NewType("PortalID", str)
LatLng = NewType("LatLng", str)


def _fix_task_params(params):
    if "todo" in params:
        params["todo"] = params["todo"].value
    if "portal_id" in params:
        params["portalID"] = params["portal_id"]
    if "link_target" in params:
        params["linkTarget"] = params["link_target"]
    if "linkTarget" in params:
        params["linkTarget"] = params["linkTarget"].to_api()
    if "group_name" in params:
        params["groupName"] = params["group_name"]
    if "portal_image" in params:
        params["portalImage"] = params["portal_image"]
    if "start" in params:
        params["start"] = params["start"].timestamp() * 1000
    if "end" in params:
        params["end"] = params["end"].timestamp() * 1000
    if "created_at" in params:
        params["createdAt"] = params["created_at"]
    if "createdAt" in params:
        params["createdAt"] = params["createdAt"].timestamp() * 1000
    if "updated_at" in params:
        params["createdAt"] = params["updated_at"]
    if "updatedAt" in params:
        params["updatedAt"] = params["updatedAt"].timestamp() * 1000


class LinkTarget:
    def __init__(self, name: str, portal_id: PortalID, lat: float, lon: float):
        self.name = name
        self.portal_id = portal_id
        self.lat = lat
        self.lon = lon

    def to_api(self):
        return {
            "name": self.name,
            "portalID": self.portalID,
            "lat": self.lat,
            "lon": self.lon
        }


class TaskType(Enum):
    DESTROY = 1
    CAPTRURE = 2
    FLIP = 4
    LINK = 8
    KEYFARM = 9
    MEET = 10
    RECHARGE = 11
    UPGRADE = 12
    OTHER = 99


class TaskStatus(Enum):
    PENDING = "pending"
    ACKNOWLEDGE = "acknowledge"
    DONE = "done"


class Task:
    def __init__(self, proxy, api_result):
        """
        Don't create tasks using this contructor, use Operation.new_task
        """
        self._proxy = proxy
        self._api_repr = api_result

    def __eq__(self, other):
        return self.id == other.id

    @property
    def id(self) -> TaskID:
        """
         Id of this task. Unique inside of an operation.
        """
        return self._api_repr["id"]

    @property
    def op(self) -> OpID:
        """
         ID of the Operation this task belongs to.
        """
        return self._api_repr["op"]

    @property
    def name(self) -> Optional[str]:
        """
         Name of that task.
        """
        return self._api_repr.get("name")

    @name.setter
    def name(self, value: str):
        self._api_repr["name"] = value

    @property
    def owner(self) -> GID:
        """
         Google ID.
        """
        return self._api_repr["owner"]

    @property
    def lat(self) -> float:
        """
        Latitude.
        """
        return self._api_repr["lat"]

    @lat.setter
    def lat(self, value: float):
        self._api_repr["lat"] = value

    @property
    def lon(self) -> float:
        """
        Longitude.
        """
        return self._api_repr["lon"]

    @lon.setter
    def lon(self, value: float):
        self._api_repr["lon"] = value

    @property
    def portal(self) -> Optional[str]:
        """
         Name of the Portal targeted in the task.
        """
        return self._api_repr.get("portal")

    @portal.setter
    def portal(self, value: str):
        self._api_repr["portal"] = value

    @property
    def portal_id(self) -> Optional[PortalID]:
        """
         ID (guid) of the Portal targeted in the task.
        """
        if "portalID" in self._api_repr:
            return PortalID(self._api_repr["portalID"])
        else:
            return None

    @portal_id.setter
    def portal_id(self, value: PortalID):
        self._api_repr["portalID"] = value

    @property
    def start(self) -> datetime:
        """
        The date and Time when it starts.
        """
        return datetime.fromtimestamp(self._api_repr["start"] / 1000)

    @start.setter
    def start(self, value: datetime):
        self._api_repr["start"] = value.timestamp() * 1000

    @property
    def end(self) -> Optional[datetime]:
        """
        The date and Time when it ends.
        """
        if "end" in self._api_repr:
            return datetime.fromtimestamp(self._api_repr["end"] / 1000)
        else:
            return None

    @end.setter
    def end(self, value: datetime):
        self._api_repr["end"] = value.timestamp() * 1000

    @property
    def comment(self) -> Optional[str]:
        """
         A comment for the agent to read.
        """
        return self._api_repr.get("comment")

    @comment.setter
    def comment(self, value):
        self._api_repr["comment"] = value

    @property
    def previous(self) -> Optional[TaskID]:
        """
         If this task needs another task to be completed before.
        """
        if "previous" in self._api_repr:
            return TaskID(self._api_repr["previous"])
        else:
            return None

    @previous.setter
    def previous(self, value: TaskID):
        self._api_repr["previous"] = value

    @property
    def alternative(self) -> Optional[TaskID]:
        """
         If this task is an alternative to another task.
        """
        if "alternative" in self._api_repr:
            return TaskID(self._api_repr["alternative"])
        else:
            return None

    @alternative.setter
    def alternative(self, value: TaskID):
        self._api_repr["alternative"] = value

    @property
    def priority(self) -> Optional[int]:
        """
         How important this task is (1 is most important).
        """
        return self._api_repr.get("priority")

    @priority.setter
    def priority(self, value: TaskID):
        self._api_repr["priority"] = value

    @property
    def repeat(self) -> Optional[int]:
        """
         How often should this task be done?
        """
        return self._api_repr.get("repeat")

    @repeat.setter
    def repeat(self, value: int):
        self._api_repr["repeat"] = value

    @property
    def todo(self) -> TaskType:
        """
         What should be done?
        """
        if "todo" in self._api_repr:
            return TaskType(self._api_repr["todo"])
        else:
            return None

    @todo.setter
    def todo(self, value: TaskType):
        self._api_repr["todo"] = value.value

    @property
    def link_target(self) -> Optional[List[LinkTarget]]:  # CHECKEAR
        """
         For LINK type tasks.
         It's a list of LinkTarget, but you can set it with a single one and
         it will be casted to list.
        """
        if "linkTarget" not in self._api_repr:
            return None
        if type(self._api_repr["linkTarget"]) is list:
            return [LinkTarget(lt["name"],
                               lt["portalID"],
                               lt["lat"],
                               lt["lon"])
                    for lt in self._api_repr["linkTarget"]]
        if type(self._api_repr["linkTarget"]) is dict:
            lt = self._api_repr["linkTarget"]
            return [LinkTarget(lt["name"],
                               lt["portalID"],
                               lt["lat"],
                               lt["lon"])]

    @link_target.setter
    def link_target(self, value: Union[LinkTarget, List[LinkTarget]]):
        if type(value) is LinkTarget:
            self._api_repr["linkTarget"] = value.to_api()
        if type(value) is list:
            self._api_repr["linkTarget"] = [va.to_api() for va in value]

    @property
    def created_at(self) -> datetime:
        """
         When it was created.
        """
        return datetime.fromtimestamp(self._api_repr["createdAt"] / 1000)

    @property
    def updated_at(self) -> datetime:
        """
         When it was updated.
        """
        return datetime.fromtimestamp(self._api_repr["updatedAt"] / 1000)

    @property
    def accepted(self):
        """
         Who accepted this task.
        """
        return self._api_repr.get("accepted")

    @accepted.setter
    def accepted(self, value):
        self._api_repr["accepted"] = value

    @property
    def assigned(self):
        """
        If that task is assigned to a single agent.
        """
        return self._api_repr.get("assigned")

    @assigned.setter
    def assigned(self, value):
        self._api_repr["assigned"] = value

    @property
    def done(self) -> Optional[List]:  # CHECKEAR
        """
         Who completed this task.
        """
        return self._api_repr.get("done")

    @done.setter
    def done(self, value):
        self._api_repr["done"] = value

    @property
    def group_name(self) -> Optional[str]:
        """
         If that task meant for a group of agents.
        """
        return self._api_repr.get("groupName")

    @group_name.setter
    def group_name(self, value: str):
        self._api_repr["groupName"] = value

    @property
    def status(self) -> TaskStatus:
        """
        TaskStatus of this task. Set by backend for specific actions.
        PENDING after creation.
        ACKNOWLEDGE after the task was accepted by an agent and current status
        was pending.
        DONE after the task was marked as done.
        """
        return TaskStatus(self._api_repr["status"])

    @property
    def portal_image(self) -> str:
        """
         Image url for portal.
        """
        return self._api_repr.get("portalImage")

    @portal_image.setter
    def portal_image(self, value: str):
        self._api_repr["portalImage"] = value

    @property
    def portal_init_state(self) -> dict:
        """
        Dicttionary describing the state of the portal when the task was
        created.
        I was to lazy to define classes for this.
        """
        return self._api_repr["portalInitState"]

    @portal_init_state.setter
    def portal_init_state(self, value: dict):
        self._api_repr["portalInitState"] = value

    @property
    def latlng_string(self) -> LatLng:
        return str(self.lat) + "," + str(self.lon)

    @property
    def maps_link(self):
        return u"https://maps.google.com/maps?ll=" \
               + self.latlng_string + "&q=" + self.latlng_string

    @property
    def intel_link(self):
        return u"https://intel.ingress.com/intel?ll=" \
               + self.latlng_string + "&z=17&pll=" + self.latlng_string

    def _base_url(self):
        return "/op/" + str(self.op) + "/task/" + str(self.id)

    def save(self):
        """
        Save changes to Tasks server.
        """
        self._proxy.put(self._base_url(), self._api_repr)

    def update(self):
        """
        Update data from Tasks servers.
        """
        self._api_repr = self._proxy.get(self._base_url())[0]

    def delete(self):
        """
        Delete this task.
        Also deletes task specific grants.
        """
        self._proxy.delete(self._base_url())

    def grant(self, grant: dict):
        """
        Grant permission.
        """
        self._proxy.post(self._base_url() + "/grant", grant)

    def remove_grant(self, grant):
        """
        Remove grant.
        """
        self._proxy.delete(self._base_url() + "/grant", grant)

    def get_grants(self):
        """
        Retrieve all grants on this task.
        """
        return self._proxy.get(self._base_url() + "/grant")

    def my_grants(self):
        """
        Retrieve all grants applicable to this user.
        """
        return self._proxy.get(self._base_url() + "/permissions")

    def accept(self):
        """
        User accepts this task.
        """
        self._proxy.post(self._base_url() + "/acknowledge", {})

    def decline(self):
        """
        User who accepted this task declines it afterwards.
        """
        self._proxy.delete(self._base_url() + "/acknowledge")

    def assign(self, who: dict):
        """
        Assign this task to a user or list of users.
        """
        self._proxy.post(self._base_url() + "/assigned", who)

    def unassign(self):
        """
        Unassign task.
        """
        self._proxy.delete(self._base_url() + "/assigned")

    def complete(self):
        """
        User has completed this task.
        """
        self._proxy.post(self._base_url() + "/complete", {})

    def get_complete(self):
        """
        User who completed this task.
        """
        return self._proxy.get(self._base_url() + "/complete")

    def get_acknowledge(self):
        """
        User who accepted this task.
        """
        return self._proxy.get(self._base_url() + "/acknowledge")

    def get_assigned(self):
        """
        "User who were assigned to this task."
        """
        return self._proxy.get(self._base_url() + "/assigned")
