# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}$

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Plugin purpose
==============

Support Z-wave technology

Implements
==========

-Zwave

@author: Nico <nico84dev@gmail.com>
@copyright: (C) 2007-2012 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

from collections import namedtuple
import binascii
import threading
import openzwave
from openzwave import PyManager
import time
from time import sleep
import os.path


# Déclaration de tuple nomée pour la clarification des infos des noeuds zwave (node)
# Juste à rajouter ici la déclaration pour future extension.
OZWPLuginVers = "0.1b"
NamedPair = namedtuple('NamedPair', ['id', 'name'])
NodeInfo = namedtuple('NodeInfo', ['generic','basic','specific','security','version'])
GroupInfo = namedtuple('GroupInfo', ['index','label','maxAssociations','members'])
# Listes de commandes Class reconnues comme device domogik
CmdsClassAvailable = ['COMMAND_CLASS_BASIC', 'COMMAND_CLASS_SWITCH_BINARY', 'COMMAND_CLASS_SENSOR_BINARY', 
                               'COMMAND_CLASS_SENSOR_MULTILEVEL', 'COMMAND_CLASS_BATTERY']
                                
                          

class OZwaveException(Exception):
    """"    Zwave Exception     """
            
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
                                
    def __str__(self):
        return repr(self.value)
                                            

class ZWaveValueNode:
    """ Représente une des valeurs du node """
    def __init__(self, homeId, nodeId, valueData):
        '''
        Initialise la valeur du node
        @param homeid: ID du réseaux home/controleur
        @param nodeid: ID du node
        @param valueData: valueId dict (voir openzwave.pyx)
            ['valueId'] = {
                    'homeId' : uint32, # Id du réseaux
                    'nodeId' : uint8,   # Numéro du noeud
                    'commandClass' : PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()], # Liste des cmd CLASS reconnues
                    'instance' : uint8  # numéro d'instance de la value 
                    'index' : uint8 # index de classement de la value
                    'id' : uint64 # Id unique de la value (Util pour AKC zwave)
                    'genre' : enum ValueGenre:   # Type de data OZW
                                ValueGenre_Basic = 0
                                ValueGenre_User = 1
                                ValueGenre_Config = 2
                                ValueGenre_System = 3
                                ValueGenre_Count = 4
                    'type' : enum ValueType:  # Type de données
                                ValueType_Bool = 0
                                ValueType_Byte = 1
                                ValueType_Decimal = 2
                                ValueType_Int = 3
                                ValueType_List = 4
                                ValueType_Schedule = 5
                                ValueType_Short = 6
                                ValueType_String = 7
                                ValueType_Button = 8
                                ValueType_Max = ValueType_Button
                                
                    'value' : str,      # Valeur même
                    'label' : str,      # Nom de la value OZW
                    'units' : str,      # unité
                    'readOnly': manager.IsValueReadOnly(v),  # Type d'accès lecture/ecriture
                    }   
        '''
        self._homeId = homeId
        self._nodeId = nodeId
        self._valueData = valueData
        self._lastUpdate = None
        
    # On accède aux attributs uniquement depuis les property
  
    homeId = property(lambda self: self._homeId)
    nodeId = property(lambda self: self._nodeId)
    lastUpdate = property(lambda self: self._lastUpdate)
    valueData = property(lambda self: self._valueData)

    def getValue(self, key):
        """Retourne la valeur du dict valueData correspondant à key"""
        return self.valueData[key] if self._valueData.has_key(key) else None
    
    def update(self, args):
        """Mise à jour de valueData depuis les arguments du callback """
        self._valueData = args['valueId']
        self._lastUpdate = time.time()

    def __str__(self):
        return 'homeId: [{0}]  nodeId: [{1}]  valueData: {2}'.format(self._homeId, self._nodeId, self._valueData)


class ZWaveNode:
    '''Représente un device (node) inclu dans le réseau Z-Wave'''

    def __init__(self, homeId, nodeId):
        '''initialise le node zwave
        @param homeid: ID du réseaux home/controleur
        @param nodeid: ID du node
        '''
        self._lastUpdate = None
        self._homeId = homeId
        self._nodeId = nodeId
        self._capabilities = set()
        self._commandClasses = set()
        self._neighbors = set()
        self._values = dict()  # voir la class ZWaveValueNode
        self._name = ''
        self._location = ''
        self._manufacturer = None
        self._product = None
        self._productType = None
        self._groups = list()
        self._sleeping = True
        
    # On accède aux attributs uniquement depuis les property
    # Chaque attribut est une propriétée qui est automatique à jour au besoin via le réseaux Zwave
    id = property(lambda self: self._nodeId)
    name = property(lambda self: self._name)
    location = property(lambda self: self._location)
    product = property(lambda self: self._product.name if self._product else '')
    productType = property(lambda self: self._productType.name if self._productType else '')
    lastUpdate = property(lambda self: self._lastUpdate)
    homeId = property(lambda self: self._homeId)
    nodeId = property(lambda self: self._nodeId)
    capabilities = property(lambda self: ', '.join(self._capabilities))
    commandClasses = property(lambda self: self._commandClasses)
    neighbors = property(lambda self:self._neighbors)
    values = property(lambda self:self._values)
    manufacturer = property(lambda self: self._manufacturer.name if self._manufacturer else '')
    groups = property(lambda self:self._groups)
    isSleeping = property(lambda self: self._sleeping)
    isLocked = property(lambda self: self._getIsLocked())
    level = property(lambda self: self._getLevel())
    isOn = property(lambda self: self._getIsOn())
    batteryLevel = property(lambda self: self._getBatteryLevel())
    signalStrength = property(lambda self: self._getSignalStrength())

    def _getIsLocked(self):
        return False

# Fonction de renvoie des valeurs des valueNode en fonction des Cmd CLASS zwave
# C'est ici qu'il faut enrichire la prise en compte des fonctions Zwave
# COMMAND_CLASS implémentées :

