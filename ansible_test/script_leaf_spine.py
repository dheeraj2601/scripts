import os
import sys
import pickle

# python script_leaf_spine.py 2 4 7
# inputs : no of cores, spines and leafs

#os.chdir(sys.argv[1])
core = sys.argv[1]
spine = sys.argv[2]
leaf = sys.argv[3]


# Generate ASN for leaf, spine and core

# Private ASN : 64512 to 65535 (1024 in total)
# Core 64512 - 64525 (13)
# Spine 64526 - 65000 (474)
# Leaf 65001 - 65535 (535 can be repeated in ToR)
# Can use Four-Octet ASN

leaf_asn = []
spine_asn = []
core_asn = []

content = []
temp_content = []

for i in range(0, int(leaf)):
  leaf_asn.append(65001+int(i))

for i in range(0, int(spine)):
  spine_asn.append(64526+int(i))


for i in range(0, int(core)):
  core_asn.append(65412+int(i))

router = ""
profile = ""
local_ASN = 0
leaf_port = ""
leaf_port_local_ip = ""
spine_port_remote_ip = ""
remote_ASN = ""

def template_funct1 (hostname, profile, local_ASN):

  str1 = "hostname: "+hostname

  for line in content:
    if str1 in line:
      return
      
  content.append(" - hostname: "+hostname)
  content.append("   profile: "+profile)
  content.append("   local_ASN: "+str(local_ASN))
  content.append("   links:")

def template_funct2 (hostname, leaf_port, leaf_port_local_ip, spine_port_remote_ip, remote_ASN):

  str1 = " - hostname: "+hostname

  try:
    index1 = content.index (str1)
  except ValueError:
    return

  content.insert(index1+4, "     - leaf_port: "+leaf_port)
  content.insert(index1+5, "       leaf_port_local_ip: "+leaf_port_local_ip)
  content.insert(index1+6, "       spine_port_remote_ip: "+spine_port_remote_ip)
  content.insert(index1+7, "       remote_ASN: "+str(remote_ASN))
   
content.append("---")
content.append("switches:")

#leaf with spine
count = 1
ip_addr_leaf = "192.168."
# leaf elements : 
for leaf_num, i in enumerate(leaf_asn, start=1): # looping leaf
  header_check = 1
  for num, j in enumerate (spine_asn, start=1): # looping spine 
    
    router = "router"+str(leaf_num)
    profile = "leaf"
    local_ASN = i
    leaf_port = "eth"+str(num)
    leaf_port_local_ip = ip_addr_leaf+str(count)+".1"
    spine_port_remote_ip = ip_addr_leaf+str(count)+".0"
    remote_ASN = j

    if header_check == 1:
      template_funct1 (router, profile, local_ASN)
    template_funct2 (router, leaf_port, leaf_port_local_ip, spine_port_remote_ip, remote_ASN)

    count += 1
    header_check += 1

  count = leaf_num * 10 + 1 

  

# core with spine
# hear, leaf_port_local_ip is alias for spine_port_local_ip
#       spine_port_local_ip is alias for core_port_local_ip

count = 601
ip_addr_core = "172.16."
# leaf elements : 
for core_num, i in enumerate (core_asn, start=1): # looping spine 
  header_check = 1
  for spine_num, j in enumerate(spine_asn, start=1): # looping core
     
    router = "router"+str(core_num + 600)
    profile = "core"
    local_ASN = i
    leaf_port = "eth"+str(spine_num)
    leaf_port_local_ip = ip_addr_core+str(count - 600)+".0"
    spine_port_remote_ip = ip_addr_core+str(count - 600)+".1"
    remote_ASN = j

    if header_check == 1:
      template_funct1 (router, profile, local_ASN)
    template_funct2 (router, leaf_port, leaf_port_local_ip, spine_port_remote_ip, remote_ASN)

    count += 1 
    header_check += 1

  count = core_num * 10 + 601 

#spine with leaf

count = 501
ip_addr_leaf = "192.168."
spine_count = 0
num2 = 0
for spine_num, i in enumerate(spine_asn, start=1): # looping leaf
  header_check = 1
#spine_count not used . Assuming max 10 spines .
  spine_count = 0
  for num, j in enumerate (leaf_asn, start=0): # looping spine 
    
    router = "router"+str(spine_num + 500)
    profile = "spine"
    local_ASN = i
    leaf_port = "eth"+str(num+1)
    leaf_port_local_ip = ip_addr_leaf+str(count - 500 + (10 * num + num2))+".0"
    spine_port_remote_ip = ip_addr_leaf+str(count - 500 + (10 * num + num2))+".1"
    remote_ASN = j

    if header_check == 1:
      template_funct1 (router, profile, local_ASN)
    template_funct2 (router, leaf_port, leaf_port_local_ip, spine_port_remote_ip, remote_ASN)

    #count += 1
    header_check += 1
    spine_count += len(spine_asn)
  num2 += 1

#spine with core
count = 501
ip_addr_core = "172.16."
# leaf elements : 
num2 = 0
for spine_num, i in enumerate(spine_asn, start=1): # looping spine
  header_check = 1
# assuming max 10 spines
  for num, j in enumerate (core_asn, start=0): # looping core
     
    router = "router"+str(spine_num + 500)
    profile = "spine"
    local_ASN = i
    leaf_port = "eth"+str(num + 11)
    leaf_port_local_ip = ip_addr_core+str(count - 500 + (10 * num + num2))+".1"
    spine_port_remote_ip = ip_addr_core+str(count- 500 + (10 * num + num2))+".0"
    remote_ASN = j

    if header_check == 1:
      template_funct1 (router, profile, local_ASN)
    template_funct2 (router, leaf_port, leaf_port_local_ip, spine_port_remote_ip, remote_ASN)

    #count += 1 
    header_check += 1
  num2 += 1

with open('main123.yml', 'w') as f:
    for item in content:
        f.write("%s\n" % item)
