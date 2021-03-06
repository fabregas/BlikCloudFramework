#!/usr/bin/python
"""
Copyright (C) 2011 Konstantin Andrusenko
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.

@package blik.bootManager.bootEventListener
@author Konstantin Andrusenko
@date July 28, 2011

This module contains the implementation of BootEventListener class.
"""

import sys
import signal
from blik.utils.friBase import FriServer
from blik.utils.databaseConnection import DatabaseConnection
from blik.utils.logger import logger

LISTENER_PORT = 1986

#node admin states
NAS_NEW       = 0
NAS_ACTIVE    = 1
NAS_NOTACTIVE  = 2

#node current states
NCS_UP   = 1
NCS_DOWN = 0

ADMIN = 'admin'
MOD_HOST_OPER = 'MOD_HOSTNAME'
SYNC_OPER = 'SYNC'

class BootEventListener(FriServer):
    def __init__(self):
        self.__dbconn = DatabaseConnection()
        FriServer.__init__(self, hostname='0.0.0.0', port=LISTENER_PORT, workers_count=1)

    def onDataReceive( self, json_object ):
        #get hostname
        hostname = self.__get_element(json_object, 'hostname')

        #get ip_address (this field is optional)
        ip_address = json_object.get('ip_address', None)

        #get login
        login = self.__get_element(json_object, 'login')

        #get password
        password = self.__get_element(json_object, 'password')

        #get processor
        processor = self.__get_element(json_object, 'processor')

        #get memory
        memory = self.__get_element(json_object, 'memory')

        #get mac_address
        mac_address = self.__get_element(json_object, 'mac_address')

        #get uuid
        uuid = self.__get_element(json_object, 'uuid')

        #process boot event
        self.__process_event(uuid, hostname, login, password, mac_address, ip_address, processor, memory)


    def __get_element(self, json_object, name):
        element = json_object.get(name, None)
        if element is None:
            raise Exception('Element <%s> is not found in boot event packet!'%name)

        if type(element) == str:
            element = element.strip()

        return element

    def __process_event(self, uuid, hostname, login, password, mac_address, ip_address, processor, memory):
        hw_info = 'Processor: %s\nMemory: %s'%(processor, memory)

        rows = self.__dbconn.select("SELECT hostname FROM nm_node WHERE node_uuid=%s", (uuid,))

        if not rows:
            #this is new node, create it in database in NEW status
            self.__dbconn.modify("INSERT INTO nm_node (node_uuid, hostname, login, password, mac_address, ip_address, admin_status, current_state, hw_info)\
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (uuid, hostname, login, password, mac_address, ip_address, NAS_NEW, NCS_UP, hw_info))

        else:
            #we already has this node in database, update it
            self.__dbconn.modify("UPDATE nm_node SET hostname=%s, login=%s, password=%s, mac_address=%s, ip_address=%s, hw_info=%s, current_state=%s\
                                    WHERE node_uuid=%s", (hostname, login, password, mac_address, ip_address, hw_info, NCS_UP, uuid))


            caller = self._get_operation_caller()
            if caller:
                logger.debug('Synchronize %s node parameters'%hostname)
                ret_code, ret_message = caller.call_nodes_operation(ADMIN, [hostname], SYNC_OPER, {})
                logger.debug('call SYNC operation result: [%s] %s'%(ret_code, ret_message))



    def _get_operation_caller(self):
        #try import nodes manager caller
        try:
            from blik.nodesManager.dbusClient import DBUSInterfaceClient
            client = DBUSInterfaceClient()

            return client
        except ImportError, err:
            logger.warning('Boot manager require nodes manager for automatic changing hostname.')

            return None


#--------------------------------------------------------------------------------



if __name__ == '__main__':
    try:
        logger.info('Boot event listener starting...')

        listener = BootEventListener()

        def stop(s, p):
            global listener
            try:
                logger.info('Boot event listener stoping...')
                listener.stop()
            except Exception, err:
                logger.error('Stoping boot event listener error: %s'%err)

        signal.signal(signal.SIGINT, stop)

        listener.start()

        logger.info('Boot event listener stoped')
    except Exception, err:
        logger.error('Boot event listener error: %s. exit!'%err)
        sys.exit(1)


