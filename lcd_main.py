from bs4 import BeautifulSoup as bs
import requests
import lcddriver
from subprocess import *
import time
from datetime import datetime


# Weather
def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item
    return str
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"

def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    soup = bs(html.text, "html.parser")
    # store all results on this dictionary
    result = {}
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text

    return result

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return str(output)[2:]


def long_string(display, text='', num_line=1, num_cols=20):
    if len(text) > num_cols:
        lcd.lcd_display_string(text[:num_cols], num_line)
        time.sleep(1)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print, num_line)
            time.sleep(0.1)
        time.sleep(1)
    else:
        lcd.lcd_display_string(text, num_line)

    

# Internal IP address
cmd1 = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1 | head -n 1"

# External IP address
cmd2 = "wget http://ipinfo.io/ip -qO -"

# Rpi CPU temperature
cmd3 = "cat /sys/class/thermal/thermal_zone0/temp | awk 'NR == 1 { print $1 / 1000}' | cut -c -4"

# Rpi GPU temperature
cmd4 ="/opt/vc/bin/vcgencmd measure_temp | cut -c 6- | cut -c -4"

# CPU usage
cmd5 = "sudo bash cpu_usage.sh"

# Memory usage 
cmd6 = "free | awk 'FNR == 3 {print $3/($3+$4)*100}' | cut -c -3"

# Get free disk space
cmd7 = "df -h | sed -n 2p | awk '{ printf $4 }'"

# Calculate RX rate
cmd8 ="sudo bash rx.sh"

# Calculate TX rate
cmd9 ="bash tx.sh"


lcd = lcddriver.lcd()
lcd.lcd_clear()
#lcd_state(time1)
lcd.lcd_display_string("       Hello!",1)
lcd.lcd_display_string("Give us a moment.",4)

long_string(lcd,"We're just starting up",2)



night=["20","21","22","23","00","01","02","03","04","05","06","07"]
#lcd.lcd_display_string("Welcome", 1)
#time.sleep(2)
while True:
    x = datetime.now()
    time1="02"

    
    try:
        URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
        data = get_weather_data(URL)
        weatherlcd=data['weather_now'].title()+" "+data['temp_now']+"C"
        weatherlcd=(convertTuple(weatherlcd))
    except:
        weatherlcd="Weather not available. Check internet and restart."
    lcd.lcd_clear()

    lcd.lcd_display_string(x.strftime("%B %d, %Y"),1)
    lcd.lcd_display_string(x.strftime("%u/7      %A"),2)
    lcd.lcd_display_string(x.strftime("%I:%M:%S %p  %z"), 3)
    long_string(lcd,weatherlcd,4)
    

    
    
    

#    tempcpu = run_cmd(cmd3)
 #   usagecpu = run_cmd(cmd5)
  #  tempgpu = run_cmd(cmd4)
   # usagemem = run_cmd(cmd6)
    #time.sleep(2)
#    lcd.lcd_clear()
 #   lcd.lcd_display_string("CPU Temp:  "+tempcpu[:-3]+" 'C",1)
  #  lcd.lcd_display_string("CPU Usage: "+usagecpu[:-5]+"%",2)
   # lcd.lcd_display_string("GPU Temp:  "+tempgpu[:-3]+" 'C",3)
    #lcd.lcd_display_string("RAM Usage: "+usagemem[:-4]+"%",4)
    
    inet = run_cmd(cmd1)
    exnet= run_cmd(cmd2)
    rx = run_cmd(cmd8)
    tx = run_cmd(cmd9)
    time.sleep(2)
    lcd.lcd_clear()

    lcd.lcd_display_string("Local: "+inet[:-3], 1)
#    lcd.lcd_display_string(exnet[:-1], 2)
    lcd.lcd_display_string("Download: "+rx[:-3]+" KB/s", 3)
    lcd.lcd_display_string("Upload:   "+tx[:-3]+" KB/s", 4)
    long_string(lcd,"Current Upload & Download Speed:  ",2)
    
