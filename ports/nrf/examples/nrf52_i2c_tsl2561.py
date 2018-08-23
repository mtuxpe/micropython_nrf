import machine
from time import sleep_ms
from machine import RTCounter
from board import LED

global rtc
scl = machine.Pin.board.P27
sda = machine.Pin.board.P26
i2c = machine.I2C(0,scl,sda)
command = const(0x80)
ctl_poweron = const(0x03)
ctl_poweroff = const(0x00)
reg_timing = const(0x1)
ch0 = bytearray([0,0])
ch1 = bytearray([0,0])

def rtcint(timer_id):
  LED(1).on()
  i2c.writeto(57,bytearray([command,ctl_poweron]))
  sleep_ms(500)
  i2c.writeto(57,bytearray([command|0x20|0x0e]))
  i2c.readfrom_into(57,ch1)
  i2c.writeto(57,bytearray([command|0x20|0x0c]))
  i2c.readfrom_into(57,ch0)
  i2c.writeto(57,bytearray([command,ctl_poweroff]))
  tot = int.from_bytes(ch0,'little')
  ir = int.from_bytes(ch1,'little')
  print ('Total',tot)
  print ('IR: ',ir)
  LED(1).off()
  
def init( param):
  if param == 1:
    i2c = machine.I2C(0,scl,sda)
    i2c.writeto(57,bytearray([command,ctl_poweron]))
    i2c.writeto(57,bytearray([command|1,0]))
    i2c.writeto(57,bytearray([command|1,0x10]))
    i2c.writeto(57,bytearray([command,ctl_poweroff]))
    rtc = RTCounter(1, period=50, mode=RTCounter.PERIODIC, callback=rtcint)
    rtc.start()
  elif param == 0:
    rtc.stop()
    
def rdchn():
  init(1)

def detect():
  i2c.writeto(57,bytearray([0x0a]))


  
