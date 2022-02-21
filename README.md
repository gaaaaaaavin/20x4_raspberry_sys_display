# Installation:

- type into terminal
> sudo git clone https://github.com/gaaaaaaavin/20x4_raspberry_sys_display.git

> sudo nano startup.sh

- copy-paste the following:
> #!/bin/sh

> cd /home/pi/20x4_raspberry_sys_display

> sudo python lcd_main.py

- CTRL + S to save

> sudo chmod u+x startup.sh

> sudo crontab -e
> 
- paste this on the last line
> @reboot sudo bash /home/pi/startup.sh

- CTRL + S to save
> sudo reboot
