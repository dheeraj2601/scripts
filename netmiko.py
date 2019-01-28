# netmiko library is used to auto-configure the routers .


#!/usr/bin/env python

from datetime import datetime
from netmiko import ConnectHandler
from my_devices import spine1
import subprocess

def main():
   start_time = datetime.now()
   print start_time
   net_connect = ConnectHandler(**ocnos_spine1)
   net_connect.find_prompt()
   net_connect.enable()
   output = net_connect.send_command("show ip int brief", delay_factor=0)

   cmd_list = []
   for j in range (50, 56):
      i = '20.'+str(j)+'.20.0/24'
      commands = 'ip route ' + i + ' Null'
      cmd_list.append(commands)

   print (cmd_list)

   # Convert commands to single string
   cmd_as_string = "\n".join(cmd_list)
   output = net_connect.send_config_set(cmd_as_string, delay_factor=0)
   print output

if __name__ == "__main__":
   main()




spine1 = {
   'device_type': '_ssh',
   'ip': 'x.x.x.x',
   'username': 'root',
   'password': 'root',
   'port': 22,
   'global_delay_factor': .1
}

