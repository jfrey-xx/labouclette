 

class Patterns():
    # list of notes as in pattern order
    # NB: here we wil use pads from code25, mapped physically, should be octave 0
    notes = [48, 44, 40, 36, 49, 45, 41, 37, 50, 46, 42, 38, 51, 47, 43, 39] 
    # corresponding keyboard keys for alternative way to launch that
    keyboard = ['1','q','a','z','2','w','s','x','3','e','d','c','4','r','f','v','5','t','g','b','6','y','h','n','7','u','j','m','8','i','k',',']
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
                