 
from mididings import *
from mididings.event import *
from mididings.extra.inotify import AutoRestart
#from mididings.extra import MemorizeScene

from midi2ext import *

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
    def __init__(self, name, button, note_on = -1,note_off = -1, note_toggle = -1, totoggle = False, velocity = False, alone = False, sync = [], channel = 1, in_port = control_port, reset_off = False, reset_on = False, restore_on = False):
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
        reset_on: should disable all pattern when state activated
        reset_off: should disable all pattern when state desactivated
        restore_on: restore previous pattern on "on" (take over reset_on)
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
        self.reset_on = reset_on
        self.reset_off = reset_off
        self.restore_on = restore_on
        self.enable = False
        
        # pattern status for this state
        # FIXME: might not be reliable with the use of toggle
        self.patterns = [False] * Patterns.nb
        # for restore
        self.past_patterns = list(self.patterns)
    
    def reset_state(self, unless=[]):
        """
        switch to off all patterns
        unless: list of pattern *not* to reset (e.g. will be turned on right after)
        """
        events = []
        for p in range(0,State.nb_patterns):
            if p not in unless:
                e = self.off(p)
                if e != None:
                    events.append(e)
            else:
                print("keeps: " + str(p))
        return events
        
    
    def restore_state(self):
        """ creating events to restore state of previous patterns """
        events = []
        for p in range(0, State.nb_patterns):
            # enable what is not yet enabled
            if self.past_patterns[p] and not self.patterns[p]:
                e = self.on(p)
                if e != None:
                    events.append(e)
            elif not self.past_patterns[p] and self.patterns[p]:
                e = self.off(p)
                if e != None:
                    events.append(e)
        return events
        
    def off(self, pattern):
        """ turn off the correspoding pattern, do nothing if not active """
        if not self.patterns[pattern]:
            #print(self.name + " off: pattern " + str(pattern) + " arleady off!")
            return
            
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
        
        self.patterns[pattern] = False
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
        self.patterns[pattern] = not self.patterns[pattern]
        return event
        
    def on(self, pattern):
        """ turn on corresponding pattern, do nothing if already activated """
        if self.patterns[pattern]:
            print(self.name + " on: pattern " + str(pattern) + " arleady on!")
            return
        if self.note_on < 0:
            print("Error: state " + self.name + " has no on note")
            return
        if self.velocity:
            event = NoteOnEvent(self.in_port, self.channel, self.note_on, 0 + pattern)
        else:
            event = NoteOnEvent(self.in_port, self.channel, self.note_on + pattern, 127)
        self.patterns[pattern] = True
        return event
        
    def setEnable(self, flag):
        """ set this state alive or not, return events to execute"""
        self.enable = flag
        # safe current patterns if case of restore
        if not flag and self.restore_on:
            self.past_patterns = list(self.patterns)
            
        # restore if needed
        if flag and self.restore_on:
            return self.restore_state()
        # reset if needed
        elif flag and self.reset_on:
            return self.reset_state()
        elif not flag and self.reset_off:
            return self.reset_state()
        
    def isEnable(self):
        """ is it alive ? """
        return self.enable
                        
        
launch_state = State("launch", 3, note_toggle = 0, totoggle = True)
midithrough_state = State("midi_through", 15, note_on = 32, note_off = 33, alone = True, velocity = True, restore_on = True, reset_off = True)
#record_state = State("record", 14, note_on = 34, note_off = 35, alone = True, velocity = True, sync = [midithrough_state])
record_state = State("record", 14, note_on = 34, note_off = 35, alone = True, velocity = True, restore_on = True, reset_off = True)


# all activated states will trigger...
list_states = [launch_state, record_state, midithrough_state]

def toggle_state(event):
    """
    flip the state of buttons.
    """
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
        
        # toggle state and return associated events
        if event.value != 0:
            print("set to True")
            return state.setEnable(True)

        else:
           print("set to False")
           return state.setEnable(False)
    
    # not captured here, continue to process event
    return event
       
def toggle_pattern(event, only_first = True):
    """
    might trigger commands if a special state is on-going
    only_first: will deal with first pattern on the list, and that's it
    """

    # we don't manage anything but notes
    if (event.type != NOTEON and event.type != NOTEOFF ):
        print("not a note, pass through")
        return event

    # if event not of interest, pass it along
    if (event.type == NOTEON or event.type == NOTEOFF ) and event.note not in Patterns.notes:
        print("note not of interest, pass along")
        return event
    
    # list of states to handle
    states = []
    for i in range(0, len(list_states)):
        if list_states[i].isEnable():
            states.append(list_states[i])
            if only_first:
                print("Only consider first active pattern")
                break
    
    # if empty list, just pass the note along
    if len(states) == 0:
        print("no activated state, pass along")
        return event
        
    # we don't care about note off event from notes of interest, discard them (actions only on press)
    if event.type == NOTEOFF and event.note in Patterns.notes:
        print("discard Note Off " + str(event.note))
        return
    
    # should have only case with NOTEON of interest here...
    if event.type != NOTEON or event.note not in Patterns.notes:
        print("error, should be note on in notes of interest!!")
        return event
        
    # got some state, a note on of interest, build a set of events to return
    events = []
    
    print("Note On " + str(event.note) + " is of interest.")
    pattern = Patterns.note2pattern(event.note)
    print("Corresponding pattern: " + str(pattern))
    if pattern >= 0:
        for state in states:
            print("Process state: " + list_states[i].name)
            # check if associated state
            for syn in state.sync:
                print("associated sync state: " + syn.name)
                # ... and if should be reset for the other patterns
                if syn.alone:
                    events += syn.reset_state(unless=[pattern])
                # maybe pattern already on and no new event...
                syne = syn.activate(pattern)
                if syne != None:
                    events.append(syne)
            # reset this actual state if needed
            if state.alone:
                events += state.reset_state(unless=[pattern])
            # here again maybe pattern already on and no new event...
            e = state.activate(pattern)
            if e != None:
                events.append(e)
        return events
    else:
        # we got a negative pattern number, error code
        print("error, bad pattern")
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
