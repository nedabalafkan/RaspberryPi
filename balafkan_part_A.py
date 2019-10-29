#installation requirements to run on a Raspberry Pi
sudo python -i

sudo apt-get update
sudo apt-get install python-pip
sudo pip install pibrella

# addressing GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO pins


import pibrella
# Part A
#making sure that the Pibrella is working with the following queries

pibrella.light.red.on()
pibrella.buzzer.note(1)
sleep(30)
pibrella.buzzer.note(2)
pibrella.light.red.off()
pibrella.light.amber.high(2,3)
pibrella.light.green.pulse(2,3)
pibrella.buzzer.note(3)
pibrella.light.green.fade(0,100,5)
pibrella.light.red.pulse(2,4)