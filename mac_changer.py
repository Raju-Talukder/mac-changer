#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC Address")
    parser.add_option("-m", "--mac", dest="newMac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.newMac:
        parser.error("[-] Please specify an new MAC, use --help for more info")
    return options


def change_mac(interface, newMac):
    print("[+] Changing MAC address for " + interface + " to " + newMac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether"])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfigResult = subprocess.check_output(["ifconfig", interface])
    macAddressSearchResult = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfigResult))
    if macAddressSearchResult:
        return macAddressSearchResult.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()
currentMac = get_current_mac(options.interface)
print("Current MAC = " + str(currentMac))
change_mac(options.interface, options.newMac)
currentMac = get_current_mac(options.interface)
if currentMac == options.newMac:
    print("[+] MAC address was successfully changed to " + currentMac)
else:
    print("[-] MAC address did not changed.")
