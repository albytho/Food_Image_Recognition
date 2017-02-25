from nutritionix import Nutritionix
nix = Nutritionix(app_id="7cb9887a", api_key="a4d7fd53cc8bfde145020068f99b204d")
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor


class IphoneChat(Protocol):
    def connectionMade(self):
        #self.transport.write("""connected""")
        self.factory.clients.append(self)
        print "clients are ", self.factory.clients
    
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
    
    def dataReceived(self, data):
        print "data is ", data
        a = data.split(':')
        if len(a) > 1:
            command = a[0]
            content = a[1].rstrip()
            
            msg = ""
            if command == "iam":
                self.name = content
                msg = self.name + " has joined"
            
            elif command == "msg":
                msg = self.name + ": " + content
            
            elif command == "nix":
                msg = nix.search(content)
        
            print msg
            
            for c in self.factory.clients:
                c.message(msg)

def message(self, message):
    self.transport.write(message + '\n')


factory = Factory()
factory.protocol = IphoneChat
factory.clients = []

reactor.listenTCP(80, factory)
print "Iphone Chat server started"
reactor.run()