#        0x26: 'COMMAND_CLASS_SWITCH_MULTILEVEL',
#        0x80: 'COMMAND_CLASS_BATTERY',
#        0x25: 'COMMAND_CLASS_SWITCH_BINARY',
#        0x20: 'COMMAND_CLASS_BASIC',


# TODO:

#        0x00: 'COMMAND_CLASS_NO_OPERATION',

#        0x21: 'COMMAND_CLASS_CONTROLLER_REPLICATION',
#        0x22: 'COMMAND_CLASS_APPLICATION_STATUS',
#        0x23: 'COMMAND_CLASS_ZIP_SERVICES',
#        0x24: 'COMMAND_CLASS_ZIP_SERVER',
#        0x27: 'COMMAND_CLASS_SWITCH_ALL',
#        0x28: 'COMMAND_CLASS_SWITCH_TOGGLE_BINARY',
#        0x29: 'COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL',
#        0x2A: 'COMMAND_CLASS_CHIMNEY_FAN',
#        0x2B: 'COMMAND_CLASS_SCENE_ACTIVATION',
#        0x2C: 'COMMAND_CLASS_SCENE_ACTUATOR_CONF',
#        0x2D: 'COMMAND_CLASS_SCENE_CONTROLLER_CONF',
#        0x2E: 'COMMAND_CLASS_ZIP_CLIENT',
#        0x2F: 'COMMAND_CLASS_ZIP_ADV_SERVICES',
#        0x30: 'COMMAND_CLASS_SENSOR_BINARY',
#        0x31: 'COMMAND_CLASS_SENSOR_MULTILEVEL',
#        0x32: 'COMMAND_CLASS_METER',
#        0x33: 'COMMAND_CLASS_ZIP_ADV_SERVER',
#        0x34: 'COMMAND_CLASS_ZIP_ADV_CLIENT',
#        0x35: 'COMMAND_CLASS_METER_PULSE',
#        0x3C: 'COMMAND_CLASS_METER_TBL_CONFIG',
#        0x3D: 'COMMAND_CLASS_METER_TBL_MONITOR',
#        0x3E: 'COMMAND_CLASS_METER_TBL_PUSH',
#        0x38: 'COMMAND_CLASS_THERMOSTAT_HEATING',
#        0x40: 'COMMAND_CLASS_THERMOSTAT_MODE',
#        0x42: 'COMMAND_CLASS_THERMOSTAT_OPERATING_STATE',
#        0x43: 'COMMAND_CLASS_THERMOSTAT_SETPOINT',
#        0x44: 'COMMAND_CLASS_THERMOSTAT_FAN_MODE',
#        0x45: 'COMMAND_CLASS_THERMOSTAT_FAN_STATE',
#        0x46: 'COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE',
#        0x47: 'COMMAND_CLASS_THERMOSTAT_SETBACK',
#        0x4c: 'COMMAND_CLASS_DOOR_LOCK_LOGGING',
#        0x4E: 'COMMAND_CLASS_SCHEDULE_ENTRY_LOCK',
#        0x50: 'COMMAND_CLASS_BASIC_WINDOW_COVERING',
#        0x51: 'COMMAND_CLASS_MTP_WINDOW_COVERING',
#        0x60: 'COMMAND_CLASS_MULTI_CHANNEL_V2',
#        0x62: 'COMMAND_CLASS_DOOR_LOCK',
#        0x63: 'COMMAND_CLASS_USER_CODE',
#        0x70: 'COMMAND_CLASS_CONFIGURATION',
#        0x71: 'COMMAND_CLASS_ALARM',
#        0x72: 'COMMAND_CLASS_MANUFACTURER_SPECIFIC',
#        0x73: 'COMMAND_CLASS_POWERLEVEL',
#        0x75: 'COMMAND_CLASS_PROTECTION',
#        0x76: 'COMMAND_CLASS_LOCK',
#        0x77: 'COMMAND_CLASS_NODE_NAMING',
#        0x7A: 'COMMAND_CLASS_FIRMWARE_UPDATE_MD',
#        0x7B: 'COMMAND_CLASS_GROUPING_NAME',
#        0x7C: 'COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE',
#        0x7D: 'COMMAND_CLASS_REMOTE_ASSOCIATION',
#        0x81: 'COMMAND_CLASS_CLOCK',
#        0x82: 'COMMAND_CLASS_HAIL',
#        0x84: 'COMMAND_CLASS_WAKE_UP',
#        0x85: 'COMMAND_CLASS_ASSOCIATION',
#        0x86: 'COMMAND_CLASS_VERSION',
#        0x87: 'COMMAND_CLASS_INDICATOR',
#        0x88: 'COMMAND_CLASS_PROPRIETARY',
#        0x89: 'COMMAND_CLASS_LANGUAGE',
#        0x8A: 'COMMAND_CLASS_TIME',
#        0x8B: 'COMMAND_CLASS_TIME_PARAMETERS',
#        0x8C: 'COMMAND_CLASS_GEOGRAPHIC_LOCATION',
#        0x8D: 'COMMAND_CLASS_COMPOSITE',
#        0x8E: 'COMMAND_CLASS_MULTI_INSTANCE_ASSOCIATION',
#        0x8F: 'COMMAND_CLASS_MULTI_CMD',
#        0x90: 'COMMAND_CLASS_ENERGY_PRODUCTION',
#        0x91: 'COMMAND_CLASS_MANUFACTURER_PROPRIETARY',
#        0x92: 'COMMAND_CLASS_SCREEN_MD',
#        0x93: 'COMMAND_CLASS_SCREEN_ATTRIBUTES',
#        0x94: 'COMMAND_CLASS_SIMPLE_AV_CONTROL',
#        0x95: 'COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD',
#        0x96: 'COMMAND_CLASS_AV_RENDERER_STATUS',
#        0x97: 'COMMAND_CLASS_AV_CONTENT_SEARCH_MD',
#        0x98: 'COMMAND_CLASS_SECURITY',
#        0x99: 'COMMAND_CLASS_AV_TAGGING_MD',
#        0x9A: 'COMMAND_CLASS_IP_CONFIGURATION',
#        0x9B: 'COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION',
#        0x9C: 'COMMAND_CLASS_SENSOR_ALARM',
#        0x9D: 'COMMAND_CLASS_SILENCE_ALARM',
#        0x9E: 'COMMAND_CLASS_SENSOR_CONFIGURATION',
#        0xEF: 'COMMAND_CLASS_MARK',
#        0xF0: 'COMMAND_CLASS_NON_INTEROPERABLE'
#  

    def _getValuesForCommandClass(self, classId):
        """Optient la (les) valeur(s) pour une Cmd CLASS donnée  
        @ Param classid : Valeur hexa de la COMMAND_CLASS"""
        # extraction des valuesnode correspondante à classId, si pas reconnues par le node -> liste vide
        retval = list()
        classStr = PyManager.COMMAND_CLASS_DESC[classId]
        for value in self._values.itervalues():
            vdic = value.valueData
            if vdic and vdic.has_key('commandClass') and vdic['commandClass'] == classStr:
                retval.append(value)
        return retval

