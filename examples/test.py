import openzwave
from openzwave import PyManager

options = openzwave.PyOptions()

# Specify the open-zwave config path here
options.create("openzwave/config/","","")
options.lock()
manager = openzwave.PyManager()
manager.create()

# callback order: (notificationtype, homeid, nodeid, ValueID, groupidx, event)
def callback(args):
    print('\n%s\n[%s]:\n' % ('-'*20, args['notificationType']))
    if args:
        print('homeId: 0x%.8x' % args['homeId'])
        print('nodeId: %d' % args['nodeId'])
        v = args['valueId']
        print('valueID: %s' % v['id'])
        if v.has_key('groupIndex') and v['groupIndex'] != 0xff: print('GroupIndex: %d' % v['groupIndex'])
        if v.has_key('event') and v['event'] != 0xff: print('Event: %d' % v['event'])
        if v.has_key('value'): print('Value: %s' % str(v['value']))
        if v.has_key('label'): print('Label: %s' % v['label'])
        if v.has_key('units'): print('Units: %s' % v['units'])
        if v.has_key('readOnly'): print('ReadOnly: %s' % v['readOnly'])
    print('%s\n' % ('-'*20,))

manager.addWatcher(callback)
manager.addDriver('/dev/keyspan-2')
