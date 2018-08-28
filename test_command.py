 
from mididings import config, hook, run, PortFilter, Print, Output, Filter, Call, SceneSwitch, Process, Velocity, Transpose, NOTEON, PROGRAM, CTRL
#from mididings import *
from mididings.event import NoteOnEvent
#from mididings.extra.inotify import AutoRestart
#from mididings.extra import MemorizeScene

from midi2ext import midi2ext_pad, midi2ext_TC
import remoteOSC

import state


# trying to cnontrol seq64 with code25
# some inspiration from https://gist.oonnnoo.com/milkmiruku/2afb362b060b40f7575b8854220ad82e

# FIXME: seq64 seems to handle poorly two states at the same time on same pattern (e.g. midi through and record, or launch clip that create sound with midi through), hence the sync mechanism and multiple states is not used

# name of the input port which should be associated to transport controls
control_port = "controls"
# rest of keyboard
keyboard_port = "keyboard"


config(
    backend='jack-rt',
    client_name='example',
    out_ports = ['synth', 'extra'],
   # in_ports = [(keyboard_port, 'system:midi_capture_1'), (control_port, 'system:midi_capture_4')],
    in_ports = [keyboard_port, control_port],

)

hook(
    # auto-restart: edit and save this file in a text editor while it's
    # running, and mididings will automatically restart itself (!)
    #AutoRestart(),
    # memorize scene: every time this script is restarted, it automatically
    # comes back with the previously active scene
    #MemorizeScene('scene.txt')
)
    
# give feedback to possible OSC ui
guiOSC = remoteOSC.RemoteOSC()     
# connect to ardour OSC interface and its default OSC port
ardourOSC = remoteOSC.RemoteOSC(client_port=3819) 
# same for custom zynthian wrapper
zynthianOSC = remoteOSC.RemoteOSC(client_port=4567)                
               
        
# HOTFIX: these notes produce sounds, go through computer keyboard instead
launch_state = state.State("launch", 3, note_toggle = 0, totoggle = True, keyboard_toggle = False, remoteOSC = guiOSC)
midithrough_state = state.State("through", 15, note_on = 32, note_off = 33, alone = True, velocity = True, restore_on = True, reset_off = True, remoteOSC = guiOSC)
#record_state = State("record", 14, note_on = 34, note_off = 35, alone = True, velocity = True, sync = [midithrough_state])
record_state = state.State("record", 14, note_on = 34, note_off = 35, alone = True, velocity = True, restore_on = True, reset_off = True, remoteOSC = guiOSC)
# will set the recording to overwrite -- recording that should be set separatly
reset_state = state.State("reset", 16, note_toggle = 36, note_on = 37, note_off = 38, totoggle = True, restore_on = True, reset_off = True, velocity = True)
# all activated states will trigger...
list_states = [launch_state, record_state, midithrough_state, reset_state]


# here modifiers, not associated to pads
# hack: this modifier is just to capture pad actions, will not actually "modify" anything
glaunch_modifier = state.Modifier("glaunch", 17, totoggle = True, note_toggle = 64)
# will set the group learn modifier
glearn_modifier = state.Modifier("glearn", 18, note_activate = 46, note_deactivate = 47, totoggle = True, note_toggle = 64)
# will set the queue (simple) modifier
queue_modifier = state.Modifier("queue", 9, note_activate = 40, note_deactivate = 41)
# will set the solo (simple) modifier
replace_modifier = state.Modifier("replace", 19, note_activate = 49, note_deactivate = 50)
# will set the snapshot (simple) modifier
snapshot_modifier = state.Modifier("snapshot", 20, note_activate = 52, note_deactivate = 53)

