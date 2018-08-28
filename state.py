 
from pattern import Patterns
from mididings import NOTEON, NOTEOFF, CTRL
from mididings.event import NoteOnEvent, NoteOffEvent
from midi2ext import seq64_com
  

# Output port_name, channel, program
class State(object):
    # hom many patterns to deal with
    nb_patterns = Patterns.nb
    
    """ helper to configure the various actions """  
    def __init__(self, name, button, note_on = -1,note_off = -1, note_toggle = -1, totoggle = False, keyboard_toggle = False,                 
                 velocity = False, alone = False, sync = [], channel = 1, in_port = "controls",
                 reset_off = False, reset_on = False, restore_on = False,
                 remoteOSC = None, force_on = False, force_off = False
                ):
        """
        name: we want some debug
        button: which button on the keyboard (CC value)
        note_on: if >= 0, note for seq64 switch on (and off, and +0 to 32 if velocity == False)
        note_off:  if >= 0, note for seq64 switch off (implies velocity == True)
        note_toggle: if >= 0, note for seq64 switch toggle with note on event(+0 to 32 if velocity == False)
        totoggle: if True should be toggled instead of swiched on
        keyboard_toggle: if True, use computers keys to send command (implies totoggle, to be used with launch) -- TODO: more generic
        velocity: if True, use velocity value to set pattern. If False, will use note_* as a base and then add pattern number to it
        alone: if only one should be there at a time
        sync: list of states to synchronize with that
        channel: channel to use for output
        reset_on: should disable all pattern when state activated
        reset_off: should disable all pattern when state desactivated
        restore_on: restore previous pattern on "on" (take over reset_on)
        in_port: which input produced midi message should appear to come from
        remoteOSC: point to a RemoteOSC instance to send message when patterns changes (1 or 0), will use state name as address prefix to target pattern, e.g. launch_1, launch_2, etc.
        force_on: will set on event even if state already on
        force_off: will set on event even if state already off
        TODO: could use fixed velocity to differenciate instead of shift in notes
        """
        self.name = name
        self.button = button
        self.note_on = note_on
        self.note_off = note_off
        self.note_toggle = note_toggle
        self.totoggle = totoggle
        self.keyboard_toggle = keyboard_toggle
        self.velocity = velocity
        self.alone = alone
        self.sync = sync
        self.channel = channel
        self.in_port = in_port
        self.reset_on = reset_on
        self.reset_off = reset_off
        self.restore_on = restore_on
        self.remoteOSC = remoteOSC
        self.force_on = force_on
        self.force_off = force_off
        
        self.enable = False

        # debug check for inheritance
        print("Init state: " + self.name + " with button " + str(self.button))
        
        if self.keyboard_toggle and not self.totoggle:
            print(self.name + ": Warning, keyboard_toggle set without totoggle, won't be used")
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
        print(self.patterns)
        events = []
        for p in range(0,State.nb_patterns):
            if p not in unless:
                e = self.off(p)
                if e != None:
                    print("off" + str(p))
                    events.append(e)
            else:
                print("keeps: " + str(p))
        return events
        
    
    def restore_state(self):
        """
        creating events to restore state of previous patterns
        TODO: check if works with totoggle
        """
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
      
    def _set_pattern(self, pattern, flag):
        """ toggle states of associated patterns, send OSC messages if needed """
        self.patterns[pattern] = flag
        if self.remoteOSC != None:
            self.remoteOSC.command(self.name, pattern, flag)
        
    def off(self, pattern):
        """ turn off the correspoding pattern;; unless force_off, do nothing if not active """
        if not self.patterns[pattern] and not self.force_off:
            #print(self.name + " off: pattern " + str(pattern) + " already off!")
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
        
        self._set_pattern(pattern, False)
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
        
        event = None
        
        if self.keyboard_toggle:
            seq64_com(Patterns.keyboard[pattern]) 
        else:
            if self.velocity:
                event = NoteOnEvent(self.in_port, self.channel, self.note_toggle, 0 + pattern)
            else:
                event = NoteOnEvent(self.in_port, self.channel, self.note_toggle + pattern, 127)
                
        self._set_pattern(pattern, not self.patterns[pattern])
        return event

        
    def on(self, pattern):
        """ turn on corresponding pattern, unless force_on, do nothing if already activated """
        if self.patterns[pattern] and not self.force_on:
            #print(self.name + " on: pattern " + str(pattern) + " already on!")
            return
        if self.note_on < 0:
            print("Error: state " + self.name + " has no on note")
            return
        if self.velocity:
            event = NoteOnEvent(self.in_port, self.channel, self.note_on, 0 + pattern)
        else:
            event = NoteOnEvent(self.in_port, self.channel, self.note_on + pattern, 127)
        self._set_pattern(pattern, True)
        return event
        
    def setEnable(self, flag):
        """ set this state alive or not, return events to execute, if any"""
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
        
    def isActive(self):
        """ is it enabled and does it process patterns (i.e. note_on or note_toggle or note_off is set) """
        return self.enable and (self.note_on >= 0 or self.note_off >= 0 or self.note_toggle >= 0)
        

    def process(self, pattern):
        """ pattern to be lauchnced, return list of required actions """
        events = []
        # check if associated state
        for syn in self.sync:
            print("associated sync state: " + syn.name)
            events += syn.process(pattern)

        # reset this actual state if needed
        if self.alone:
            events += self.reset_state(unless=[pattern])
        # maybe pattern already on and no new event...
        e = self.activate(pattern)
        if e != None:
            events.append(e)
        
        return events

