import subprocess
from subprocess import PIPE
import argparse
from ipaddress import ip_address
import re

defaultIDs = 'measureID.txt'
defaultIP = '149.149.2.70'
defaultKey = '9e6d5b6d-32ef-4836-84a7-7814e7385294'
defaultDesc = 'Chs9LKVsSReijF5iMMGDJISgE6tLvlThcVCPx0sebx4NRbfXOKrFIJUbys@^@Gbu9ZuNq^X8A0FH2ZZmW6Oxb3ITMyB5sz^N8HLv6aspNwqVBPzt5P2PYZp@sPsEGFp4qGTAVWfEQPf6ePPs4s8qT%bx6MQ**mvic9EmyK7eWHJm9Ki%4n@ODTYiUL4O38UMRbyPWjzpk6RjNZ0m%X%nnbOZZk4n'

def probesRegex(arg_value, pat=re.compile(r"[0-9]+(,[0-9]+)*")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

def from_probes_user(args):
    if args.interval > 0:
        print("\nFrom-probes Measurement Sent with an Interval\n")
        proc = subprocess.Popen("ripe-atlas measure {} --target {} --auth {} --interval {} --from-probes {} --description {}".format(args.measurement,args.target,args.authentication,args.interval,args.probes_user,args.description), stdout=PIPE, stderr=PIPE, shell=True)
        print("The commandline is {}".format(proc.args))
    else:
        print("\nFrom-probes Measurement Sent without an Interval\n")
        subprocess.Popen("ripe-atlas measure {} --target {} --auth {} --from-probes {} --description {} --no-report".format(args.measurement,args.target,args.authentication,args.probes_user,args.description), stdout=PIPE, stderr=PIPE, shell=True)

def from_probes_file(args):
    inFile = open(args.probes_file)
    f = inFile.read().splitlines()
    x = ','.join(f)

    if args.interval > 0:
        print("\nFrom file Measurement Sent with an Interval\n")
        proc = subprocess.Popen("ripe-atlas measure {} --target {} --auth {} --interval {} --from-probes {} --description {}".format(args.measurement,args.target,args.authentication,args.interval,x,args.description), stdout=PIPE, stderr=PIPE, shell=True)
        print("The commandline is {}".format(proc.args))
    else:
        print("\nFrom file Measurement Sent without an Interval\n")
        subprocess.Popen("ripe-atlas measure {} --target {} --auth {} --from-probes {} --description {} --no-report".format(args.measurement,args.target,args.authentication,x,args.description), stdout=PIPE, stderr=PIPE, shell=True)

def from_area(args):
    if args.interval > 0:
        print("\nFrom-area Measurement Sent with an Interval\n")
        subprocess.Popen("ripe-atlas measure {} --target {} --auth {} --interval {} --from-area {} --probes {} --description {}".format(args.measurement,args.target,args.authentication,args.interval,args.from_area,args.probe_amount,args.description), stdout=PIPE, stderr=PIPE, shell=True)
    else:
        print("\nFrom-area Measurement Sent without an Interval\n")
        subprocess.Popen("ripe-atlas measure {} --target {} --auth {} --from-area {} --probes {} --description {} --no-report".format(args.measurement,args.target,args.authentication,args.from_area,args.probe_amount,args.description), stdout=PIPE, stderr=PIPE, shell=True)

parser=argparse.ArgumentParser(description="run the 'ripe-atlas' command")

parser.add_argument('measurement', choices=['ping', 'traceroute', 'http', 'dns', 'ntp', 'sslcert'], help="type of measurement to send to target")
parser.add_argument('-t','--target', type=ip_address, default=defaultIP, help='URL or IP') #implement default as leo IP
parser.add_argument('-a','--authentication', default=defaultKey, help="ripe-atlas authentication key")
parser.add_argument('-i', '--interval', type=int, default=0, help="amount of time in seconds between measurements, exclude for one-off")
parser.add_argument('-d', '--description', default=defaultDesc, help="type a unique description so that you can easily find your measurements on ripe-atlas")

subparsers = parser.add_subparsers(dest='subparsers', help="send measurements either from list of probes or a specific number of probes from a region")
subparsers.required = True

#Implement input as optional text file
parser_a = subparsers.add_parser('from_probes_user', help="enter specific probe IDs")
parser_a.add_argument('probes_user', type=probesRegex, help="string of probes separated by commas with no spaces. Ex: '1003191,2685'")
parser_a.set_defaults(func=from_probes_user)

parser_b = subparsers.add_parser('from_probes_file', help="enter a file to take probe IDs from")
parser_b.add_argument('-f', '--probes_file', default=defaultIDs, help="a file containing probe IDs on seperate lines") #default will be probe IDs file name
parser_b.set_defaults(func=from_probes_file)

parser_c = subparsers.add_parser('from_area', help="enter an area and the amount of probes you want")
parser_c.add_argument('from_area', choices=['South-East', 'North-East', 'South-Central', 'North-Central', 'West'], help="select region from ripe-atlas")
parser_c.add_argument('probe_amount', type=int, help="integer for number of probes from an area")
parser_c.set_defaults(func=from_area)

args = parser.parse_args()
args.func(args)