# Traitement spécifique
    def _getLevel(self):
        values = self._getValuesForCommandClass(0x26)  # COMMAND_CLASS_SWITCH_MULTILEVEL
        if values:
            for value in values:
                vdic = value.valueData
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return 0

    def _getBatteryLevel(self):
        values = self._getValuesForCommandClass(0x80)  # COMMAND_CLASS_BATTERY
        if values:
            for value in values:
                vdic = value.valueData
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return -1

    def _getSignalStrength(self):
        return 0

    def _getIsOn(self):
        values = self._getValuesForCommandClass(0x25)  # COMMAND_CLASS_SWITCH_BINARY
        if values:
            for value in values:
                vdic = value.valueData
                if vdic and vdic.has_key('type') and vdic['type'] == 'Bool' and vdic.has_key('value'):
                    return vdic['value'] == 'True'
        return False
 
    def getValuesForCommandClass(self, commandClass) :
        """Retourne les Values correspondant à la commandeClass"""
        classId = PyManager.COMMAND_CLASS_DESC.keys()[PyManager.COMMAND_CLASS_DESC.values().index(commandClass)]
        return self._getValuesForCommandClass(classId)

    def hasCommandClass(self, commandClass):
        """ Renvois les cmdClass demandées filtrées selon celles reconnues par le node """
        return commandClass in self._commandClasses

    def __str__(self):
        return 'homeId: [{0}]  nodeId: [{1}] product: {2}  name: {3}'.format(self._homeId, self._nodeId, self._product, self._name)

        # decorator?
        #self._batteryLevel = None # if COMMAND_CLASS_BATTERY
        #self._level = None # if COMMAND_CLASS_SWITCH_MULTILEVEL - maybe state? off - ramped - on?
        #self._powerLevel = None # hmm...
        # sensor multilevel?  instance/index
        # meter?
        # sensor binary?
        

