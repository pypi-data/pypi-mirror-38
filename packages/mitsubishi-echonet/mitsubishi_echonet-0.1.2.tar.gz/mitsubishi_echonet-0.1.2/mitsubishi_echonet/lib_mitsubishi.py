"""
lib_mitsubishi is used to provide control to Mitsubishi HVAC WiFi controllers
that use the ECHONET-LITE protocol such as the Mitsubishi MAC-IF558 adaptor.

It is likely this could be used for other HVAC systems that use the ECHONET-LITE
protocol.

I originally planned for this to be a full blown ECHONET library, but at this
stage it will control the AC and thats it!

"""

import socket
import struct
import sys
from .eojx import *
from .epc  import *
from .esv  import *
from .functions  import Function as F

ENL_PORT = 3610
ENL_MULTICAST_ADDRESS = "224.0.23.0"


"""
BuildEchonetMsg is used to build an ECHONET-LITE control message in the form
of a byte string

param data: a dict representing the control message.
return: an int representing the control message.
"""
def BuildEchonetMsg(data):
   try:
      # EHD is fixed to 0x1081 because I am lazy.
      message = 0x1081

      # validate TID (set a default value if none provided)
      # TODO - TID message overlap.
      if 'TID' not in data:
         data['TID'] = 0x01
      elif data['TID'] > 0xFFFF:
         raise ValueError('Transaction ID is larger then 2 bytes.')
      message = (message << 16) + data['TID']

      # append SEOJ
      message = (message << 24) + 0x05FF01

      # validate DEOJ
      if data['DEOJGC'] in EOJX_GROUP:
          message = (message << 8) + data['DEOJGC']
      else:
          raise ValueError('Value ' + str(hex(data['DEOJGC'])) + ' not a valid SEO Group code')

      if data['DEOJCC'] in EOJX_CLASS[data['DEOJGC']]:
          message = (message << 8) + data['DEOJCC']
      else:
          raise ValueError('Value ' + str(hex(data['DEOJCC'])) + ' not a valid SEO class code')
      message = (message << 8) + data['DEOJIC']

      # validate ESV by looking up the codes.
      if data['ESV'] in ESV_CODES:
          # ESV code is a string
          message = (message << 8) + data['ESV']
      else:
          raise ValueError('Value not in ESV code table')

      # validate OPC
      message = (message << 8) + len(data['OPC'])

      # You can have multiple OPC per transaction.
      for values in data['OPC']:
        # validate EPC
        message =  (message << 8) + values['EPC']
        if 'PDC' in values:
            message =  (message << 8) + values['PDC']
        # if PDC has a value then concat EDT to message
            if values['PDC'] > 0:
                message =  (message << 8 * values['PDC']) + values['EDT']
        else:
            message =  (message << 8) + 0x00
      return format(int(message), 'x')
# some sloppy error handling here.
   except ValueError as error:
        # print('Caught this error: ' + repr(error))
        quit()


"""
DecodeEchonetMsg is used to build an ECHONET-LITE control message in the form
of a byte string

param bytes: A string representing the hexadecimal control message in ECHONET LITE
return: a dict representing the deconstructed ECHONET packet
"""
def DecodeEchonetMsg(byte):
  data = {}
  try:
      data['EHD1'] = byte[0]
      if data['EHD1'] not in EHD1:
          raise ValueError('EHD1 Header invalid')
      data['EHD2'] = byte[1]
      if data['EHD2'] not in EHD2:
          raise ValueError('EHD2 Header invalid')
      data['TID'] = int.from_bytes(byte[2:4], byteorder='big')

      # Decode SEOJ
      data['SEOJGC'] = byte[4]
      data['SEOJCC'] = byte[5]
      data['SEOJIC'] = byte[6]

      # Decode DEOJ
      data['DEOJGC'] =  byte[7]
      data['DEOJCC'] =  byte[8]
      data['DEOJIC'] =  byte[9]

      # DEcode Service property
      data['ESV'] =  byte[10]

      i = 0
      epc_pointer = 12
      data['OPC'] = []
      # decode multiple processing properties (OPC)
      while i <  (byte[11]):
          OPC = {}
          pdc_pointer = epc_pointer + 1
          edt_pointer = pdc_pointer + 1
          end_pointer = edt_pointer
          OPC['EPC'] = byte[epc_pointer]
          OPC['PDC'] =  byte[pdc_pointer]
          pdc_len = byte[pdc_pointer]
          end_pointer += pdc_len
          OPC['EDT'] = byte[edt_pointer:end_pointer]
          epc_pointer = end_pointer
          i += 1
          data['OPC'].append(OPC)

  except ValueError as error:
        print('Caught this error: ' + repr(error))
        quit()
  return data

