from spidev import SpiDev

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    def read(self, channel):
#print channel
 #       cmd1 = 4 | 2 | (( channel & 4) >> 2)
#	print cmd1
  #      cmd2 = (channel & 3) << 6
#
 #       adc = self.spi.xfer2([cmd1, cmd2, 0])
#	print adc
  #      data = ((adc[1] & 15) << 8) + adc[2]'''
	adc=self.spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3)<<8)+adc[2]
#	print data
    	return data
    def read_7(self,channel):
	adc= self.spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3)<<8)+adc[2]
	#print data
	return data
           
    def close(self):
        self.spi.close()
