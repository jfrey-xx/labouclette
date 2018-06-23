<Cabbage>
form caption("OSCSend"), size(410, 300), pluginid("oscsend"), guirefresh(10)

rslider bounds(10, 10, 100, 100), channel("knob1"), colour(255, 0, 0, 255), range(-5, 5, 0, 1, 0.01) increment(0.001) text("ch1")
rslider bounds(100, 10, 100, 100),channel("knob2"), colour(255, 0, 0, 255), range(-5, 5, 0, 1, 0.01) increment(0.001) text("ch2")
rslider bounds(200, 10, 100, 100), channel("knob3"), colour(255, 0, 0, 255), range(-5, 5, 0, 1, 0.01) increment(0.001) text("ch3")
rslider bounds(300, 10, 100, 100), channel("knob4"), colour(255, 0, 0, 255), range(-5, 5, 0, 1, 0.01) increment(0.001) text("ch4")

rslider bounds(10, 120, 100, 100), channel("knob5"), colour(255, 0, 0, 255), range(-5, 5, 0, 1, 0.01) increment(0.001) text("ch5")
rslider bounds(100, 120, 100, 100),channel("knob6"), colour(255, 0, 0, 255), range(-5, 5, 0, 1, 0.01) increment(0.001) text("ch6")
rslider bounds(200, 120, 100, 100), channel("knob7"), colour(255, 0, 0, 255), range(-5, 5, 0, 1, 0.01) increment(0.001) text("ch8")
rslider bounds(300, 120, 100, 100), channel("knob8"), colour(255, 0, 0, 255), range(-5, 5, 0, 1, 0.01) increment(0.001) text("ch8")

nslider bounds(150, 230, 100, 50), channel("port"), range(0, 65535, 7000, 1, 1), velocity(50), text("OSC output port"), fontcolour(255, 255, 255, 255), colour(0, 100, 255, 255) 

</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-dm0 -n 
</CsOptions>
<CsInstruments>
sr 	= 	480000
ksmps 	= 	32
nchnls 	= 	0
0dbfs	=	1


instr 1
kData1 chnget "knob1"
kData2 chnget "knob2"
kData3 chnget "knob3"
kData4 chnget "knob4"
kData5 chnget "knob5"
kData6 chnget "knob6"
kData7 chnget "knob7"
kData8 chnget "knob8"
kPort chnget "port"

OSCsend_lo kData1, "localhost", round(kPort), "/ch/1", "f", kData1
OSCsend_lo kData2, "localhost", round(kPort), "/ch/2", "f", kData2
OSCsend_lo kData3, "localhost", round(kPort), "/ch/3", "f", kData3
OSCsend_lo kData4, "localhost", round(kPort), "/ch/4", "f", kData4
OSCsend_lo kData5, "localhost", round(kPort), "/ch/5", "f", kData5
OSCsend_lo kData6, "localhost", round(kPort), "/ch/6", "f", kData6
OSCsend_lo kData7, "localhost", round(kPort), "/ch/7", "f", kData7
OSCsend_lo kData8, "localhost", round(kPort), "/ch/8", "f", kData8

endin

</CsInstruments>
<CsScore>
i 1 0 [3600*24*7]
</CsScore>
</CsoundSynthesizer>

