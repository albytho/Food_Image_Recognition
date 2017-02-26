from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from nutritionix import Nutritionix
nix = Nutritionix(app_id="43833828", api_key="ca216d8b1580d9e6dc9bf7853dce8a81")
import json


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
            flag = 0
            
            msg = ""
            if command == "iam":
                self.name = content
                msg = self.name + " has joined"
            
            #elif command == "msg":
            #    msg = self.name + ": " + content
            #    print msg
            
            elif command == "nix":
                res = []
                temp = nix.search(content).json()
                for i in temp['hits']:
                    for key, value in i['fields'].iteritems():
                        if (key == "item_id"):
                            index = [];
                            for key2, value2 in nix.item(id=value).json().iteritems():
                                if (key2 == "nf_calories_from_fat" or key2 == "nf_calcium_dv" \
                                    or key2 == "nf_cholesterol" or key2 == "nf_iron_dv" \
                                    or key2 == "nf_vitamin_c_dv" or key2 == "nf_sugars" \
                                    or key2 == "nf_total_fat" or key2 == "nf_total_carbohydrate" \
                                    or key2 == "nf_protein" or key2 == "nf_calories" \
                                    or key2 == "nf_vitamin_a_dv" or key2 == "nf_sodium"):
                                    if ((key2 == "nf_calories" or key2 == "nf_total_carbohydrate" or key2 == "nf_vitamin_c_dv" or key2 == "nf_vitamin_a_dv") and flag < 4):
                                        msg += str(value2) + ","
                                        print key2, ", ", value2
                                        flag += 1
                                    #print key2, ", ", value2
                                    #index.append((key2, value2))
                            #if len(index) > 0:
                                #res.append(index)
                    #print '\n'
                #print res

            for c in self.factory.clients:
                message(c, msg)
            

            


def message(self, message):
    self.transport.write(message + '\n')


factory = Factory()
factory.protocol = IphoneChat
factory.clients = []

reactor.listenTCP(81, factory)
print "Iphone Chat server started"
reactor.run()
