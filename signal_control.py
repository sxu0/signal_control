import time

import pandas as pd
import pyvisa

band = 54
pol = 's'
fft = 0

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

resources = pyvisa.ResourceManager('')
print(resources.list_resources())

synthesizer = resources.open_resource('GPIB::19::INSTR')
print(synthesizer.query('*IDN?'))

# frequency sweep implementation
synthesizer.write('POW:LEV -5 DBM')
for i in range(len(test_tones)):
    print(i)
    synthesizer.write('FREQ:CW %f GHZ' %(test_tones[i]))
    time.sleep(3)
    # take one HiSRAMS sample (controlled by HiSRAMS computer)
synthesizer.close()
