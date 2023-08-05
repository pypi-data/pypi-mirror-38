from .base_class import DynamicRobotApiClass
from robot.api.deco import keyword
from furl import furl


class SalabsUtils(DynamicRobotApiClass):
    def __init__(self):
        pass

    @keyword("Add Basic Authentication To Url")
    def add_authentication(self, url, l, p):
        data = furl(url)
        data.username = l
        data.password = p
        return data.tostr()
