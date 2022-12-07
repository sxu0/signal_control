import time

import pyvisa

resources = pyvisa.ResourceManager('')
resources.list_resources()

synthesizer = resources.open_resource('GPIB::19::INSTR')
print(synthesizer.query('*IDN?'))

# frequency sweep implementation
synthesizer.write('POW:LEV -5 DBM')
synthesizer.write('FREQ:CW 9.661817 GHZ; STEP 0.049899 GHZ')
for i in range(1, 101):
    synthesizer.write('FREQ:CW UP')
    time.sleep(2)
    # take one HiSRAMS sample (controlled by HiSRAMS computer)
synthesizer.close()
