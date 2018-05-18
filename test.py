 
from mididings import *
from mididings.extra.inotify import AutoRestart
#from mididings.extra import MemorizeScene

from midi2ext import *

# name of the input port which should be associated to transport controls
control_port = "controls"
# rest of keyboard
keyboard_port = "keyboard"



config(
    backend='jack-rt',
    client_name='example',
    out_ports = ['synth', 'extra'],
    in_ports = [(keyboard_port, 'system:midi_capture_1'), (control_port, 'system:midi_capture_4')],

)

hook(
    # auto-restart: edit and save this file in a text editor while it's
    # running, and mididings will automatically restart itself (!)
    #AutoRestart(),
    # memorize scene: every time this script is restarted, it automatically
    # comes back with the previously active scene
    #MemorizeScene('scene.txt')
)


# Output port_name, channel, program


#organ   = Output('synth',   3)

# pass all event related to keyboard port
out_keyboard_all = PortFilter(keyboard_port ) >> Output('synth')

# meant to use pad for launching clips
out_seq64_pad = PortFilter(keyboard_port ) >> Filter(NOTEON) >> Call(midi2ext_pad)

# meant to pass only buttons related to controls
out_control = PortFilter(control_port) >> Filter(NOTEON) >> Call(midi2ext_TC)

run(
    scenes = {
        # scene 1: play piano.
        # this will switch the sampler to program 1, then route all events
        # to it
        #1:  piano,
        1: Print() >> Velocity(fixed=0) >> out_keyboard_all,

        # scene 2: play organ, transposed one octave down
        2: [out_control, Velocity(fixed=1) >> out_keyboard_all],

        # scene 3: to seq64
        3: [out_control , out_seq64_pad],
        
        # scene 4: same but transposed to reach for the others patches
        4: [out_control , Transpose(16) >> out_seq64_pad],


    },

    # control patch: use program changes on channel 16 to switch between
    # scenes
    control = Filter(PROGRAM) >> SceneSwitch(),

    # preprocessing: filter out program changes, everything else is sent to
    # the current scene
    pre = ~Filter(PROGRAM),
)
