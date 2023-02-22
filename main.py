# Unicode fun.
import tkinter as tk
from tkinter import font
import tkinter.messagebox as messagebox
import traceback
import layout, codepoints, evt_check, fonts

debug_show_keypress = False

root = tk.Tk()
#Doesnt seem to work? #https://stackoverflow.com/questions/20324103/how-to-set-font-of-a-messagebox-with-python-tkinter
font1 = font.Font(name='TkCaptionFont', exists=True)
font1.config(family='Helvetica', size=16)

root.geometry("1024x384")
root.title("Unicode is like text but more. Much more. Ctrl+H for HELP.")
root.minsize(height=0, width=0)
root.maxsize(height=8192, width=8192)
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def debug_keypress(evt):
    mods = evt_check.get_mods(evt)
    if len(mods)>0:
        print('Keypress:', mods, '+', evt.keysym)#, hex(evt.state))
    else:
        print('Keypress:', evt.keysym)#, hex(evt.state))

class GUI(tk.Frame):
    def __init__(self, root=root):
        super(GUI, self).__init__(root)

        self.nshow = 1024
        self.last_location = 0

        self.textbox = tk.Text(root)#, yscrollcommand=scrollbar.set)
        #self.textbox.config(state='disabled')
        #self.text_input.bind('<<Modified>>', self.text_changed_callback, add='+')
        #root.bind("<Configure>", self.resize, add='+')
        self.textbox.pack() #fill=tk.BOTH

        self.numberbox = tk.Entry(root, bg = "#77FF77")
        self.numberbox.want_size = 0.08

        #self.numberbox = tk.Entry(root, bg = "#77FF77")

        self.numberbox.bind('<KeyRelease>', self.numberbox_keypress, add='+')
        self.fontbox = tk.Entry(root, bg = "#FFFF77")
        self.fontbox.want_size = [0.5, 0.0625]
        self.all_widgets = [self.textbox, self.numberbox, self.fontbox]
        _rows = [0,1,1]
        for i in range(len(self.all_widgets)):
            w = self.all_widgets[i]
            w.bind('<KeyPress>', self.maybe_tabthru, add='+')
            w.bind('<KeyPress>', self.maybe_open_help, add='+')
            w.bind('<KeyPress>', self.maybe_set_fontname, add='+')
            if i<2:
                w.bind('<MouseWheel>', self.on_wheel, add='+')
            w.which_row = _rows[i]
        self.fontbox.bind('<MouseWheel>', self.on_font_wheel, add='+')
        self.fontbox.bind('<KeyPress>', self.maybe_enter_font, add='+')

        layout.place_all(None, None, self.all_widgets)
        #layout.add_bigsmall_fns(self.all_widgets); layout.place_all(None, None, self.all_widgets)
        layout.add_fontsize_fns(self.all_widgets)
        #layout.focus_cycle(root, self.all_widgets)
        self.set_unicode_where(0)
        self._set_font_to('Times New Roman'); self.last_font = 'Times New Roman'

    def _getix(self):
        ix = self.get_unicode_where()
        if ix is None:
            ix = self.last_location
        return ix

    def _move_byto(self, delta, absolute_loc=None):
        if delta != 0 or absolute_loc is not None:
            ix = self._getix()
            if absolute_loc is not None:
                new_ix = absolute_loc
            else:
                new_ix = ix+delta
            new_ix = max(0, new_ix)
            self.set_unicode_where(new_ix)

    def maybe_enter_font(self, *args):
        #maybe_enter_font
        if args[0].keysym.lower()=='return':
            txt = self.fontbox.get().strip()
            match = fonts.font_match(txt)
            if match is not None:
                self._set_font_to(match)
            else:
                self._set_font_to('Times New Roman')

    def _set_font_to(self, fontname):
        # Sets the font.
        [layout.set_font_name(w, fontname) for w in self.all_widgets]
        self.fontbox.delete(0,tk.END)
        self.fontbox.insert(0,fontname)
        self.last_font = fontname

    def maybe_open_help(self, *args):
        if evt_check.emacs(args[0], 'C+h'):
            messagebox.showinfo("Help", layout.get_help_txt())

    def on_wheel(self, *args):
        evt = args[0]
        delta = evt.delta
        if delta>0:
            delta = -1
        elif delta<0:
            delta = 1
        mods = evt_check.get_mods(evt)
        if 'S' not in mods:
            delta = delta*16
        if 'C' in mods:
            delta = delta*4
        self._move_byto(delta)
        root.after(0, self.scroll2top)

    def on_font_wheel(self, *args):
        #txt = self.fontbox.get().strip()
        delta = args[0].delta
        if delta>0:
            delta = -1
        elif delta<0:
            delta = 1
        mods = evt_check.get_mods(args[0])
        if 'C' in mods:
            delta = delta*8
        if delta != 0:
            self._set_font_to(fonts.font_roll(self.last_font, delta))

    def maybe_tabthru(self, *args):
        delta = 0
        ix = self.get_unicode_where()
        hk = layout.hotkeys()
        if evt_check.emacs(args[0], hk['scroll256'][0]):
            delta = 256
        elif evt_check.emacs(args[0], hk['scroll-256'][0]):
            delta = -256
        if evt_check.emacs(args[0], hk['scroll1'][0]):
            delta = 1
        elif evt_check.emacs(args[0], hk['scroll-1'][0]):
            delta = -1
        if evt_check.emacs(args[0], hk['scroll16'][0]):
            delta = 16
        elif evt_check.emacs(args[0], hk['scroll-16'][0]):
            delta = -16

        if evt_check.emacs(args[0],hk['nextGroup'][0]):
            ix = codepoints.next_group(self._getix())
            self._move_byto(0, ix)
        elif evt_check.emacs(args[0],hk['prevGroup'][0]):
            ix = codepoints.prev_group(self._getix())
            self._move_byto(0, ix)
        elif evt_check.emacs(args[0],hk['nextSGroup'][0]):
            ix = codepoints.next_Sgroup(self._getix())
            self._move_byto(0, ix)
        elif evt_check.emacs(args[0],hk['prevSGroup'][0]):
            ix = codepoints.prev_Sgroup(self._getix())
            self._move_byto(0, ix)
        else:
            self._move_byto(delta)

    def maybe_set_fontname(self, *args):
        if evt_check.emacs(args[0],layout.hotkeys()['fontName']):
            fams = list(fonts.fontlist())
            #print('Font families:', fams)
            import random
            font_name = random.choice(fams)
            self._set_font_to(font_name)

    def get_unicode_where(self, hit_enter_mode=False):
        ntxt = self.numberbox.get().strip()
        #print('Numberbox txt:', txt)
        try:
            if hit_enter_mode:
                start_ix = codepoints.get_ix0(ntxt)
            else:
                start_ix = codepoints.get_ix(ntxt)
        except:
            print('Error with codepoints.get_ix, using last ix')
            return self.last_location
        self.last_location = start_ix
        return start_ix

    def set_unicode_where(self, start_ix):
        n = self.nshow

        self.textbox.delete(1.0, tk.END)
        txts, actives = codepoints.text_pieces(start_ix, start_ix+n)
        # TODO: colors of text properly.
        ########################################################################
        colors = ["#000000", "#FF0000", "#00AA00","#0000FF",'#CC4400','#229922','#2244AA','#999999']
        ck = len(colors)
        for i in range(ck):
            # https://stackoverflow.com/questions/47591967/changing-the-colour-of-text-automatically-inserted-into-tkinter-widget
            col = colors[i]
            # background=FOO means can't be selected.
            self.textbox.tag_config(str(i), foreground=col)

        for i in range(len(txts)):
            if actives[i]:
                col_ix = i%(ck-1)
            else:
                col_ix = ck-1
            self.textbox.insert(tk.END, txts[i], str(col_ix))
        self.scroll2top()
        ########################################################################

        set_txt_to = codepoints.canonical_wheretext(start_ix, self.numberbox.get().strip(),  self.nshow)
        cursor_position = self.numberbox.index(tk.INSERT)
        if set_txt_to.strip() != self.numberbox.get().strip():
            self.numberbox.delete(0,tk.END)
            self.numberbox.insert(0,set_txt_to)
            self.numberbox.icursor(cursor_position)

    def numberbox_keypress(self, *args):
        #print('Numberbox txt:', txt)
        start_ix = self.get_unicode_where(args[0].keysym.lower()=='return')
        if start_ix is not None:
            self.set_unicode_where(start_ix)

    def scroll2top(self, *args):
        self.textbox.yview(0)

    def resize(self, *args):
        try:
            [w,h] = [args[0].width, args[0].height]
        except:
            [w,h] = args[0]
        layout.place_all(w,h,self.all_widgets)
        root.after(0, self.scroll2top)

try:
    gui = GUI()
    gui.mainloop()
except Exception:
    traceback.print_exc()
