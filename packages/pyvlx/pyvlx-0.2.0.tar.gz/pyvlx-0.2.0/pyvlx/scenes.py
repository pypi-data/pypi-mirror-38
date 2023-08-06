"""Module for storing and accessing scene list."""
from .scene import Scene
from .get_scene_list import GetSceneList
from .exception import PyVLXException


class Scenes():
    """Class for storing and accessing ."""

    def __init__(self, pyvlx):
        """Initialize Scenes class."""
        self.pyvlx = pyvlx
        self.__scenes = []

    def __iter__(self):
        """Iterator."""
        yield from self.__scenes

    def __getitem__(self, key):
        """Return scene by name or by index."""
        for scene in self.__scenes:
            if scene.name == key:
                return scene
        if isinstance(key, int):
            return self.__scenes[key]
        raise KeyError

    def __len__(self):
        """Return number of scenes."""
        return len(self.__scenes)

    def add(self, scene):
        """Add scene."""
        if not isinstance(scene, Scene):
            raise TypeError()
        self.__scenes.append(scene)

    async def load(self):
        """Load scenes from KLF 200."""
        get_scene_list = GetSceneList(pyvlx=self.pyvlx)
        await get_scene_list.do_api_call()
        if not get_scene_list.success:
            raise PyVLXException("Unable to retrieve scene information")
        for scene in get_scene_list.scenes:
            self.add(Scene(pyvlx=self.pyvlx, scene_id=scene[0], name=scene[1]))