"""
SendMessage is used for ECHONET Unicast and Multicast transcations
message is assumed a correctly formatted ECHONET string
SendMessage will receive multiple messages if multicast is used "eg 224.0.23.0"

param message: an int representing the ECHONET message
param ip_address: a string representing the IPv4 address e.g "1.2.3.4"

return: an array representing the received response from the ECHONET message
"""
def SendMessage(message, ip_address):
    data =[]
    transaction_group = (ip_address, ENL_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('',ENL_PORT))
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    sock.settimeout(0.5)

    # Set the time-to-live for messages to 1 so they do not
    # go past the local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        sent = sock.sendto(bytearray.fromhex(message), transaction_group)
        # Look for responses from all recipients
        while True:
            try:
                payload, server = sock.recvfrom(1024)
            except socket.timeout:
                break
            else:
                # Received a packet.
                data.append({'server':server,'payload':payload})
    finally:
        sock.close()
    return data

"""
Discover is used to identify ECHONET nodes. Original plan was for this library
to fully support a multitude of ECHONET devices.

return: an array of discovered ECHONET node objects.
"""
def Discover():
    eoa = []; # array containing echonet objects
    tx_payload = {
        'TID' : 0x01, # Transaction ID 1
        'DEOJGC': 0x0E,
        'DEOJCC': 0xF0,
        'DEOJIC': 0x00,
        'ESV' : 0x62,
        'OPC' : [{'EPC': 0xD6}]
    }
    # Build ECHONET discover messafge.
    message = BuildEchonetMsg(tx_payload)

    # Send message to multicast group and receive data
    data = SendMessage(message, ENL_MULTICAST_ADDRESS);
    # Decide received message for each node discovered:
    for node in data:
        rx = DecodeEchonetMsg(node['payload'])
        if (tx_payload['DEOJGC'] == rx['SEOJGC'] and
        rx['TID'] == tx_payload['TID'] and
        rx['OPC'][0]['EPC'] == 0xd6):
            print('ECHONET lite node discovered at {}'.format(node['server'][0]))

            # Action EDT payload by calling applicable function using lookup table
            edt = EPC_CODE[rx['SEOJGC']][rx['SEOJCC']][rx['OPC'][0]['EPC']][1](rx['OPC'][0]['EDT'])
            e = eval(EPC_CODE[edt['eojgc']][edt['eojcc']]['class'])(node['server'][0], edt['eojci'])
            eoa.append(e)

    return eoa


"""
Superclass for Echonet node objects.
"""
class EchoNetNode:

    """
    Construct a new 'EchoNet' object.

    :param instance: Instance ID
    :param netif: IP address of node
    """
    def __init__(self, instance = 0x1, netif="", polling = 10 ):
        self.netif = netif
        self.last_transaction_id = 0x1
        self.self_eojgc = None
        self.self_eojcc = None
        self.instance = instance
        self.available_functions = None
        self.status = False

    """
    GetMessage is used to fire ECHONET request messages to get Node information
    Assumes one OPC is sent per message.

    :param tx_epc: EPC byte code for the request.
    :return: the deconstructed payload for the response
    """
    def GetMessage(self, tx_epc):
        self.last_transaction_id += 1
        tx_payload = {
        'TID' : self.last_transaction_id,
        'DEOJGC': self.self_eojgc ,
        'DEOJCC': self.self_eojcc ,
        'DEOJIC': self.instance,
        'ESV' : GET,
        'OPC' : [{'EPC': tx_epc, 'PDC': 0x00}]
        }
        message = BuildEchonetMsg(tx_payload)

        data = SendMessage(message, self.netif);
        rx = DecodeEchonetMsg(data[0]['payload'])
        rx_edt = rx['OPC'][0]['EDT']
        rx_epc = rx['OPC'][0]['EPC']
        value = EPC_CODE[self.self_eojgc][self.self_eojcc]['functions'][rx_epc][1](rx_edt)
        return value


    """
    SetMessage is used to fire ECHONET request messages to set Node information
    Assumes one OPC is sent per message.

    :param tx_epc: EPC byte code for the request.
    :param tx_edt: EDT data relevant to the request.
    :return: the deconstructed payload for the response
    """
    def SetMessage(self, tx_epc, tx_edt):
        self.last_transaction_id += 1
        tx_payload = {
        'TID' : self.last_transaction_id,
        'DEOJGC': self.self_eojgc ,
        'DEOJCC': self.self_eojcc ,
        'DEOJIC': self.instance,
        'ESV' : SETC,
        'OPC' : [{'EPC': tx_epc, 'PDC': 0x01, 'EDT': tx_edt}]
        }
        message = BuildEchonetMsg(tx_payload)
        # print(message)
        data = SendMessage(message, self.netif);
        # print(data)
        rx = DecodeEchonetMsg(data[0]['payload'])

        rx_epc = rx['OPC'][0]['EPC']
        rx_pdc = rx['OPC'][0]['PDC']
        if rx_epc == tx_epc and rx_pdc == 0x00:
        # value = epc.CODE[self.self_eojgc][self.self_eojcc]['functions'][rx_epc][1](rx_edt)
            return True
        else:
            return False

    """
    GetOperationalStatus returns the ON/OFF state of the node

    :return: status as a string.
    """
    def GetOperationalStatus(self): # EPC 0x80
        print("Checking Operational Status..")
        self.status = self.GetMessage(0x80)['status']
        if self.status == 'On':
            print("The node is switched ON")
        else:
            print("The node is switched OFF")
        return self.status


    """
    setOperationalStatus sets the ON/OFF state of the node

    :param status: True if On, False if Off.
    """
    def SetOperationalStatus(self, status): # EPC 0x80
        print("Setting Operational Status..")
        self.SetMessage(0x80, 0x30 if status else 0x31)

    """
    On sets the node to ON.

    """
    def On (self): # EPC 0x80
        print("Switching on..")
        self.SetMessage(0x80, 0x30)

    """
    On sets the node to OFF.

    """
    def Off (self): # EPC 0x80
        print("Switching off..")
        self.SetMessage(0x80, 0x31)