# control for zynthian
zynthian_encoder_1 = state.Modifier("zynthian_but0", 58, remoteOSC = zynthianOSC, osc_activate = "/zyn/encoder/inc", osc_deactivate = "/zyn/encoder/dec", osc_arg = 0, osc_send_val = True, cc_relative = True)
zynthian_encoder_2 = state.Modifier("zynthian_but0", 60, remoteOSC = zynthianOSC, osc_activate = "/zyn/encoder/inc", osc_deactivate = "/zyn/encoder/dec", osc_arg = 1, osc_send_val = True, cc_relative = True)
zynthian_encoder_3 = state.Modifier("zynthian_but0", 59, remoteOSC = zynthianOSC, osc_activate = "/zyn/encoder/inc", osc_deactivate = "/zyn/encoder/dec", osc_arg = 2, osc_send_val = True, cc_relative = True)
zynthian_encoder_4 = state.Modifier("zynthian_but0", 61, remoteOSC = zynthianOSC, osc_activate = "/zyn/encoder/inc", osc_deactivate = "/zyn/encoder/dec", osc_arg = 3, osc_send_val = True, cc_relative = True)
#zynthian_button_1 = state.Modifier("zynthian_but0", 17, remoteOSC = zynthianOSC, osc_activate = "/zyn/press", osc_deactivate = "/zyn/release", osc_arg = 0)
zynthian_button_2 = state.Modifier("zynthian_but0", 28, remoteOSC = zynthianOSC, osc_activate = "/zyn/press", osc_deactivate = "/zyn/release", osc_arg = 1)
zynthian_button_3 = state.Modifier("zynthian_but0", 29, remoteOSC = zynthianOSC, osc_activate = "/zyn/press", osc_deactivate = "/zyn/release", osc_arg = 2)
zynthian_button_4 = state.Modifier("zynthian_but0", 30, remoteOSC = zynthianOSC, osc_activate = "/zyn/press", osc_deactivate = "/zyn/release", osc_arg = 3)

# concatenate everything to check -- patterns, if any associated, will only be processed by the first active. however  something like queue (only modifier, no notes associated to patterns) will not interfere
list_modifiers = [glaunch_modifier, glearn_modifier, queue_modifier, replace_modifier, snapshot_modifier, zynthian_encoder_1, zynthian_encoder_2, zynthian_encoder_3, zynthian_encoder_4, zynthian_button_2, zynthian_button_3, zynthian_button_4]

# then here deal with transport controls -- NB: we don't cate about "pause"
play_control = state.Modifier("play", 94, note_activate = 55)
stop_control = state.Modifier("stop", 93, note_activate = 56)
# these ones are special, sending messages to ardour
click_control = state.Modifier("click", 95, remoteOSC = ardourOSC, osc_activate = "/toggle_click")
gotostart_control = state.Modifier("goto_start", 91, remoteOSC = ardourOSC, osc_activate = "/goto_start")
gotoend_control = state.Modifier("goto_end", 92, remoteOSC = ardourOSC, osc_activate = "/goto_end")

list_TC = [play_control, stop_control, click_control, gotoend_control, gotostart_control]
        
# pass all event related to keyboard port
out_keyboard_all = PortFilter(keyboard_port ) >> Print() >> Output('synth', 1)
# pass all event related to control to dedicated port, with specific channel
out_command = PortFilter(control_port ) >> Print() >> Output('extra', 14)

# meant to use pad for launching clips
out_seq64_pad = PortFilter(keyboard_port ) >> Filter(NOTEON) >> Call(midi2ext_pad)

# meant to pass only buttons related to controls
out_control = PortFilter(control_port) >> Filter(NOTEON) >> Call(midi2ext_TC)

run(
    scenes = {
        # scene 1: play piano.
        # this will switch the sampler to program 1, then route all events
        # to it
        1: Print() >> [
            # we might get info from transport control port, that should be commands
            PortFilter(control_port) >> Process(state.toggle_state, list_TC, checkTC = True) >> out_command,
            # regular input input, process CC events for general modifier, if any
            PortFilter(keyboard_port) >> Process(state.toggle_state, list_modifiers) >> [
                # created commands from modifier (with control port) get their output
                out_command,
                # what was not used for modifier still might be processed, process CC events for general states, if any
                 PortFilter(keyboard_port) >> Process(state.toggle_state, list_states) >>  [
                    # created commands (with control port) get their output
                    out_command,
                    # process regular keyboard events, that could become controls depending on state of button, first for modifiers -- for which only one is allowed at a time
                    PortFilter(keyboard_port) >>  Process(state.toggle_pattern, list_modifiers, only_first = True) >> [
                        # output pattern for modifier
                        out_command,
                        # process regular keyboard events, that could become controls depending on state of button, first for modifiers
                        PortFilter(keyboard_port) >>  Process(state.toggle_pattern, list_states) >> [
                            # again, new commands get their output
                            out_command,
                            out_keyboard_all
                            ]
                        ],
                    ],
                ],
            ],

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
