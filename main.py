from Hologram.HologramCloud import HologramCloud

#Instantiating a hologram instance
hologram = HologramCloud(dict(), network='cellular')

result = hologram.network.connect()
if result == False:
    print ' Failed to connect to cell network'

response_code = hologram.sendMessage("hello, world!")
print hologram.getResultString(response_code)

#Find Location
print hologram.network.location
