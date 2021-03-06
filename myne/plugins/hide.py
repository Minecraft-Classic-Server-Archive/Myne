
import random
from myne.plugins import ProtocolPlugin
from myne.decorators import *
from myne.constants import *

class HidePlugin(ProtocolPlugin):
    
    commands = {
        "hide": "commandHide",
    }
    
    hooks = {
        "playerpos": "playerMoved",
    }
    
    def gotClient(self):
        self.hidden = False
    
    def playerMoved(self, x, y, z, h, p):
        "Stops transmission of player positions if hide is on."
        if self.hidden:
            return False
    
    @admin_only
    def commandHide(self, params):
        "/hide - Hides you so no other players can see you. Toggle."
        if not self.hidden:
            self.client.sendServerMessage("You are now hidden.")
            self.hidden = True
            # Send the "player has disconnected" command to people
            self.client.queueTask(TASK_PLAYERLEAVE, [self.client.id])
        else:
            self.client.sendServerMessage("You are now visible.")
            self.hidden = False
            # Imagine that! They've mysteriously appeared.
            self.client.queueTask(TASK_NEWPLAYER, [self.client.id, self.client.username, self.client.x, self.client.y, self.client.z, self.client.h, self.client.p])
    