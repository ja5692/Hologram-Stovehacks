from Hologram.HologramCloud import HologramCloud

#Instantiating a hologram instance
hologram = HologramCloud(dict(), network='cellular')

result = hologram.network.connect()
if result == False:
    print ' Failed to connect to cell network'

#Find Location
location = hologram.network.location
print "Altitude:"
print location.altitude
print "Longitude:"
print location.longitude
print "Latitude:"
print location.latitude
print "Uncertainty:"
print location.uncertainty
print "Time:"
print location.time

#Upload Databa
hologram.sendMessage(location)

#Disconnect
hologram.network.disconnect()
