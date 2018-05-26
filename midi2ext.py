 
# Will trigger various events from mididings input


from subprocess import call


def midi2ext(param):
    print("got something!")
    print(param)
    
    
# association between note and key to send
TC_keys = {
    # stop
    93: 'Escape',
    # play
    94: 'space',
    }


pad_keys = {
    48: '1',
    49: '2',
    50: '3',
    51: '4',
}


def seq64_com(key):
    """ send key to seq64, relies on external xdootool """
    # name of the seq64 window, to be used with xdotool -- note the "ppqn", trick to get the window of interest
    seq64_wname = 'seq64 .* ppqn'
    call(["xdotool", "search", "--name", seq64_wname, "key",  "--clearmodifiers", key])



def midi2ext_TC(event):
    """ deal with transport control, input is meant to be NoteOn, should be filtered first """
    print("seq64 control!")
    print(event)
    print(event.note)
    key = TC_keys.get(event.note)
    if key != None:
        print("Will use key: [" + key + "]")
        seq64_com(key)
    else:
        print("not found in dic")

    
def midi2ext_pad(event):
    """ deal with pads, global control for seq64, input is meant to be NoteOn, should be filtered first """
    print("seq64 pads!")
    print(event)
    print(event.note)
    key = pad_keys.get(event.note)
    if key != None:
        print("Will use key: [" + key + "]")
        seq64_com(key)
    else:
        print("not found in dic")