
from .x import joke

def main():
  print('foo = ', 2)
  print(joke())

if __name__ == '__main__':
  main()

  device = AtlasI2C()   # creates the I2C port object, specify the address or bus if necessary
  
  device.set_i2c_address(99)
  print(device.query("R"))



