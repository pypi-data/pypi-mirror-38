"""
"""


class DynamicRobotApiClass():
    """
    Base class for exposing dynamic api for Robot Framework
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def get_keyword_names(self):
        """Robot Framework dynamic API keyword collector."""
        return [name for name in dir(self) if hasattr(getattr(self, name), 'robot_name')]