class OZWavemanager(threading.Thread):
    """
    ZWave class manager
    """

    def __init__(self, config,  cb_send_xPL, cb_sendxPL_trig, stop , log,  ozwconfig = "../../../share/domogik/data/ozwave/plugins/ozwconfig/", ozwuser="",  ozwlog = False, msgEndCb =  False):
        """ Ouverture du manager py-openzwave
            @ param config : configuration du plugin pour accès aux valeurs paramètrées"
            @ param cb_send_xpl : callback pour envoi msg xpl
            @ param cb_send_trig : callback pour trig xpl
            @ param stop : flag d'arrêt du plugin         
            @ param log : log instance domogik
            @ param ozwconfig : chemin d'accès au répertoire de configuration pour la librairie openszwave (déf = "./../plugins/ozwconfig/")
            @ param ozwuser : chemin d'accès au répertoire de sauvegarde de la config openzwave et du log."
            @ param ozwlog (optionnel) : Activation du log d'openzawe, fichier OZW_Log.txt dans le répertoire user (déf = "--logging false")
            @ param msgEndCb (désactivée pour l'instant) Envoi d'une notification quand la transaction est complete (defaut = "--NotifyTransactions  false")
        """
        self._device = None
        self._configPlug=config
        self._log = log
        self._cb_send_xPL= cb_send_xPL
        self._cb_sendxPL_trig= cb_sendxPL_trig
        self._stop = stop
        self._homeId = 0
        # self._nodeid = None
        self._activeNodeId= None # node actif courant, pour utilisation dans les fonctions du manager
        self._ctrlnodeId = 0
        self._controller = None
        self._nodes = dict()
        self._libraryTypeName = 'Unknown'
        self._libraryVersion = 'Unknown'
        self._pyOzwlibVersion =  'Unknown'
        
        self._ozwconfig = ozwconfig
        
        self._ready = False
        # récupération des association nom de réseaux et homeID
        self._nameAssoc ={}
        if self._configPlug != None :
            num = 1
            loop = True
            while loop == True:
                HIdName = self._configPlug.query('ozwave', 'homename-%s' % str(num))
                HIdAssoc = self._configPlug.query('ozwave', 'homeidass-%s' % str(num))
                if HIdName != None : 
                    try :
                        self._nameAssoc[HIdName] = long(HIdAssoc,  16)
                    except OZwaveException as e:
                        self._log.error(e.value)
                        print e.value
                        self._nameAssoc[HIdName]  = 0
                else:
                    loop = False
                num += 1                
        print self._nameAssoc
        threading.Thread.__init__(self, target=self.run)
    
        if not os.path.exists(self._ozwconfig) : 
            self._log.debug("Directory openzwave config not exist : %s" , self._ozwconfig)
            print ("Directory openzwave config not exist : %s"  % self._ozwconfig)
            # TODO: lancer une execption
        # Séquence d'initialisation de py-openzwave
        # Spécification du chemain d'accès à la lib open-zwave
        opt=""
        if ozwlog=="True" : opts = "--logging true"
        else : opts = "--logging false"
        # if msgEndCb : opts = opts + "--NotifyTransactions true" # false par defaut  --- desactivé, comportement bizard
        self._log.info("Try to run openzwave manager")
        self.options = openzwave.PyOptions()
        self.options.create(self._ozwconfig, ozwuser,  opts) 
        self.options.lock() # nécessaire pour bloquer les options et autoriser le PyManager à démarrer
        self._manager = openzwave.PyManager()
        self._manager.create()
        self._manager.addWatcher(self.cb_openzwave) # ajout d'un callback pour les notifications en provenance d'OZW.
        self._log.info(self.pyOZWLibVersion + " -- plugin version :" + OZWPLuginVers)
        # self.manager.addDriver(self._device)  # ajout d'un driver dans le manager, fait par self.openDevice() dans class OZwave(XplPlugin):
        print ('user config :',  ozwuser,  " Logging openzwave : ",  opts)
        print self.pyOZWLibVersion + " -- plugin version :" + OZWPLuginVers
    #    sleep(5)
        
     # On accède aux attributs uniquement depuis les property
    device = property(lambda self: self._device)
    homeId = property(lambda self: self._homeId)
    activeNodeId= property(lambda self: self._activeNodeId)
    controllerNode = property(lambda self: self._controller)
    controllerDescription = property(lambda self: self._getControllerDescription())
    nodes = property(lambda self: self._nodes)   
    libraryDescription = property(lambda self: self._getLibraryDescription())
    libraryTypeName = property(lambda self: self._libraryTypeName)
    libraryVersion = property(lambda self: self._libraryVersion)
    nodeCount = property(lambda self: len(self._nodes))
    nodeCountDescription = property(lambda self: self._getNodeCountDescription())
    sleepingNodeCount = property(lambda self: self._getSleepingNodeCount())
    ready = property(lambda self: self._ready)
    pyOZWLibVersion = property(lambda self: self._getPyOZWLibVersion())

    def openDevice(self, device):
        """Ajoute un controleur au manager (en developpement 1 seul controleur actuellement)"""
        # TODO: Gérer une liste de controleurs
        if self._device != None and self._device != device :
            self._log.info("Remove driver from openzwave : %s",  self._device)
            self._manager.removeDriver(self._device)
        self._device = device
        self._log.info("adding driver to openzwave : %s",  self._device)
        self._manager.addDriver(self._device)  # ajout d'un driver dans le manager
        
    def stop(self):
        """ Stop class OZWManager
        """
        self._manager.removeDriver(self.device)
        self._ready = False

    def run(self, stop):
        """ Maintient la class OZWManager pour le fonctionnement du plugin
        @param stop : an Event to wait for stop request
        """
        # tant que le plugins est en cours mais pas lancer pour l'instant, vraiment util ?
        self._log.info("Start plugin listenner")
        print ("Start plugin listenner")
        try:
            while not stop.isSet():
                sleep (1)  # utile pour libérer le temps processeur ?
        except OZwaveException :
            self._log.error("Error listener run")
            return
        print ("Stop plugin listener")
        
    def _getPyOZWLibVersion(self):
        """Renvoi les versions des librairies py-openzwave ainsi que la version d'openzwave"""
        self._pyOzwlibVersion = self._manager.getPythonLibraryVersion ()
        if self._pyOzwlibVersion :
            return 'py-openzwave : {0} , OZW revision : r532'.format(self._pyOzwlibVersion )
        else:
            return 'Unknown'
            
    def _getSleepingNodeCount(self):
        """ Renvoi le nombre de node en veille """
        retval = 0
        for node in self._nodes.itervalues():
            if node.isSleeping:
                retval += 1
        return retval - 1 if retval > 0 else 0

    def _getLibraryDescription(self):
        """Renvoi le type de librairie ainsi que la version du controleur du réseaux zwave HomeID"""
        if self._libraryTypeName and self._libraryVersion:
            return '{0} Library Version {1}'.format(self._libraryTypeName, self._libraryVersion)
        else:
            return 'Unknown'

    def _getNodeCountDescription(self):
        """Renvoi le nombre de node total et/ou le nombre en veille (return str)"""
        retval = '{0} Nodes'.format(self.nodeCount)
        sleepCount = self.sleepingNodeCount
        if sleepCount:
            retval = '{0} ({1} sleeping)'.format(retval, sleepCount)
        return retval

    def _getControllerDescription(self):
        """ Renvoi la description du node actif (fabriquant et produit)"""
        if self._activeNodeId:
            node = self._getNode(self._homeId, self._activeNodeId)
            if node and node._product:
                return node._product.name
        return 'Unknown Controller'

    def cb_openzwave(self,  args):
        """Callback depuis la librairie py-openzwave 
        """
    # callback ordre : (notificationtype, homeid, nodeid, ValueID, groupidx, event) 
    # notification implémentés
#         ValueAdded = 0                    / A new node value has been added to OpenZWave's list. These notifications occur after a node has been discovered, and details of its command classes have been received.  Each command class may generate one or more values depending on the complexity of the item being represented.
#         ValueChanged = 2                  / A node value has been updated from the Z-Wave network and it is different from the previous value.
#         NodeNew = 5                       / A new node has been found (not already stored in zwcfg*.xml file)
#         NodeAdded = 6                     / A new node has been added to OpenZWave's list.  This may be due to a device being added to the Z-Wave network, or because the application is initializing itself.
#         NodeEvent = 10                    / A node has triggered an event.  This is commonly caused when a node sends a Basic_Set command to the controller.  The event value is stored in the notification.
#         DriverReady = 17                  / A driver for a PC Z-Wave controller has been added and is ready to use.  The notification will contain the controller's Home ID, which is needed to call most of the Manager methods.
#         NodeQueriesComplete = 22          / All the initialisation queries on a node have been completed.
#         AwakeNodesQueried = 23            / All awake nodes have been queried, so client application can expected complete data for these nodes.
#         AllNodesQueried = 24              / All nodes have been queried, so client application can expected complete data.

