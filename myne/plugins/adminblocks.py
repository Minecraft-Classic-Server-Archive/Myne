
from myne.plugins import ProtocolPlugin
from myne.decorators import *
from myne.constants import *

class AdminBlocksPlugin(ProtocolPlugin):
    
    commands = {
        "solid": "commandSolid",
        "adminblocks": "commandAdminblocks",
    }
    
    hooks = {
        "blockchange": "blockChanged",
        "rankchange": "sendAdminBlockUpdate",
        "canbreakadmin": "canBreakAdminBlocks",
    }
    
    def gotClient(self):
        self.building_solid = False
    
    def blockChanged(self, x, y, z, block, selected_block):
        "Hook trigger for block changes."
        # Admincrete hack check
        if not self.canBreakAdminBlocks():
            def check_block(block):
                if ord(block) == BLOCK_GROUND_ROCK:
                    self.client.sendError("Don't build admincrete!")
                    self.client.world[x, y, z] = chr(BLOCK_AIR)
            self.client.world[x,y,z].addCallback(check_block)
        # See if they are in solid-building mode
        if self.building_solid and block == BLOCK_ROCK:
            return BLOCK_GROUND_ROCK
    
    def canBreakAdminBlocks(self):
        "Shortcut for checking permissions."
        if hasattr(self.client, "world"):
            return (not self.client.world.admin_blocks) or self.client.isOp()
        else:
            return False
    
    def sendAdminBlockUpdate(self):
        "Sends a packet that updates the client's admin-building ability"
        self.client.sendPacked(TYPE_INITIAL, 6, "Admincrete Update", "If you see this, it's a bug", self.canBreakAdminBlocks() and 100 or 0)
    
    @op_only
    @on_off_command
    def commandAdminblocks(self, onoff):
        "/adminblocks on|off - Turns on/off unbreakable admin/op blocks."
        if onoff == "on":
            self.client.world.admin_blocks = True
            self.client.sendWorldMessage("Admin blocks are now enabled here.")
            self.client.sendServerMessage("Admin Blocks on in %s" % self.client.world.id)
        else:
            self.client.world.admin_blocks = False
            self.client.sendWorldMessage("Admin blocks are now disabled here.")
            self.client.sendServerMessage("Admin Blocks off in %s" % self.client.world.id)
        for client in self.client.world.clients:
            client.sendAdminBlockUpdate()
    
    @op_only
    def commandSolid(self, parts):
        "/solid - Toggles admincrete creation."
        if self.building_solid:
            self.client.sendServerMessage("You are now placing normal rock.")
        else:
            self.client.sendServerMessage("You are now placing admin rock.")
        self.building_solid = not self.building_solid
    