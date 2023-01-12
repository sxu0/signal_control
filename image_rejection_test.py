import time

import pandas as pd
import pyvisa

band = 54
pol = 's'
fft = 0
int_time = 0.5

if band == 54:
    if pol == 's':
        if fft == 0:
            lookup = 1
        elif fft == 1:
            lookup = 2
    elif pol == 'd':
        lookup = 3
elif band == 183:
    if pol == 's':
        if fft == 0:
            lookup = 4
        elif fft == 1:
            lookup = 5
    elif pol == 'd':
        lookup = 6

df = pd.read_csv('test_tones.csv', header=None, skiprows=3)
test_tones = df.iloc[:,lookup] / 1000  # convert MHz to GHz

power_levels = [0, 5, 10, 15]  # with 80 dBm of attenuators
# power_levels = [0, 5, 10]  # with 60 dBm of attenuators

resources = pyvisa.ResourceManager('')
print(resources.list_resources())

synthesizer = resources.open_resource('GPIB::19::INSTR')
print(synthesizer.query('*IDN?'))

# frequency sweep implementation
synthesizer.write('OUTP:STAT ON')  # power on
# set breakpoint at next line to manually sync each outer loop with bash script on HiSRAMS computer
for j in range(len(power_levels)):
    synthesizer.write('POW:LEV %f DBM' %(power_levels[j]))  # set power level
    time.sleep(2 + int_time)
    for i in range(len(test_tones)):
        print(i)
        synthesizer.write('FREQ:CW %f GHZ' %(test_tones[i]))  # set freq
        time.sleep(2 + int_time)
        # take one HiSRAMS sample (controlled by HiSRAMS computer)
synthesizer.write('OUTP:STAT OFF')  # power off
synthesizer.close()
