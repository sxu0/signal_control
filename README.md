Sources
-------
https://hackaday.com/2016/11/16/how-to-control-your-instruments-from-a-computer-its-easier-than-you-think/

2022-12-08 Operation Notes
--------------------------
* 0 dBm setting on signal generator + {20 dBm + 10 dBm} attenuators hooked up --> measured -33 dBm on power meter (extra attenuation may come from the wire)
* 7 power settings * 100 frequencies = 700 samples desired
* 707 samples total including gaps for power change
* for 0.5 s integration time, 2.5 s delay after each power change & after each frequency change --> total time is ~29.5 min
* for 1.0 s integration time, 3.0 s delay after each power change & after each frequency change --> total time is ~35.4 min
