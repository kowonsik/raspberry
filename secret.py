
def secret(plug_id):
	plug_secret = (plug_id * 2654435761) % 8192
	return plug_secret

for gw in range(10) :
    home = gw+1001
    home1 = home*100 + 1
    home3 = home*100 + 3
    home4 = home*100 + 4
    print "HOME=", home, 
    print map(secret, [home1, home3, home4])
    print " "

