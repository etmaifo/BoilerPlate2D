import sys, os
import pytmx

class LevelCreator(object):
    def __init__(self, filename):
        self.players = []
        self.blocks = []
        self.filename = filename
        self.width = 0
        self.height = 0
        self.data = ""

        self.load_assets()


    def load_assets(self):
        self.data = pytmx.TiledMap(self.filename)
        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight

        for layer in self.data.layers:
            if layer.name.upper() == "PLAYER":
                self.players = layer
                self.lifts = layer
            elif layer.name == "Blocks":
                self.blocks = layer