#TODO: notification à implémenter
#         ValueRemoved = 1                  / A node value has been removed from OpenZWave's list.  This only occurs when a node is removed.
#         ValueRefreshed = 3                / A node value has been updated from the Z-Wave network.
#         Group = 4                         / The associations for the node have changed. The application should rebuild any group information it holds about the node.
#         NodeRemoved = 7                   / A node has been removed from OpenZWave's list.  This may be due to a device being removed from the Z-Wave network, or because the application is closing.
#         NodeProtocolInfo = 8              / Basic node information has been receievd, such as whether the node is a listening device, a routing device and its baud rate and basic, generic and specific types. It is after this notification that you can call Manager::GetNodeType to obtain a label containing the device description.
#         NodeNaming = 9                    / One of the node names has changed (name, manufacturer, product).
#         PollingDisabled = 11              / Polling of a node has been successfully turned off by a call to Manager::DisablePoll
#         PollingEnabled = 12               / Polling of a node has been successfully turned on by a call to Manager::EnablePoll
#         CreateButton = 13                 / Handheld controller button event created 
#         DeleteButton = 14                 / Handheld controller button event deleted 
#         ButtonOn = 15                     / Handheld controller button on pressed event
#         ButtonOff = 16                    / Handheld controller button off pressed event 
#         DriverFailed = 18                 / Driver failed to load
#         DriverReset = 19                  / All nodes and values for this driver have been removed.  This is sent instead of potentially hundreds of individual node and value notifications.
#         MsgComplete = 20                  / The last message that was sent is now complete.
#         EssentialNodeQueriesComplete = 21 / The queries on a node that are essential to its operation have been completed. The node can now handle incoming messages.
#         Error = 25                        / An error has occured that we need to report.

        print('\n%s\n[%s]:' % ('-'*20, args['notificationType']))
        print args

