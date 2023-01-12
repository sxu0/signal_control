import time

import pandas as pd
import pyvisa

int_time = 0.5

LOOKUP = 6  # {183 GHz band, dual pol, either fft} test tones

df = pd.read_csv('test_tones.csv', header=None, skiprows=3)
test_tones = df.iloc[:,LOOKUP] / 1000  # convert MHz to GHz
test_tones = test_tones[75:]

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
    time.sleep(2)
    for i in range(len(test_tones)):
        print(i)
        synthesizer.write('FREQ:CW %f GHZ' %(test_tones[i]))  # set freq
        time.sleep(30 * int_time)
        # take one HiSRAMS sample (controlled by HiSRAMS computer)
synthesizer.write('OUTP:STAT OFF')  # power off
synthesizer.close()
