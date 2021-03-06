
from myne.plugins import ProtocolPlugin
from myne.decorators import *
from myne.constants import *

class NickPlugin(ProtocolPlugin):
    
    commands = {
        "nick": "commandNick",
    }
    
    @admin_only
    def commandNick(self, params):
        "/nick - Changes your username and skin. Use with great care."
        if len(params) < 1:
            self.client.sendServerMessage("Please enter a username.")
        else:
            username = params[1]
            if username in self.client.factory.usernames:
                self.client.sendServerMessage("Someone is using that username on this server.")
            else:
                old_username, self.client.username = self.client.username, username
                self.client.factory.usernames[username] = self.client.factory.usernames[old_username]
                del self.client.factory.usernames[old_username]
                self.client.respawn()
    