#        if args:
#            print('homeId: 0x%.8x' % args['homeId'])
#            print('nodeId: %d' % args['nodeId'])
#            v = args['valueId']
#            print('valueID: %s' % v['id'])
#            if v.has_key('groupIndex') and v['groupIndex'] != 0xff: print('GroupIndex: %d' % v['groupIndex'])
#            if v.has_key('event') and v['event'] != 0xff: print('Event: %d' % v['event'])
#            if v.has_key('value'): print('Value: %s' % str(v['value']))
#            if v.has_key('label'): print('Label: %s' % v['label'])
#            if v.has_key('units'): print('Units: %s' % v['units'])
#            if v.has_key('readOnly'): print('ReadOnly: %s' % v['readOnly'])
#        print('%s\n' % ('-'*20,)) 
#        
        notifyType = args['notificationType']
        if notifyType == 'DriverReady':
            self._handleDriverReady(args)
        elif notifyType in ('NodeAdded', 'NodeNew'):
            self._handleNodeChanged(args)
        elif notifyType == 'ValueAdded':
            self._handleValueAdded(args)
        elif notifyType == 'ValueChanged':
            self._handleValueChanged(args)
        elif notifyType == 'NodeEvent':
            self._handleNodeEvent(args)
        elif notifyType == 'NodeQueriesComplete':
            self._handleNodeQueryComplete(args)
        elif notifyType in ('AwakeNodesQueried', 'AllNodesQueried'):
            self._handleInitializationComplete(args)

        else : self._log.info("zwave callback : %s is not handled yet",  notifyType)
    
    def _handleDriverReady(self, args):
        """Appelé une fois que le controleur est déclaré et initialisé dans OZW.
        l'HomeID et NodeID du controlleur sont enregistrés."""
        self._homeId = args['homeId']
        self._activeNodeId= args['nodeId']
        self._libraryVersion = self._manager.getLibraryVersion(self._homeId)
        self._libraryTypeName = self._manager.getLibraryTypeName(self._homeId)
        self._ctrlnodeId =  self._activeNodeId
        self._log.info("Device %s ready. homeId is 0x%0.8x, controller node id is %d, using %s library version %s", self._device,  self._homeId, self._activeNodeId, self._libraryTypeName, self._libraryVersion)
        self._log.info('OpenZWave Initialization Begins.')
        self._log.info('The initialization process could take several minutes.  Please be patient.')
        print ('controleur prêt' )
        
    def _handleNodeQueryComplete(self, args):
        """Les requettes d'initialisation du node sont complété."""
        node = self._getNode(self._homeId, args['nodeId'])
        self._updateNodeCapabilities(node)
        self._updateNodeCommandClasses(node)
        self._updateNodeNeighbors(node)
        self._updateNodeInfo(node)
        self._updateNodeGroups(node)
        self._controller = self._getNode(self._homeId, self._ctrlnodeId )
        self._log.info('Z-Wave Device Node {0} is ready.'.format(node.id))

    def _getNode(self, homeId, nodeId):
        """ Renvoi l'objet node correspondant"""
        return self._nodes[nodeId] if self._nodes.has_key(nodeId) else None
        
    def _fetchNode(self, homeId, nodeId):
        """ Renvoi et construit un nouveau node s'il n'existe pas et l'enregistre dans le dict """
        retval = self._getNode(homeId, nodeId)
        if retval is None:
            retval = ZWaveNode(homeId, nodeId)
            self._log.debug('Created new node with homeId 0x%0.8x, nodeId %d', homeId, nodeId)
            self._nodes[nodeId] = retval
        return retval

    def _handleNodeChanged(self, args):
        """Un node est ajouté ou nouveau"""
        node = self._fetchNode(args['homeId'], args['nodeId'])
        node._lastUpdate = time.time()
        self._log.info ('Node %d as add (homeId %.8x)' , args['nodeId'],  args['homeId'])

    def _getValueNode(self, homeId, nodeId, valueId):
        """Renvoi la valueNode du node"""
        node = self._getNode(homeId, nodeId)
        if node is None:
           raise OZwaveException('Value notification received before node creation (homeId %.8x, nodeId %d)' % (homeId, nodeId))
        vid = valueId['id']
        if node._values.has_key(vid):
            retval = node._values[vid]
        else:
            retval = ZWaveValueNode(homeId, nodeId, valueId)
            self._log.debug('Created new value node with homeId %0.8x, nodeId %d, valueId %s', homeId, nodeId, valueId)
            node._values[vid] = retval
        return retval 

    def _handleValueAdded(self, args):
        """Un valueNode est ajouté au node depuis le réseaux zwave"""
        homeId = args['homeId']
        activeNodeId= args['nodeId']
        valueId = args['valueId']
        node = self._fetchNode(homeId, activeNodeId)
        node._lastUpdate = time.time()
        valueNode = self._getValueNode(homeId, activeNodeId, valueId)
        valueNode.update(args) 
       
    def _handleValueChanged(self, args):
        """"Un valuenode à changé sur le réseaux zwave"""
        sendxPL = False
        homeId = args['homeId']
        activeNodeId= args['nodeId']
        valueId = args['valueId']
        node = self._fetchNode(homeId, activeNodeId)
        node._sleeping = False # TODO: pas sur que le device soit réèlement sortie du mode spleeping
        node._lastUpdate = time.time()
        valueNode = self._getValueNode(homeId, activeNodeId, valueId)
        valueNode.update(args) 
        # formattage infos générales
        msgtrig = {'typexpl':'xpl-trig',
                          'addressety' : "%s.%d.%d" %(self._nameAssoc.keys()[self._nameAssoc.values().index(homeId)] , activeNodeId,valueId['instance']) ,               
                          'valuetype':  valueId['type'], 
                          'type' : valueId['label'].lower()}  # ici l'idée est de passer tout les valeurs stats et trig en identifiants leur type par le label forcé en minuscule.
                                                                                 # les labels sont liste dans les tableaux des devices de la page spéciale, il faut les saisir dans sensor.basic-ozwave.xml.
        # TODO: Traiter le formattage en fonction du type de message à envoyer à domogik rajouter ici le traitement pour chaque command_class
        # ne pas modifier celles qui fonctionnent mais rajouter. la fusion ce fera après implémentation des toutes les command-class.
        if valueId['commandClass'] == 'COMMAND_CLASS_BASIC' :
            if valueId['genre'] == 'Basic' and 'Power Switch' in node.productType:
                sendxPL = True
                msgtrig['schema'] ='ozwave.basic'
                msgtrig['genre'] = 'actuator'
                msgtrig['level']=  valueId['value']
        if valueId['commandClass'] == 'COMMAND_CLASS_SWITCH_BINARY' :
            if valueId['type'] == 'Bool' :
                sendxPL = True
                msgtrig['schema'] ='ozwave.basic'
                msgtrig['genre'] = 'actuator'
                msgtrig['level']=  valueId['value']
        elif valueId['commandClass'] == 'COMMAND_CLASS_SENSOR_BINARY' : 
            if valueId['type'] == 'Bool' :
                sendxPL = True
                msgtrig['schema'] ='sensor.basic'
                msgtrig ['genre'] = 'sensor'
                msgtrig ['type'] = 'status'
                msgtrig ['value'] = valueId['value']
          #      args2 = args  # pour debug a supp
          #      args2['event'] = valueId['value']
          #      self._handleNodeEvent(args2) # pour debug a supp
        elif valueId['commandClass'] == 'COMMAND_CLASS_SENSOR_MULTILEVEL' :
                sendxPL = True
                msgtrig['schema'] ='sensor.basic'
                msgtrig ['genre'] = 'sensor'
                msgtrig ['value'] = valueId['value']
                msgtrig ['type'] = valueId['label'].lower()
                msgtrig ['units']= valueId['units']
        elif valueId['commandClass'] == 'COMMAND_CLASS_BATTERY' :
                sendxPL = True
                msgtrig['schema'] ='sensor.basic'
                msgtrig ['genre'] = 'sensor'
                msgtrig ['value'] = valueId['value']
                msgtrig ['units']= valueId['units']        
                
        if sendxPL: self._cb_sendxPL_trig(msgtrig)
        else : print ('commande non  implémentée : %s'  % valueId['commandClass'] )

    def _handleNodeEvent(self, args):
        """Un node à envoyé une Basic_Set command  au controlleur.  
        Cette notification est générée par certains capteur,  comme les decteurs de mouvement type PIR, pour indiquer qu'un événements a été détecter.
        Elle est aussi envoyée dans le cas d'une commande locale d'un device. """
        CmdsClassBasicType = ['COMMAND_CLASS_SWITCH_BINARY', 'COMMAND_CLASS_SENSOR_BINARY', 'COMMAND_CLASS_SENSOR_MULTILEVEL', 
                                             'COMMAND_CLASS_SWITCH_MULTILEVEL',  'COMMAND_CLASS_SWITCH_ALL',  'COMMAND_CLASS_SWITCH_TOGGLE_BINARY',  
                                              'COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL', 'COMMAND_CLASS_SENSOR_MULTILEVEL', ]
        sendxPL = False
        homeId = args['homeId']
        activeNodeId= args['nodeId']
        # recherche de la valueId qui a envoyée le NodeEvent
        node = self._fetchNode(homeId, activeNodeId)
        values = node.getValuesForCommandClass('COMMAND_CLASS_BASIC')
        print "*************** Node event handle *******"
        print node.productType
        print node._commandClasses 
        args2 = ""
        for classId in node._commandClasses :
            if PyManager.COMMAND_CLASS_DESC[classId] in CmdsClassBasicType :
                valuebasic = node.getValuesForCommandClass(PyManager.COMMAND_CLASS_DESC[classId] )
                args2 = dict(args)
                del args2['event']
                valuebasic[0].valueData['value'] = args['event']
                args2['valueId'] = valuebasic[0].valueData
                args2['notificationType'] = 'ValueChanged'
                break
        print "Valeur event :" + args['event']
        for value in values :
            print "-- Value :"
            print value
        if args2 :
                print "Event transmit à ValueChanged :"
                print args2
                self._handleValueChanged(args2)
                print"********** Node event handle fin du traitement ******"        
                
    def _updateNodeCapabilities(self, node):
        """Mise à jour des capabilities set du node"""
        nodecaps = set()
        if self._manager.isNodeListeningDevice(node._homeId, node._nodeId): nodecaps.add('listening')
        if self._manager.isNodeRoutingDevice(node._homeId, node._nodeId): nodecaps.add('routing')

        node._capabilities = nodecaps
        self._log.debug('Node [%d] capabilities are: %s', node._nodeId, node._capabilities)

    def _updateNodeCommandClasses(self, node):
        """Mise à jour des command classes"""
        classSet = set()
        for cls in PyManager.COMMAND_CLASS_DESC:
            if self._manager.getNodeClassInformation(node._homeId, node._nodeId, cls):
                classSet.add(cls)
        node._commandClasses = classSet
        self._log.debug('Node [%d] command classes are: %s', node._nodeId, node._commandClasses)
        # TODO: add command classes as string

    def _updateNodeNeighbors(self, node):
        '''Update node's neighbor list'''
        # TODO: I believe this is an OZW bug, but sleeping nodes report very odd (and long) neighbor lists
        neighborstr = str(self._manager.getNodeNeighbors(node._homeId, node._nodeId))
        if neighborstr is None or neighborstr == 'None':
            node._neighbors = None
        else:
            node._neighbors = sorted([int(i) for i in filter(None, neighborstr.strip('()').split(','))])

        if node.isSleeping and node._neighbors is not None and len(node._neighbors) > 10:
            self._log.warning('Probable OZW bug: Node [%d] is sleeping and reports %d neighbors; marking neighbors as none.', node.id, len(node._neighbors))
            node._neighbors = None
            
        self._log.debug('Node [%d] neighbors are: %s', node._nodeId, node._neighbors)

    def _updateNodeInfo(self, node):
        '''Update general node information'''
        node._name = self._manager.getNodeName(node._homeId, node._nodeId)
        node._location = self._manager.getNodeLocation(node._homeId, node._nodeId)
        node._manufacturer = NamedPair(id=self._manager.getNodeManufacturerId(node._homeId, node._nodeId), name=self._manager.getNodeManufacturerName(node._homeId, node._nodeId))
        node._product = NamedPair(id=self._manager.getNodeProductId(node._homeId, node._nodeId), name=self._manager.getNodeProductName(node._homeId, node._nodeId))
        node._productType = NamedPair(id=self._manager.getNodeProductType(node._homeId, node._nodeId), name=self._manager.getNodeType(node._homeId, node._nodeId))
        node._nodeInfo = NodeInfo(
            generic = self._manager.getNodeGeneric(node._homeId, node._nodeId),
            basic = self._manager.getNodeBasic(node._homeId, node._nodeId),
            specific = self._manager.getNodeSpecific(node._homeId, node._nodeId),
            security = self._manager.getNodeSecurity(node._homeId, node._nodeId),
            version = self._manager.getNodeVersion(node._homeId, node._nodeId)
        )

    def _updateNodeGroups(self, node):
        '''Update node group/association information'''
        groups = list()
        for i in range(0, self._manager.getNumGroups(node._homeId, node._nodeId)):
            groups.append(GroupInfo(
                index = i,
                label = self._manager.getGroupLabel(node._homeId, node._nodeId, i),
                maxAssociations = self._manager.getMaxAssociations(node._homeId, node._nodeId, i),
                members = self._manager.getAssociations(node._homeId, node._nodeId, i)
            ))
        node._groups = groups
        self._log.debug('Node [%d] groups are: %s', node._nodeId, node._groups)

    def _updateNodeConfig(self, node):
        self._log.debug('Requesting config params for node [%d]', node._nodeId)
        self._manager.requestAllConfigParams(node._homeId, node._nodeId)

    def _handleInitializationComplete(self, args):
        # La séquence d'initialisation est terminée
        controllercaps = set()
        if self._manager.isPrimaryController(self._homeId): controllercaps.add('primaryController')
        if self._manager.isStaticUpdateController(self._homeId): controllercaps.add('staticUpdateController')
        if self._manager.isBridgeController(self._homeId): controllercaps.add('bridgeController')
        self._controllerCaps = controllercaps
        self._log.info('Controller capabilities are: %s', controllercaps)
        for node in self._nodes.values():
            self._updateNodeCapabilities(node)
            self._updateNodeCommandClasses(node)
            self._updateNodeNeighbors(node)
            self._updateNodeInfo(node)
            self._updateNodeGroups(node)
            self._updateNodeConfig(node)
        self._ready = True
        self._log.info("OpenZWave initialization is complete.  Found {0} Z-Wave Device Nodes ({1} sleeping)".format(self.nodeCount, self.sleepingNodeCount))
        #self._manager.writeConfig(self._homeId)

    def refresh(self, node):
        self._log.debug('Requesting refresh for node {0}'.format(node.id))
        self._manager.refreshNodeInfo(node.homeId, node.id)
    
    def setNodeName(self, node, name):
        self._log.debug('Requesting setNodeName for node {0} with new name {1}'.format(node.id, name))
        self._manager.setNodeName(node.homeId, node.id, name)
 
    def setNodeLocation(self, node, loc):
        self._log.debug('Requesting setNodeLocation for node {0} with new location {1}'.format(node.id, loc))
        self._manager.setNodeLocation(node.homeId, node.id, loc)
        
    def setNodeOn(self, node):
        self._log.debug('Requesting setNodeOn for node {0}'.format(node.id))
        self._manager.setNodeOn(node.homeId, node.id)

    def setNodeOff(self, node):
        self._log.debug('Requesting setNodeOff for node {0}'.format(node.id))
        self._manager.setNodeOff(node.homeId, node.id)

    def setNodeLevel(self, node, level):
        self._log.debug('Requesting setNodeLevel for node {0} with new level {1}'.format(node.id, level))
        self._manager.setNodeLevel(node.homeId, node.id, level)
    
    def getCommandClassName(self, commandClassCode):
        return PyManager.COMMAND_CLASS_DESC[commandClassCode]

    def getCommandClassCode(self, commandClassName):
        for k, v in PyManager.COMMAND_CLASS_DESC.iteritems():
            if v == commandClassName:
                return k
        return None
        
    def getNetworkInfo(self):
        """ Retourne les infos principales du réseau zwave (dict) """
        retval={}
        if self.ready :
            retval["HomeID"] ="0x%.8x" % self.homeId
            retval["Model"]= self.controllerNode.manufacturer + " -- " + self.controllerNode.product
            retval["Primary controller"] = self.controllerDescription
            retval["Device"] = self.device
            retval["Node"] = self.controllerNode.nodeId
            retval["Library"] = self._libraryTypeName
            retval["Version"] = self._libraryVersion
            retval["Node count"] = self.nodeCount
            retval["Node sleeping"] = self.sleepingNodeCount
            retval["PYOZWLibVers"] = self.pyOZWLibVersion
            retval["OZWPluginVers"] = OZWPLuginVers
            ln = []
            for n in self.nodes : ln.append(n)
            retval["ListNodeId"] = ln
            return retval
        else : return {'error' : 'Zwave network not ready, be patient...'}
        
    def saveNetworkConfig(self):
        """Enregistre le configuration au format xml"""
        retval = {}
        self._manager.writeConfig(self.homeId)
        print "config sauvée"
        retval["File"] ="confirmed"
        return retval

    def getZWRefFromxPL(self, addresseTy):
        """ Retourne  les références Zwave envoyées depuis le xPL domogik 
        @ param : addresseTy format : nomReseaux.NodeID.Instance """
        ids = addresseTy.split('.')
        retval ={}
        retval['homeId'] = self._nameAssoc[ids[0]] if self._nameAssoc[ids[0]]  else self.homeId
        if (retval['homeId'] == 0) : retval['homeId'] = self.homeId # force le homeid si pas configuré correctement, TODO : gérer un message pour l'utilisateur pour erreur de config.
        print "getZWRefFromxPL : ", retval
        retval['nodeId']  = int(ids[1])
        retval['instance']  = int(ids[2])
        print "getZWRefFromxPL : ", retval
        return retval
        
    def sendNetworkZW(self, command,  addresseTy, opt =""):
        """ En provenance du réseaux xPL
              Envoie la commande sur le réseaux zwave  """ 
        print ("envoi zwave command %s" % command)
        if addresseTy != None :
            addrZW = self.getZWRefFromxPL(addresseTy)
            nodeID = int(addrZW['nodeId'])
            homeId = addrZW['homeId'] # self.homeId
            instance = addrZW['instance']
            print('homeId: %d' % homeId)
	    if (opt != "") and (opt != 'None'):
	        opt = int(opt)
            if (opt == 'None') :
                opt = 0
            if instance == 1 :
                if command == 'level':
                    self._manager.setNodeLevel(self.homeId, nodeID, opt)
                elif command == 'on':
                    self._manager.setNodeOn(homeId, nodeID)
                elif command == 'off':
                    self._manager.setNodeOff(homeId, nodeID)
                else : 
                    self._log.info("xPL to ozwave unknown command : %s , nodeID : %d",  command,  nodeID)
            else : # instance secondaire, utilisation de set value
                print ("instance secondaire")
                node = self._getNode(self.homeId,  nodeID)
                cmdsClass= ['COMMAND_CLASS_BASIC', 'COMMAND_CLASS_SWITCH_BINARY']
                for value in node.values.keys() :
                    val = node.values[value].valueData
                    print ("valeur : " + val['commandClass'])
                    if (val['commandClass'] in cmdsClass)  and val['instance'] == instance :
                        if command=='on' : opt = 255
                        elif command=='off' : opt = 0
                        print ("setValue de %s, instance :%d, value : %d, on valueId : %d" %(val['commandClass'], instance,  opt, val['id']))                        
                        if not self._manager.setValue(val['id'], opt)  : 
                            self._log.error ("setValue return bad type : %s, instance :%d, value : %d, on valueId : %d" %(val['commandClass'], instance,  opt, val['id']))
                            print("return bad type value")
                        break
            print ("commande transmise")
            print "Request demande Type : " + self._manager.getNodeType(homeId,  nodeID)
            print "Manufact node : "+ self._manager.getNodeManufacturerName(homeId,nodeID)

    def getNodeInfo(self,  nodeID):
        """ Retourne les informations d'un device, format dict{} """
        retval={}
        if self.ready :
            node = self._getNode(self.homeId,  nodeID)
            self._updateNodeInfo(node) # mise à jour selon OZW
            retval["HomeID"] ="0x%.8x" % node.homeId
            retval["Model"]= node.manufacturer + " -- " + node.product
            retval["State sleeping"] = 'true' if node.isSleeping else 'false'
            retval["Node"] = node.nodeId
            retval["Name"] = node.name if node.name else 'Undefined'
            retval["Location"] = node.location if node.location else 'Undefined'
            retval["Type"] = node.productType
            retval["Last update"] = time.ctime(node.lastUpdate)
            retval["Neighbors"] = node.neighbors if  node.neighbors else 'No one'
            return retval
        else : return {"error" : "Zwave network not ready, can't find node %d" %nodeID}
        
    def getNodeValuesInfo(self,  nodeID):
        """ Retourne les informations de values d'un device, format dict{} """
        retval={}
        if self.ready :
            node = self._getNode(self.homeId,  nodeID)
            self._updateNodeInfo(node) # mise à jour selon OZW
            retval['Values'] = []
            for value in node.values.keys():
                val = node.values[value].valueData
                val['homeId'] = int(val['homeId'])
                val['id'] = int(val['id'])
                val['domogikdevice']  = True if (val['commandClass'] in  CmdsClassAvailable) else False
                retval['Values'].append(val)
            print  retval['Values']
            return retval
        else : return {"error" : "Zwave network not ready, can't find node %d" %nodeID}
           
    def setUINodeNameLoc(self,  nodeID,  newname, newloc):
        """Change le nom et/ou le localisation du node dans OZW et dans le decive si celui-ci le supporte """
        if self.ready :
            node = self._getNode(self.homeId,  nodeID)
            if node.name != newname :
                self.setNodeName(node,  newname)
            if node.location != newloc :
                self.setNodeLocation(node,  newloc)
            return self.getNodeInfo(nodeID)                                
        else : return {"error" : "Zwave network not ready, can't find node %d" %nodeID}
        
