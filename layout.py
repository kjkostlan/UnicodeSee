# Widget layout.
# Based on simple priority stuff.
import evt_check

def hotkeys():
    # All the hotkeys. Change these by editing this function.
    out = {}
    out['scroll1'] = ['C+.', 'Forward one char']
    out['scroll-1'] = ['C+,', 'Backward one char']
    out['scroll16'] = ['M+.', 'Forward 16 char']
    out['scroll-16'] = ['M+,', 'Backward 16 char']
    out['scroll256'] = ['CS+.', 'Forward 256 char']
    out['scroll-256'] = ['CS+,', 'Forward 256 char']
    out['nextGroup'] = ['C+]', 'Next block']
    out['prevGroup'] = ['C+[', 'Prev block']
    out['nextSGroup'] = ['CS+]', 'Next sister block']
    out['prevSGroup'] = ['CS+[', 'Prev sister block']

    out['fontbig'] = ['C+=', 'Bigger font']
    out['fontBIG'] = ['CS+=', 'BIGGER font']
    out['fontsmall'] = ['C+-', 'Smaller font']
    out['fontSMALL'] = ['CS+-', 'SMALLER font']
    out['fontName'] = ['C+f', 'Random font']

    #out['']
    return out

def row_groups(widgets):
    groups = []
    ix = 0
    for w in widgets:
        if 'which_row' not in w.__dict__:
            w.which_row = ix; ix = ix+1
        while w.which_row>=len(groups):
            groups.append([])
        groups[w.which_row].append(w)
    for g in groups:
        if len(g)==0:
            raise Exception('Empty rows in which zero widgets have to stretch a while.')
    return groups

def normalize_widget_sizes(widgets, dim):
    # Creates the want_size attribute, and sum to one.
    total = 0.0
    for w in widgets:
        if 'want_size' not in w.__dict__:
            w.want_size = [1.0, 1.0]
        elif type(w.want_size) is not list and type(w.want_size) is not tuple:
            w.want_size = [1.0, w.want_size]
        total = total+w.want_size[dim]
    for w in widgets:
        w.want_size[dim] = w.want_size[dim]/total

def place_all(window_x, window_y, widgets):
    widgetss = row_groups(widgets)
    widgets_leftcolum = [widgets[0] for widgets in widgetss]
    normalize_widget_sizes(widgets_leftcolum, 1)
    relys = []; relhs = []
    used_up = 0.0
    for w in widgets_leftcolum:
        relys.append(used_up); relhs.append(w.want_size[1])
        used_up = used_up+w.want_size[1]

    for i in range(len(widgetss)): # Each row.
        widgets = widgetss[i]
        normalize_widget_sizes(widgets, 0)
        used_up = 0.0
        for j in range(len(widgets)):
            #https://www.tutorialspoint.com/python/tk_place.htm
            _ry = relys[i]; _rw = widgets[j].want_size[0]
            #print('Widget fun:', [used_up, _ry, _rw, relhs[i]], [i,j])
            widgets[j].place(relx=used_up, rely=_ry, relwidth=_rw, relheight=relhs[i])
            used_up = used_up+widgets[j].want_size[0]

def add_bigsmall_fns(widgets):
    # Alt + and Alt -
    def maybe_change_sz(widget_ix, evt):
        char = evt.char
        fac = 1.0
        if evt_check.emacs(evt, ['M+-', 'M+=', 'SM+-', 'SM+=']):
            if char=='-' or char == '_':
                fac = 7.0/8.0
            elif char=='=' or char == '+':
                fac = 8.0/7.0
            if evt_check.emacs(evt, ['SM+-', 'SM+=']):
                fac = fac**0.25
        if fac != 1.0:
            normalize_widget_sizes(widgets)
            widgets[widget_ix].want_size = widgets[widget_ix].want_size*fac
            place_all(None, None, widgets)

    for i in range(len(widgets)):
        widgets[i].bind('<KeyPress>', lambda evt, j=i: maybe_change_sz(j, evt=evt), add='+')

def set_font_name(widget, fontname):
    widget.lovely_font[0] = fontname
    widget.config(font=widget.lovely_font)

def add_fontsize_fns(widgets):
    for w in widgets:
        w.lovely_font = ['Courier', 18]
        w.config(font=w.lovely_font)
    hk = hotkeys()
    def maybe_change_font(w, evt):
        char = evt.char
        keysym = evt.keysym
        delta = 0
        if evt_check.emacs(evt,hk['fontbig'][0]):
            delta = 1
        elif evt_check.emacs(evt,hk['fontsmall'][0]):
            delta = -1
        elif evt_check.emacs(evt,hk['fontBIG'][0]):
            delta = 4
        elif evt_check.emacs(evt,hk['fontSMALL'][0]):
            delta = -4

        if delta != 0:
            w.lovely_font[1] = max(1,int(w.lovely_font[1]+delta+0.5))
            w.config(font=w.lovely_font)
    for w in widgets:
        w.bind('<KeyPress>', lambda evt, wd=w: maybe_change_font(wd, evt=evt), add='+')

def focus_cycle(root, widgets):

    def which_has_focus(widgets):
        w0 = root.focus_get()
        for i in range(len(widgets)):
            if widgets[i] is w0:
                return i
        return -1

    def maybe_cycle_focus(evt):
        char = evt.char
        keysym = evt.keysym
        if keysym=='grave' or keysym=='asciitilde':
            focus = which_has_focus(widgets)
            #print('Current focus:', focus, 'mod_state:', mod_state)
            if focus==-1:
                focus = 0
            if evt_check.emacs(evt, 'C+~'):
                focus = (focus+1)%len(widgets)
            elif evt_check.emacs(evt, 'CS+~'):
                focus = (focus-1)%len(widgets)
            if evt_check.emacs(evt, ['C+~', 'CS+~']):
                #print('Set focus:', focus)
                widgets[focus].focus_set()

    for w in widgets:
        w.bind('<KeyPress>', maybe_cycle_focus, add='+')

def get_help_txt():
    help_txt = ['How to input a location in the lower box:']
    help_txt.append('  Mode 1: Direct hex, i.e. "0x1234"')
    help_txt.append('  Mode 2: Block lookup, i.e. "Greek" or "Greek A"')
    help_txt.append('  Mode 3: insert a unicode char, i.e. "α"')

    rpairs = [['C+','Ctrl-'],['CS+','Ctrl-Shift-'],['M+','Alt-']]

    help_txt.append('Hotkeys:')
    help_txt.append('  '+'Hold Shift and/or Ctrl to change mousewheel speed.')
    hk = hotkeys()
    for k in hk.keys():
        txt = '  '+hk[k][0]+' '+hk[k][1]
        for rp in rpairs:
            txt = txt.replace(rp[0],rp[1])
        help_txt.append(txt)

    help_txt.append('Why is it jumping around?')
    help_txt.append('  Many characters affect placement.')
    help_txt.append('  Accents are decorators and Arabic is reversed.')
    help_txt.append('  Splaying them out in order, as we do, is a bit silly.')
    help_txt.append('Did it freeze?')
    help_txt.append('  Loading unicode hase a one-time cost.')
    help_txt.append('  Is there faster under-the-hood code to use?')
    help_txt.append('Greek isnt Greek to Python!')
    help_txt.append('  Python can use many unicode chars.')
    help_txt.append('  Look for the happy snake!')

    return '\n'.join(help_txt)
