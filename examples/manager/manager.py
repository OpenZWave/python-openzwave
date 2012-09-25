"""
simpler manager API using louie for callbacks
"""
import openzwave
from louie import dispatcher

class Manager(object):
    def __init__(self, device='/dev/keyspan-2', configDir="openzwave/config/"):
        """
        calls will fail until the homeid is known. You may have to retry them.
        """
        self.options = openzwave.PyOptions()

        # Specify the open-zwave config path here
        self.options.create(configDir,"","")
        self.options.lock()

        self.manager = openzwave.PyManager()
        self.manager.create()

        self._homeId = None

        self.manager.addWatcher(self.callback)
        self.manager.addDriver(device)

    @property
    def homeId(self):
        if self._homeId is None:
            raise ValueError("haven't received a homeId yet")
        return self._homeId

    def callback(self, n):
        self._homeId = n['homeId']
        dispatcher.send(n['type'], **n['valueId'])

    def getNodes(self):
        # there is a point during startup that this will return many
        # wrong nodes, but then it settles down to the right
        # number. I'm not sure how to filter out that bad window
        base = self.manager.getControllerNodeId(self.homeId)
        return [Node._init(self, i) for i in
                self.manager.getNodeNeighbors(self.homeId, base)]

class Node(object):
    @classmethod
    def _init(cls, manager, nodeId):
        new = cls()
        new.manager = manager
        new.nodeId = nodeId

        for name in '''refreshNodeInfo requestNodeState isNodeListeningDevice
          isNodeRoutingDevice getNodeMaxBaudRate getNodeVersion
          getNodeSecurity getNodeBasic getNodeGeneric getNodeSpecific
          getNodeType getNodeManufacturerName getNodeProductName
          getNodeName getNodeLocation getNodeManufacturerId
          getNodeProductType getNodeProductId'''.split():
            meth = getattr(manager.manager, name)
            setattr(new, name,
                    lambda meth=meth: meth(new.manager.homeId, new.nodeId))
        
        return new

    def __repr__(self):
        return "<Node %s, id=%s>" % (self.getNodeProductName(), self.nodeId)

    def setLevel(self, level):
        """
         Sets the basic level of a node
         
         This is a helper method to simplify basic control of a node.
         It is the equivalent of changing the value reported by the
         nodes Basic command class and will generate a ValueChanged
         notification from that class.
         
         @param level The level to set the node.  Valid values are
         0-99 and 255.  Zero is off and 99 is fully on.  255 will turn
         on the device at its last known level (if supported).

        """
        self.manager.manager.setNodeLevel(self.manager.homeId, self.nodeId, level)

    def getLevel(self):
        pass # todo: watch for notifications to this node
        
