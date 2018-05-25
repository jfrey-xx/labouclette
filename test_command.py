 
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




class Modifier():
    """ juste trigger events associated to a button """
    def __init__(self, name, button, note_on = -1, note_off = -1, note_toggle = -1, velocity = 127, channel = 1, in_port = control_port):
        """
        name: you guess it, name of the modifier        
        button: which button on the keyboard (CC value)
        note_on, note_off, note_toggle: note associated to each one of these actions
        velocity: velocity to use for each action
        channel: channel to use for output
        in_port: which input produced midi message should appear to come from
        """
        self.name = name
        self.button = button
        self.note_on = note_on
        self.note_off = note_off
        self.note_toggle = note_toggle
        self.velocity = velocity
        self.channel = channel
        self.in_port = in_port
    
    def _action(self, note, action_name):
        """ actually create the note """
        print("Modifier " + self.name + " ation " + str(action_name))
        if note > 0:
            return NoteOnEvent(self.in_port, self.channel, note, self.velocity)
        else:
            print("Error: associated note not set")
        
    def on(self):
        """ send not associated to on """
        return self._action(self.note_on, "note_on")
    
    def off(self):
        """ send note associated to off """
        return self._action(self.note_off, "note_off")
    
    def toggle(self):
        """
        send note associated to toggle
        NB: not used at the moment
        """
        return self._action(self.note_toggle, "note_toggle")
        
    
# give feedback to possible OSC ui
remoteOSC = remoteOSC.RemoteOSC()                     
        
# HOTFIX: these notes produce sounds, go through computer keyboard instead
launch_state = state.State("launch", 3, note_toggle = 0, totoggle = True, keyboard_toggle = False, remoteOSC = remoteOSC)
midithrough_state = state.State("through", 15, note_on = 32, note_off = 33, alone = True, velocity = True, restore_on = True, reset_off = True, remoteOSC = remoteOSC)
#record_state = State("record", 14, note_on = 34, note_off = 35, alone = True, velocity = True, sync = [midithrough_state])
record_state = state.State("record", 14, note_on = 34, note_off = 35, alone = True, velocity = True, restore_on = True, reset_off = True, remoteOSC = remoteOSC)
# will set the recording to overwrite -- recording that should be set separatly
reset_state = state.State("reset", 16, note_toggle = 36, note_on = 37, note_off = 38, totoggle = True, restore_on = True, reset_off = True, velocity = True)

# all activated states will trigger...
list_states = [launch_state, record_state, midithrough_state, reset_state]


# here modifiers, not associated to pads
# will set the queue state -- recording that should be set separatly
queue_modifier = Modifier("queue", 9, note_toggle = 39, note_on = 40, note_off = 41)
# concatenate everything to check
list_modifiers = [queue_modifier]


def toggle_modifier(event):
    """
    generate events related to modifiers
    """
    # if one of the used controls
    if event.type is CTRL:
        print("a button is pressed")
        print(event.ctrl)
        
        # retrieve state
        modifier = None
        for m in list_modifiers:
            if m.button == event.ctrl:
                modifier = m
        if modifier == None:
            print("Could not find corresponding modifier")
            return event
        print("Modifier: " + modifier.name)
        
        # toggle state and return associated events
        if event.value != 0:
            print("set to True")
            return modifier.on()

        else:
           print("set to False")
           return modifier.off()
    
    # not captured here, continue to process event
    return event
    
        
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
        #1:  process CC events for general modifier, if any
        1: Print() >> Process(toggle_modifier) >> [
            # created commands from modifier (with control port) get their output
            out_command,
            # what was not used for modifier still might be processed, process CC events for general states, if any
             PortFilter(keyboard_port) >> Process(state.toggle_state, list_states) >>  [
                # created commands (with control port) get their output
                out_command,
                # process regular keyboard events, that could become controls depending on state of button
                PortFilter(keyboard_port) >>  Process(state.toggle_pattern, list_states) >> [
                    # again, new commands get their output
                    out_command,
                    out_keyboard_all
                    ]
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