"""Class for Home AirConditioner Objects"""
class HomeAirConditioner(EchoNetNode):

    """
    Construct a new 'HomeAirConditioner' object.
    In theory this would work for any ECHNONET enabled domestic AC.

    :param instance: Instance ID
    :param netif: IP address of node
    """
    def __init__(self, netif, instance = 0x1):
        EchoNetNode.__init__(self, instance, netif)
        self.self_eojgc = 0x01
        self.self_eojcc = 0x30
        self.available_functions = EPC_CODE[self.self_eojgc][self.self_eojcc]['functions']
        self.setTemperature = None
        self.roomTemperature = None
        self.mode = False
        self.fan_speed = None
        self.JSON = {}

    """
    Update is used as a quick and dirty way of producing a dict useful for API polling etc

    return: A string with the following attributes:
    {'status': '###', 'set_temperature': ##, 'fan_speed': '###', 'room_temperature': ##, 'mode': '###'}

    """
    def Update(self):
        self.last_transaction_id += 1
        tx_payload = {
        'TID' : self.last_transaction_id,
        'DEOJGC': self.self_eojgc ,
        'DEOJCC': self.self_eojcc ,
        'DEOJIC': self.instance,
        'ESV' : GET,
        'OPC' : [{'EPC':0x80},{'EPC': 0xB3},{'EPC': 0xA0},{'EPC': 0xBB},{'EPC': 0xB0}]
        }

        message = BuildEchonetMsg(tx_payload)
        data = SendMessage(message, self.netif);
        try:
            rx = DecodeEchonetMsg(data[0]['payload'])
        except IndexError as error:
            print('No Data Received')
            return self.JSON
        for data in rx['OPC']:
            rx_edt = data['EDT']
            rx_epc = data['EPC']
            value = EPC_CODE[self.self_eojgc][self.self_eojcc]['functions'][rx_epc][1](rx_edt)
            self.JSON.update(value)


        print(self.JSON)
        self.setTemperature = self.JSON['set_temperature']
        self.mode = self.JSON['mode']
        self.fan_speed = self.JSON['fan_speed']
        self.roomTemperature = self.JSON['room_temperature']
        self.status = self.JSON['status']
        return self.JSON

    """
    GetOperationaTemperature get the temperature that has been set in the HVAC

    return: A string representing the configured temperature.
    """
    def GetOperationalTemperature(self):
        self.setTemperature = self.GetMessage(0xB3)['set_temperature']
        # print("Current configured unit temperature is " + str(self.setTemperature) + " Degrees")
        return self.setTemperature


    """
    SetOperationaTemperature get the temperature that has been set in the HVAC

    param temperature: A string representing the desired temperature.
    """
    def SetOperationalTemperature(self, temperature):
        # print("Setting the configured temperature to " + str(temperature))
        if self.SetMessage(0xB3, int(temperature)):
            print("Temperature set sucessfully")
            self.GetOperationalTemperature()

    """
    GetMode returns the current configured mode (e.g Heating, Cooling, Fan etc)

    return: A string representing the configured mode.
    """
    def GetMode(self):
        self.mode = self.GetMessage(0xB0)['mode']
        print("Current configured mode is " + str(self.mode))

    """
    SetMode set the desired mode (e.g Heating, Cooling, Fan etc)

    param mode: A string representing the desired mode.
    """
    def SetMode(self, mode):
        print("Set the current operating mode")
        if self.SetMessage(0xB0, MODES[mode]):
            print("Mode set sucessfully")
        self.GetMode()

    """
    GetFanSpeed gets the current fan speed (e.g Low, Medium, High etc)

    return: A string representing the fan speed
    """
    def GetFanSpeed(self):
        self.fan_speed = self.GetMessage(0xA0)['fan_speed']
        print("Fan speed is " + str(self.fan_speed))


    """
    SetFanSpeed set the desired fan speed (e.g Low, Medium, High etc)

    param fans_speed: A string representing the fan speed
    """
    def SetFanSpeed(self, fan_speed):
        print("Set the current fan speed")
        if self.SetMessage(0xA0, FAN_SPEED[fan_speed]):
            print("Fan Speed set sucessfully")
        self.GetFanSpeed()
