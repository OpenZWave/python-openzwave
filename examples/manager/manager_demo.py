from louie import dispatcher, All
import manager
m = manager.Manager(configDir="localconfig")

def anyNotification(signal, **kw):
    # demo that prints all params of all notifications
    print "notification %s: %s" % (signal, kw)
dispatcher.connect(anyNotification, All)

def valueChanged(nodeId, label, value):
    # demo that announces value changes
    print "Value of node %s changed: %s -> %s" % (nodeId, label, value)
dispatcher.connect(valueChanged, "ValueChanged")

from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()
ipshell()
