import pylatex

# TODO: Read pylatex doc on leadsheets pkg; integrate w/ pylatex
# https://ctan.math.washington.edu/tex-archive/macros/latex/contrib/leadsheets/leadsheets_en.pdf
# See also music21's handling of streams, measures, etc:
# https://www.music21.org/music21docs/usersGuide/usersGuide_04_stream1.html

from pylatex import Document, Package

doc = Document()
doc.packages.append(Package("leadsheets"))

ABBREVIATIONS = {
    "major" : "maj",
    "minor" : "min",
    "diminished" : "dim",
    "augmented" : "aug",
    "flat" : "b",
    "sharp" : "#",
    "double flat" : "bb",
    "double sharp" : "##"
}

class QUALITIES:
    MAJOR = "major"
    MINOR = "minor"
    DIMINISHED = "diminished"
    AUGMENTED = "augmented"

class ACCIDENTALS:
    NATURAL = "natural"
    FLAT = "flat"
    SHARP = "sharp"
    DOUBLE_FLAT = "double flat"
    DOUBLE_SHARP = "double sharp"

SHORTCUTS = {
    "b" : ACCIDENTALS.FLAT,
    "#" : ACCIDENTALS.SHARP,
    "bb" : ACCIDENTALS.DOUBLE_FLAT,
    "##" : ACCIDENTALS.DOUBLE_SHARP,
    "maj" : QUALITIES.MAJOR,
    "min" : QUALITIES.MINOR,
    "dim" : QUALITIES.DIMINISHED,
    "aug" : QUALITIES.AUGMENTED
}

class Chord:
    def __init__(
            self,
            root: int=1,
            accidental: str = ACCIDENTALS.NATURAL,
            quality: str = QUALITIES.MAJOR,
            bass: int=0,
            extensions: str=None
     ):
        self.root = root
        self.accidental = accidental
        self.quality = quality
        self.bass = bass if bass else root
        self.extensions = extensions if extensions else ""

    @classmethod
    def from_string(cls, string: str):
        """
        create a chord object from a string
        params:
            string: string representation of the chord
        returns:
            chord object

        format: <accidentals><root><optional/><bass if prev is '/'><quality><extensions>
        """

        i = 0 # "##2aug9"
        if string[i] in "b#":
            i += 1
            if string[i] in "b#": # double flat or sharp
                i += 1
                accidental = SHORTCUTS[string[:i]]
            else: # single flat or sharp
                accidental = SHORTCUTS[string[0]]
        else:
            accidental = ACCIDENTALS.NATURAL
        root = int(string[i])
        i += 1
        if string[i] == "/": # TODO: what about inverted borrow chords
            i += 1
            bass = int(string[i])
        else:
            bass = root
        # i += 1
        if string[i:i+3] in SHORTCUTS.keys():
            quality = SHORTCUTS[string[i:i+3]]
            i += 3
        else:
            quality = QUALITIES.MAJOR
        extensions = string[i:]

        return Chord(
            root=root,
            accidental=accidental,
            quality=quality,
            bass=bass,
            extensions=extensions
        )

    def is_inverted(self):
        return self.bass != self.root

    def __repr__(self):
        result = ""
        if self.accidental != ACCIDENTALS.NATURAL:
            abbrev = ABBREVIATIONS[self.accidental]
            result += abbrev
        result += str(self.root)
        if self.is_inverted():
            result += f"/{self.bass}"
        qual = "" if (self.quality == QUALITIES.MAJOR and not self.extensions) else self.quality
        qual = ABBREVIATIONS[qual] if qual in ABBREVIATIONS else qual
        result += f" {qual}"
        if self.extensions:
            for ext in self.extensions:
                result += f"{ext}"
        return result

def main():
    chord = Chord(7, "flat", quality=QUALITIES.DIMINISHED)
    print(chord)

    chord_str = "b3maj7"
    chord = Chord.from_string(chord_str)
    print(chord)

    chord_str = "##2aug9"
    print(Chord.from_string(chord_str))

if __name__ == "__main__":
    main()


