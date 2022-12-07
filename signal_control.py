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

freq_start = test_tones[0]
freq_step = test_tones[1] - test_tones[0]

resources = pyvisa.ResourceManager('')
print(resources.list_resources())

synthesizer = resources.open_resource('GPIB::19::INSTR')
print(synthesizer.query('*IDN?'))

# frequency sweep implementation
synthesizer.write('POW:LEV -5 DBM')
synthesizer.write('FREQ:CW %f GHZ; STEP %f GHZ' %(freq_start, freq_step))
for i in range(len(test_tones)-1):
    time.sleep(3)
    # take one HiSRAMS sample (controlled by HiSRAMS computer)
    synthesizer.write('FREQ:CW UP')
synthesizer.close()
