#!/usr/bin/python
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

- Zwave

@author: Nico <nico84dev@gmail.com>
@copyright: (C) 2007-2012 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

import sys
# sys.path.append("/var/lib/domogik")

from domogik.xpl.common.xplconnector import Listener
from domogik.xpl.common.plugin import XplPlugin
from domogik.xpl.common.xplmessage import XplMessage
from domogik.xpl.common.queryconfig import Query
from domogik_packages.xpl.lib.ozwave import OZWavemanager
from domogik_packages.xpl.lib.ozwave import OZwaveException
# from lib.ozwave import OZWave


class OZwave(XplPlugin):
    """ Implement à listener for Zwave command messages
        and launch background  manager to listening zwave events by callback
    """
    def __init__(self):
        """ Create listener and background zwave manager
        """
        XplPlugin.__init__(self, name = 'ozwave')
        
        # Récupère la config 
        # - device
        self._config = Query(self.myxpl, self.log)
        device = self._config.query('ozwave', 'device')
        ozwlogConf = self._config.query('ozwave', 'ozwlog')
        self._config = Query(self.myxpl, self.log)
        print ('Mode log openzwave :',  ozwlogConf)
        # Recupère l'emplacement des fichiers de configuration OZW
        pathConfig = self.get_data_files_directory() + '/ozwconfig/'
        pathUser = self.get_data_files_directory()  +'/'
        # Initialise le manager Open zwave
        try:
            self.myzwave = OZWavemanager(self._config, self.send_xPL, self.sendxPL_trig, self.get_stop(), self.log, ozwconfig = pathConfig,  ozwuser = pathUser,  ozwlog = ozwlogConf,  msgEndCb = True) # ozwlog="")
        except OZwaveException as e:
            self.log.error(e.value)
            print e.value
            self.force_leave()
            return    
                 
        # Crée le listener pour les messages de commande xPL traités par les devices zwave
        Listener(self.ozwave_cmd_cb, self.myxpl,{'schema': 'ozwave.basic',
                                                 'xpltype': 'xpl-cmnd'})
        
        # run du plugin
        #ozwave_process = threading.Thread(None,
         #                          self.myzwave.run,
          #                         "ozw-process-reader",
            #                       (self.get_stop(),),
               #                    {})
        #self.register_thread(ozwave_process)
        #ozwave_process.start()
        # Validation avant l'ouverture du controleur, la découverte du réseaux zwave prends trop de temps -> RINOR Timeout
        self.enable_hbeat()
        # Ouverture du controleur principal
        self.myzwave.openDevice(device)                  

    def ozwave_cmd_cb(self, message):
        """" Envoie la cmd xpl vers le OZWmanager"""
        print ("commande xpl reçu")
        print message
        if 'command' in message.data:
            if 'group'in message.data:
                # en provenance de l'UI spéciale
                self.ui_cmd_cb(message)
            else :
                cmd = message.data['command']
                # addresseTy = int(message.data['node'])
                addresseTy = message.data['addressety']
                if cmd == 'level' :
                    print ("appel envoi zwave command %s" %cmd)
                    lvl = message.data['level']
                    self.myzwave.sendNetworkZW(cmd, addresseTy, lvl)
                elif cmd == "on"  or cmd == "off" :
                    print ("appel envoi zwave command %s" %cmd)
                    self.myzwave.sendNetworkZW(cmd, addresseTy)
                else:
                    self.myzwave.sendNetworkZW(cmd, addresseTy)
                    
    def getdict2UIdata(self, UIdata):
        """ retourne un format dict en provenance de l'UI (passage outre le format xPL)"""
        retval = UIdata.replace('|', '{').replace('\\', '}')
        try :
            return  eval(retval.replace(';', ','))
        except :
            return {'error': 'invalid format'}
            
    def getUIdata2dict(self, ddict):
        """Retourne le dict formatter pour UI (passage outre le format xPL)"""
        return str(ddict).replace('{', '|').replace('}', '\\').replace(',',';').replace('False', 'false').replace('True', 'true')
        
    def ui_cmd_cb(self, message):
        """xpl en provenace de l'UI (config/special)"""
        info = "essais"
        request = self.getdict2UIdata(message.data['value'])
        print("Commande UI")
        if message.data['group'] =='UI' :
            mess = XplMessage()
            mess.set_type('xpl-trig') 
            mess.set_schema('ozwave.basic')
            print request
            if request['request'] == 'GetNetworkID' :
                info = self.getUIdata2dict(self.myzwave.getNetworkInfo())
                mess.add_data({'command' : 'Refresh-ack', 
                                    'group' :'UI', 
                                    'node' : 0, 
                                    'data': info})
                print "Refresh network info"
            elif request['request'] == 'GetNodeInfo' :
                info = self.getUIdata2dict(self.myzwave.getNodeInfo(request['node']))
                mess.add_data({'command' : 'Refresh-ack', 
                                    'group' :'UI', 
                                    'node' : request['node'], 
                                    'data': info})
                print "Refresh node :",  request['node']
            elif  request['request'] == 'SaveConfig':
                info = self.getUIdata2dict(self.myzwave.saveNetworkConfig())
                mess.add_data({'command' : 'Refresh-ack', 
                                    'group' :'UI', 
                                    'node' :0, 
                                    'data': info})
            elif  request['request'] == 'SetNodeNameLoc':
                info = self.getUIdata2dict(self.myzwave.setUINodeNameLoc(request['node'], request['newname'],  request['newloc']))
                mess.add_data({'command' : 'Refresh-ack', 
                                    'group' :'UI', 
                                    'node' : request['node'], 
                                    'data': info})
            elif  request['request'] == 'GetNodeValuesInfo':
                info =self.myzwave.getNodeValuesInfo(request['node'])
                mess.add_data({'command' : 'Refresh-ack', 
                                    'group' :'UI', 
                                    'node' : request['node'], 
                                    'count': len(info['Values']) })
                i=0
                for inf in info['Values']:
                    mess.add_data({'value%d' %i :  self.getUIdata2dict(inf)})
                    i = i +1
                print mess
            else :
                mess.add_data({'command' : 'Refresh-ack', 
                                    'group' :'UI', 
                                    'node' : request['node'], 
                                    'data': "unknow request"})
                print "commande inconnue"
            self.myxpl.send(mess)
                                  
                                    
    def send_xPL(self, write):
        """ Envoie une commande zwave vers XPL"""
        # TODO : a implémenter pour les sénarios zwave entre module ?
        pass
        
    def sendxPL_trig(self, msgtrig):
        mess = XplMessage()
        if 'info' in msgtrig:
            self.log.error ("Error : Node %s unreponsive" % msgtrig['node'])
        elif 'Find' in msgtrig:
            print("node enregistré : %s" % msgtrig['Find'])
        elif 'typexpl' in msgtrig:
            print ("send xpl-trig")
            print msgtrig	
            mess.set_type('xpl-trig') # force xpl-trig
            mess.set_schema(msgtrig['schema'])
            if msgtrig['genre'] == 'actuator' :
                if msgtrig['level'] in ['0', 'False'] : cmd ="off"
                elif msgtrig['level'] in ['255', 'True']: cmd ="on"
                else: cmd ='level'
                mess.add_data({'addressety' : msgtrig['addressety'],
                            'command' : cmd,
                            'level': msgtrig['level']})
                if msgtrig.has_key('type'): mess.add_data({'type' : msgtrig['type'] })
            elif msgtrig['genre'] == 'sensor' :  # tout sensor
                if msgtrig['type'] =='status' :  # gestion du sensor binary pour widget portal
                    mess.add_data({'addressety' : msgtrig['addressety'],
                            'type' : msgtrig['type'] ,
                            'current' : 'low' if (msgtrig['value'] =='True')  else 'high'})
                else : mess.add_data({'addressety' : msgtrig['addressety'],  
                            'type' : msgtrig['type'] ,
                            'current' : msgtrig['value'] })
            if msgtrig.has_key('units'): mess.add_data({'units' : msgtrig['units'] })
            print mess
            self.myxpl.send(mess)
        elif 'command' in msgtrig and msgtrig['command'] == 'Info':
            print("Home ID is %s" % msgtrig['Home ID'])

if __name__ == "__main__":
    OZwave()
