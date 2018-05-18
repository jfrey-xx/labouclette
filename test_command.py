 
from mididings import *
from mididings.event import *
from mididings.extra.inotify import AutoRestart
#from mididings.extra import MemorizeScene

from midi2ext import *

# trying to cnontrol seq64 with code25
# some inspiration from https://gist.oonnnoo.com/milkmiruku/2afb362b060b40f7575b8854220ad82e

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

class Patterns():
    # list of notes as in pattern order
    # NB: here we wil use pads from code25, mapped physically, should be octave 0
    notes = [48, 44, 40, 36, 49, 45, 41, 37, 50, 46, 42, 38, 51, 47, 43, 39] 
    nb = len(notes)
    
    @staticmethod
    def note2pattern(note):
        """ retrieve pattern number from note, -1 if nothing """
        if note not in Patterns.notes:
            print("Error: note " + str(note) + " is not among known patterns")
            return -1
        for i in range(0, len(Patterns.notes)):
            if Patterns.notes[i] == note:
                return i
        

# Output port_name, channel, program
class State():
    # hom many patterns to deal with
    nb_patterns = Patterns.nb
    
    """ helper to configure the various actions """  
    def __init__(self, name, button, note_on = -1,note_off = -1, note_toggle = -1, totoggle = False, velocity = False, alone = False, sync = [], channel = 1, in_port = control_port):
        """
        name: we want some debug
        button: which button on the keyboard (CC value)
        note_on: if >= 0, note for seq64 switch on (and off, and +0 to 32 if velocity == False)
        note_off:  if >= 0, note for seq64 switch off (implies velocity == True)
        note_toggle: if >= 0, note for seq64 switch toggle with note on event(+0 to 32 if velocity == False)
        totoggle: if True should be toggled instead of swiched on
        velocity: if True, use velocity value to set pattern. If False, will use note_* as a base and then add pattern number to it
        alone: if only one should be there at a time
        sync: list of states to synchronize with that
        channel: channel to use for output
        in_port: which input produced midi message should appear to come from
        
        TODO: could use fixed velocity to differenciate instead of shift in notes
        """
        self.name = name
        self.button = button
        self.note_on = note_on
        self.note_off = note_off
        self.note_toggle = note_toggle
        self.totoggle = totoggle
        self.velocity = velocity
        self.alone = alone
        self.sync = sync
        self.channel = channel
        self.in_port = in_port
        self.enable = False
    
    # list of notes for each action
    def reset_state(self, unless=[]):
        """
        switch to off all patterns
        unless: list of pattern *not* to reset (e.g. will be turned on right after)
        """
        events = []
        for p in range(0,State.nb_patterns):
            if p not in unless:
                events.append(self.off(p))
            else:
                print("keeps: " + str(p))                
        return events

    def off(self, pattern):
        """ turn off the correspoding pattern """
        # don't bother is no available way to turn off
        if self.velocity and self.note_off < 0:
            print("Error: state " + self.name + " use velocity but has no off note for off")
            return
        if not self.velocity and self.note_on < 0:
            print("Error: state " + self.name + " has no note for off")
            return
        
        print("reset: " + str(pattern))
        if self.velocity:
            event = NoteOnEvent(self.in_port, self.channel, self.note_off, 0 + pattern)
        else:
            event = NoteOffEvent(self.in_port, self.channel, self.note_on + pattern)
        return event
    
    def activate(self, pattern):
        """ will pick on or toggle  to activate corresponding pattern """
        if self.totoggle:
            return self.toggle(pattern)
        else:
            return self.on(pattern)
    
    def toggle(self, pattern):
        if self.note_toggle < 0:
            print("Error: state " + self.name + " has no toggle note")
            return
        if self.velocity:
            event = NoteOnEvent(self.in_port, self.channel, self.note_toggle, 0 + pattern)
        else:
            event = NoteOnEvent(self.in_port, self.channel, self.note_toggle + pattern, 127)
        return event
        
    def on(self, pattern):
        if self.note_on < 0:
            print("Error: state " + self.name + " has no on note")
            return
        if self.velocity:
            event = NoteOnEvent(self.in_port, self.channel, self.note_on, 0 + pattern)
        else:
            event = NoteOnEvent(self.in_port, self.channel, self.note_on + pattern, 127)
        return event
        
    def setEnable(self, flag):
        """ set this state alive or not """
        self.enable = flag
        
    def isEnable(self):
        """ is it alive ? """
        return self.enable
                        
        
launch_state = State("launch", 3, note_toggle = 0, totoggle = True)
midithrough_state = State("midi_through", 9, note_on = 32, note_off = 33, alone = True, velocity = True)
record_state = State("record", 14, note_on = 34, note_off = 35, alone = True, velocity = True, sync = [midithrough_state])

# priority will be in this order for actions
list_states = [launch_state, midithrough_state, record_state]

def toggle_state(event):
    """ flip the state of buttons. """
    # if one of the used controls
    if event.type is CTRL:
        print("a button is pressed")
        print(event.ctrl)
        
        # retrieve state
        state = None
        for s in list_states:
            if s.button == event.ctrl:
                state = s
        if state == None:
            print("Could not find corresponding state")
            return event
        print("State: " + state.name)
        
        if event.value != 0:
            print("set to True")
            state.setEnable(True)
        else:
           print("set to False")
           state.setEnable(False)
        
        # reset if needed
        if state.alone:
            return state.reset_state()
            
        # otherwise noting to return as midi event
        return
    
    # not captured here, continue to process event
    return event
       
def toggle_pattern(event):
    """ might trigger commands if a special state is on-going """
    for i in range(0, len(list_states)):
        # select the first state
        if list_states[i].isEnable():
            state = list_states[i]
            print("Current state: " + state.name)
            # check if event of interest
            if event.type == NOTEON and event.note in Patterns.notes:
                print("Note On " + str(event.note) + " is of interest.")
                pattern = Patterns.note2pattern(event.note)
                print("Corresponding pattern: " + str(pattern))
                events = []                    
                if pattern >= 0:
                    # check if associated state
                    for syn in state.sync:
                        # ... and if should be reset for the other patterns
                        if syn.alone:
                            events += syn.reset_state(unless=[pattern])
                        events.append(syn.activate(pattern))
                    # reset this actual state if needed
                    if state.alone:
                        events += state.reset_state(unless=[pattern])
                    events.append(state.activate(pattern))
                    return events
            # silently discard NOTEOFF    
            elif event.type == NOTEOFF and event.note in Patterns.notes:
                print("Note Off " + str(event.note) + " was of interest.")
                return
    # we got nothing, pass the event along
    return event
        
# pass all event related to keyboard port
out_keyboard_all = PortFilter(keyboard_port ) >> Print() >> Output('synth')
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
        #1:  process CC events for general state if any
        1: Print() >> Process(toggle_state) >>  [
            # created commands (with control port) get their output
            out_command,
            # process regular keyboard events, that could become controls depending on state of button
            PortFilter(keyboard_port) >>  Process(toggle_pattern) >> [
                # again, new commands get their output
                out_command,
                out_keyboard_all
                ]
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