class Modifier(State):
    """ special instance of state, that send itself a midi note on activation / deactivation. Also possible to send an OSC message"""
    
    def __init__(self, *args, **kwargs):
        """
        init method with new keywords
        note_activate, note_deactivate: note associated to each one of these actions (default -1)
        velocity: velocity to use for each action (default 127)
        osc_activate, osc_deactivate: address to send a signal to for each state (NB: remoteOSC should be set)
        osc_arg: what to send along osc message (default: 1)
        osc_arg_val: if True, will send the associated CC value / velocity
        """
        # setting new keywods
        self.note_activate = kwargs.pop('note_activate', -1)
        self.note_deactivate = kwargs.pop('note_deactivate', -1)      
        self.velocity = kwargs.pop('velocity', 127)
        self.osc_activate = kwargs.pop('osc_activate', None)
        self.osc_deactivate = kwargs.pop('osc_deactivate', None)
        self.osc_arg = kwargs.pop('osc_arg', 1)

        
        # passing the rest to upper class
        super(Modifier, self).__init__(*args, **kwargs)        
        print("init modifier with activate " + str(self.note_activate) + " and deactivate " + str(self.note_deactivate))
        
    def _action(self, note, action_name, osc_address, osc_arg):
        """ actually create the note and send OSC message"""
        print("Modifier " + self.name + " action " + str(action_name))
        if note > 0:
            return NoteOnEvent(self.in_port, self.channel, note, self.velocity)
        else:
            print("Error: associated note not set")
        
        if self.remoteOSC != None and osc_address != None:
            self.remoteOSC.command_raw(osc_address, osc_arg)
        
    def setEnable(self, flag):
        """ overload State.setEnable to also send associated note """
        # first inform upper class and gather results
        events = super(Modifier, self).setEnable(flag)
        
        # if there was no events, create list
        if events == None:
            events = []
            
        # second, check associated note
        if flag:
            event = self._action(self.note_activate, "note_on", self.osc_activate, self.osc_arg)
        else:
            event = self._action(self.note_deactivate, "note_off", self.osc_deactivate, self.osc_arg)
        
        if event != None:
            events.append(event)
        
        return events


def toggle_state(event, list_states, checkTC = False):
    """
    flip the state of buttons.
    list_states: list of states to check the event against
    checkTC: if True, then will look for NOTEON event instead of CC, as is it what transport controls will look like -- will discard any even if not processed!
    """
    # if one of the used controls
    if event.type is CTRL or checkTC and event.type is NOTEON:
        if checkTC:
            print("a TC is pressed")
            print(event.note)
        else:
            print("a button is pressed")
            print(event.ctrl)
        
        # retrieve state
        state = None
        for s in list_states:
            if (checkTC and s.button == event.note) or (not checkTC and s.button == event.ctrl):
                state = s
        if state == None:
            print("Could not find corresponding state")
            # in case of TC we really don't want to process it
            if checkTC:
                return
            else:
                return event
        print("State: " + state.name)
        
        # toggle state and return associated events
        if (checkTC and event.velocity != 0) or (not checkTC and event.value != 0):
            print("set to True")
            return state.setEnable(True)

        else:
           print("set to False")
           return state.setEnable(False)
    # note TC could also get noteoff, we want to discard that
    elif checkTC and event.type is NOTEOFF:
        return
    
    # not captured here, continue to process event
    return event
        
def toggle_pattern(event, list_states, only_first = False, channel = 2):
    """
    might trigger commands if a special state is on-going
    list_states: list of states to check the event (and pattern) against
    only_first: will deal with first state on the list which accepts pattern, and that's it
    channel: which channel patterns should come from
    """
    # only deal with channel 2 (which should be pads)
    if event.channel != channel:
        print("not channel" + str(channel) + ", pass through")
        return event

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
        if list_states[i].isActive():
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
            events+=state.process(pattern)
        return events
    else:
        # we got a negative pattern number, error code
        print("error, bad pattern")
        return event