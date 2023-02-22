# Handles fonts.
from tkinter import font

def fontlist():
    out = list(font.families())
    out.sort()
    return out

def font_roll(cur_font, delta):
    ls = fontlist()
    ix = 0
    for i in range(len(ls)):
        if cur_font.lower()==ls[i].lower():
            ix = i; break
    ix1 = (ix+delta)%len(ls)
    return ls[ix1]

def font_match(txt):
    # Tries to match the font.
    txt = txt.strip().lower()
    ls = fontlist()
    while len(txt)>0:
        for f in ls:
            if txt == f.lower():
                return f
        for f in ls:
            if f.lower().startswith(txt):
                return f
        for f in ls:
            if txt in f.lower():
                return f
        txt = txt[0:-1]