<Cabbage>
form caption("OSCSendMulti"), size(890, 420), pluginid("oscsendmulti"), guirefresh(10)

rslider bounds(10, 10, 100, 100), channel("knob1_1"), colour(255, 0, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch1")
rslider bounds(100, 10, 100, 100),channel("knob1_2"), colour(255, 0, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch2")
rslider bounds(200, 10, 100, 100), channel("knob1_3"), colour(255, 0, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch3")
rslider bounds(300, 10, 100, 100), channel("knob1_4"), colour(255, 0, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch4")
rslider bounds(400, 10, 100, 100), channel("knob1_5"), colour(255, 0, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch5")
rslider bounds(500, 10, 100, 100), channel("knob1_6"), colour(255, 0, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch6")
rslider bounds(600, 10, 100, 100), channel("knob1_7"), colour(255, 0, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch7")
rslider bounds(700, 10, 100, 100), channel("knob1_8"), colour(255, 0, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch8")
nslider bounds(810, 20, 50, 50), channel("port1"), range(0, 65535, 7000, 1, 1), velocity(50), text("port_1"), fontcolour(255, 255, 255, 255), colour(200, 0, 0, 255) 

rslider bounds(10, 110, 100, 100), channel("knob2_1"), colour(0, 255, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch1")
rslider bounds(100, 110, 100, 100),channel("knob2_2"), colour(0, 255, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch2")
rslider bounds(200, 110, 100, 100), channel("knob2_3"), colour(0, 255, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch3")
rslider bounds(300, 110, 100, 100), channel("knob2_4"), colour(0, 255, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch4")
rslider bounds(400, 110, 100, 100), channel("knob2_5"), colour(0, 255, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch5")
rslider bounds(500, 110, 100, 100), channel("knob2_6"), colour(0, 255, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch6")
rslider bounds(600, 110, 100, 100), channel("knob2_7"), colour(0, 255, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch7")
rslider bounds(700, 110, 100, 100), channel("knob2_8"), colour(0, 255, 0, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch8")
nslider bounds(810, 120, 50, 50), channel("port2"), range(0, 65535, 7002, 1, 1), velocity(50), text("port_2"), fontcolour(255, 255, 255, 255), colour(0, 200, 0, 255) 

rslider bounds(10, 210, 100, 100), channel("knob3_1"), colour(0, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch1")
rslider bounds(100, 210, 100, 100),channel("knob3_2"), colour(0, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch2")
rslider bounds(200, 210, 100, 100), channel("knob3_3"), colour(0, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch3")
rslider bounds(300, 210, 100, 100), channel("knob3_4"), colour(0, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch4")
rslider bounds(400, 210, 100, 100), channel("knob3_5"), colour(0, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch5")
rslider bounds(500, 210, 100, 100), channel("knob3_6"), colour(0, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch6")
rslider bounds(600, 210, 100, 100), channel("knob3_7"), colour(0, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch7")
rslider bounds(700, 210, 100, 100), channel("knob3_8"), colour(0, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch8")
nslider bounds(810, 220, 50, 50), channel("port3"), range(0, 65535, 7004, 1, 1), velocity(50), text("port_3"), fontcolour(255, 255, 255, 255), colour(0, 0, 200, 255) 

rslider bounds(10, 310, 100, 100), channel("knob4_1"), colour(255, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch1")
rslider bounds(100, 310, 100, 100),channel("knob4_2"), colour(255, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch2")
rslider bounds(200, 310, 100, 100), channel("knob4_3"), colour(255, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch3")
rslider bounds(300, 310, 100, 100), channel("knob4_4"), colour(255, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch4")
rslider bounds(400, 310, 100, 100), channel("knob4_5"), colour(255, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch5")
rslider bounds(500, 310, 100, 100), channel("knob4_6"), colour(255, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch6")
rslider bounds(600, 310, 100, 100), channel("knob4_7"), colour(255, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch7")
rslider bounds(700, 310, 100, 100), channel("knob4_8"), colour(255, 0, 255, 255), range(0, 10, 0, 1, 0.001) increment(0.001) text("ch8")
nslider bounds(810, 320, 50, 50), channel("port4"), range(0, 65535, 7006, 1, 1), velocity(50), text("port_4"), fontcolour(255, 255, 255, 255), colour(200, 0, 200, 255) 

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
    ; retrieve last value
    kData1_1 chnget "knob1_1"
    kData1_2 chnget "knob1_2"
    kData1_3 chnget "knob1_3"
    kData1_4 chnget "knob1_4"
    kData1_5 chnget "knob1_5"
    kData1_6 chnget "knob1_6"
    kData1_7 chnget "knob1_7"
    kData1_8 chnget "knob1_8"
    kPort1 chnget "port1"

    kData2_1 chnget "knob2_1"
    kData2_2 chnget "knob2_2"
    kData2_3 chnget "knob2_3"
    kData2_4 chnget "knob2_4"
    kData2_5 chnget "knob2_5"
    kData2_6 chnget "knob2_6"
    kData2_7 chnget "knob2_7"
    kData2_8 chnget "knob2_8"
    kPort2 chnget "port2"

    kData3_1 chnget "knob3_1"
    kData3_2 chnget "knob3_2"
    kData3_3 chnget "knob3_3"
    kData3_4 chnget "knob3_4"
    kData3_5 chnget "knob3_5"
    kData3_6 chnget "knob3_6"
    kData3_7 chnget "knob3_7"
    kData3_8 chnget "knob3_8"
    kPort3 chnget "port3"

    kData4_1 chnget "knob4_1"
    kData4_2 chnget "knob4_2"
    kData4_3 chnget "knob4_3"
    kData4_4 chnget "knob4_4"
    kData4_5 chnget "knob4_5"
    kData4_6 chnget "knob4_6"
    kData4_7 chnget "knob4_7"
    kData4_8 chnget "knob4_8"
    kPort4 chnget "port4"

    ; send them periodically in case server disconnect / reconnect
    ; FIXME: odd frequency to get around 1Hz (??). With csound 6.11, 0.001 with a print and here with OSC should increase??
    ktrig metro 5
        ; FIXME another oddity, ktrig == 1 does not work (??). But then might send send twice the value??
    if (ktrig < 2) then
        OSCsend_lo ktrig, "localhost", round(kPort1), "/ch/1", "f", kData1_1
        OSCsend_lo ktrig, "localhost", round(kPort1), "/ch/2", "f", kData1_2
        OSCsend_lo ktrig, "localhost", round(kPort1), "/ch/3", "f", kData1_3
        OSCsend_lo ktrig, "localhost", round(kPort1), "/ch/4", "f", kData1_4
        OSCsend_lo ktrig, "localhost", round(kPort1), "/ch/5", "f", kData1_5
        OSCsend_lo ktrig, "localhost", round(kPort1), "/ch/6", "f", kData1_6
        OSCsend_lo ktrig, "localhost", round(kPort1), "/ch/7", "f", kData1_7
        OSCsend_lo ktrig, "localhost", round(kPort1), "/ch/8", "f", kData1_8
    
        OSCsend_lo ktrig, "localhost", round(kPort2), "/ch/1", "f", kData2_1
        OSCsend_lo ktrig, "localhost", round(kPort2), "/ch/2", "f", kData2_2
        OSCsend_lo ktrig, "localhost", round(kPort2), "/ch/3", "f", kData2_3
        OSCsend_lo ktrig, "localhost", round(kPort2), "/ch/4", "f", kData2_4
        OSCsend_lo ktrig, "localhost", round(kPort2), "/ch/5", "f", kData2_5
        OSCsend_lo ktrig, "localhost", round(kPort2), "/ch/6", "f", kData2_6
        OSCsend_lo ktrig, "localhost", round(kPort2), "/ch/7", "f", kData2_7
        OSCsend_lo ktrig, "localhost", round(kPort2), "/ch/8", "f", kData2_8

        OSCsend_lo ktrig, "localhost", round(kPort3), "/ch/1", "f", kData3_1
        OSCsend_lo ktrig, "localhost", round(kPort3), "/ch/2", "f", kData3_2
        OSCsend_lo ktrig, "localhost", round(kPort3), "/ch/3", "f", kData3_3
        OSCsend_lo ktrig, "localhost", round(kPort3), "/ch/4", "f", kData3_4
        OSCsend_lo ktrig, "localhost", round(kPort3), "/ch/5", "f", kData3_5
        OSCsend_lo ktrig, "localhost", round(kPort3), "/ch/6", "f", kData3_6
        OSCsend_lo ktrig, "localhost", round(kPort3), "/ch/7", "f", kData3_7
        OSCsend_lo ktrig, "localhost", round(kPort3), "/ch/8", "f", kData3_8

        OSCsend_lo ktrig, "localhost", round(kPort4), "/ch/1", "f", kData4_1
        OSCsend_lo ktrig, "localhost", round(kPort4), "/ch/2", "f", kData4_2
        OSCsend_lo ktrig, "localhost", round(kPort4), "/ch/3", "f", kData4_3
        OSCsend_lo ktrig, "localhost", round(kPort4), "/ch/4", "f", kData4_4
        OSCsend_lo ktrig, "localhost", round(kPort4), "/ch/5", "f", kData4_5
        OSCsend_lo ktrig, "localhost", round(kPort4), "/ch/6", "f", kData4_6
        OSCsend_lo ktrig, "localhost", round(kPort4), "/ch/7", "f", kData4_7
        OSCsend_lo ktrig, "localhost", round(kPort4), "/ch/8", "f", kData4_8

    endif
    
    ; and send when a value change

    OSCsend_lo kData1_1, "localhost", round(kPort1), "/ch/1", "f", kData1_1
    OSCsend_lo kData1_2, "localhost", round(kPort1), "/ch/2", "f", kData1_2
    OSCsend_lo kData1_3, "localhost", round(kPort1), "/ch/3", "f", kData1_3
    OSCsend_lo kData1_4, "localhost", round(kPort1), "/ch/4", "f", kData1_4
    OSCsend_lo kData1_5, "localhost", round(kPort1), "/ch/5", "f", kData1_5
    OSCsend_lo kData1_6, "localhost", round(kPort1), "/ch/6", "f", kData1_6
    OSCsend_lo kData1_7, "localhost", round(kPort1), "/ch/7", "f", kData1_7
    OSCsend_lo kData1_8, "localhost", round(kPort1), "/ch/8", "f", kData1_8
    
    OSCsend_lo kData2_1, "localhost", round(kPort2), "/ch/1", "f", kData2_1
    OSCsend_lo kData2_2, "localhost", round(kPort2), "/ch/2", "f", kData2_2
    OSCsend_lo kData2_3, "localhost", round(kPort2), "/ch/3", "f", kData2_3
    OSCsend_lo kData2_4, "localhost", round(kPort2), "/ch/4", "f", kData2_4
    OSCsend_lo kData2_5, "localhost", round(kPort2), "/ch/5", "f", kData2_5
    OSCsend_lo kData2_6, "localhost", round(kPort2), "/ch/6", "f", kData2_6
    OSCsend_lo kData2_7, "localhost", round(kPort2), "/ch/7", "f", kData2_7
    OSCsend_lo kData2_8, "localhost", round(kPort2), "/ch/8", "f", kData2_8

    OSCsend_lo kData3_1, "localhost", round(kPort3), "/ch/1", "f", kData3_1
    OSCsend_lo kData3_2, "localhost", round(kPort3), "/ch/2", "f", kData3_2
    OSCsend_lo kData3_3, "localhost", round(kPort3), "/ch/3", "f", kData3_3
    OSCsend_lo kData3_4, "localhost", round(kPort3), "/ch/4", "f", kData3_4
    OSCsend_lo kData3_5, "localhost", round(kPort3), "/ch/5", "f", kData3_5
    OSCsend_lo kData3_6, "localhost", round(kPort3), "/ch/6", "f", kData3_6
    OSCsend_lo kData3_7, "localhost", round(kPort3), "/ch/7", "f", kData3_7
    OSCsend_lo kData3_8, "localhost", round(kPort3), "/ch/8", "f", kData3_8

    OSCsend_lo kData4_1, "localhost", round(kPort4), "/ch/1", "f", kData4_1
    OSCsend_lo kData4_2, "localhost", round(kPort4), "/ch/2", "f", kData4_2
    OSCsend_lo kData4_3, "localhost", round(kPort4), "/ch/3", "f", kData4_3
    OSCsend_lo kData4_4, "localhost", round(kPort4), "/ch/4", "f", kData4_4
    OSCsend_lo kData4_5, "localhost", round(kPort4), "/ch/5", "f", kData4_5
    OSCsend_lo kData4_6, "localhost", round(kPort4), "/ch/6", "f", kData4_6
    OSCsend_lo kData4_7, "localhost", round(kPort4), "/ch/7", "f", kData4_7
    OSCsend_lo kData4_8, "localhost", round(kPort4), "/ch/8", "f", kData4_8
endin

</CsInstruments>
<CsScore>
i 1 0 [3600*24*7]
</CsScore>
</CsoundSynthesizer>

