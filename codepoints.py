# Unicode fun.
# https://jrgraphix.net/r/Unicode/
# https://unicode.org/emoji/charts/emoji-list.html
# https://stackoverflow.com/questions/1366068/whats-the-complete-range-for-chinese-characters-in-unicode
import re

def ranges():
    out = {}
    raw = '''

0000-001F   The Dungeon

2100-214F   Symbols A
2600-26FF   Symbols B
2B00-2BFF   Symbols C
1F700-1F77F   Symbols D
1FB00-1FBFF   Symbols E
25A0-25FF   Shapes A
1F780-1F7FF   Shapes B
2580-259F   Blocks
2700-27BF   Dingbats
2500-257F   Boxes
2900-297F   Arrows C
27F0-27FF   Arrows B
2190-21FF   Arrows A
2B00-2BFF   Arrows D
1F800-1F8FF   Arrows E
2800-28FF   Braille
2440-245F   Robot
1F300-1F5FF   Emojis A
1F600-1F64F   Emojis B
1F680-1F6FF   Emojis C
1F900-1F9FF   Emojis D
1FA70-1FAFF   Emojis E

0300-036F   Accents A
1AB0-1AC0   Accents B
1DC0-1DFF   Accents C
20D0-20FF   Accents D
2DE0-2DFF   Accents E
FE20-FE2F   Accents F

20A0-20CF   Currency
1D100-1D1FF   Music
2150-218F   Fractions
A830-A83F   Indic Numbers
111E0-111FF   Sinhala Archaic Numbers
2200-22FF   Math A
27C0-29FF   Math B
2980-29FF   Math C
2A00-2AFF   Math E
1D400-1D7FF   Math F

02B0-02FF   Spacing Modifiers
D800-DB7F   High Surrogates
DB80-DBFF   High Private Use Surrogates
DC00-DFFF   Low Surrogates
E000-F8FF   Free For All
FFF0-FFFF   Specials
2300-23FF   Miscellaneous Technical
1D000-1D0FF   Byzantine Music
2400-243F   Control Pictures
E0000-E007F   Tags

FB00-FB4F   Alphabetic Presentation Forms
FE00-FE0F   Variation Selectors
FE50-FE6F   Small Form Variants
FF00-FFEF   Halfwidth and Fullwidth Forms
A700-A71F    Modifier Tone Letters
10000-1007F   Linear B Syllabary
10080-100FF   Linear B Ideograms
2070-209F   Superscripts and Subscripts
2000-206F   Punctuation A
2E00-2E52   Punctuation B
0250-02AF   IPA A
1D00-1D7F   IPA B
2460-24FF   Enclosed Alphanumerics

1100-11FF   Hangul A
A960-A97F   Hangul B
AC00-D7FB   Hangul C

1780-17FF   Khmer A
19E0-19FF   Khmer B

1400-167F   Canadian Aboriginal A
18B0-18FF   Canadian Aboriginal B

2E80-2EFF   CJK Radicals Supplement
2F00-2FDF   Kangxi Radicals
2FF0-2FFF   Ideographic Description Characters
3000-303F   CJK Symbols and Punctuation
3040-309F   Hiragana
30A0-30FF   Katakana
3100-312F   Bopomofo A
3130-318F   Hangul Compatibility Jamo
3190-319F   Kanbun
31A0-31BF   Bopomofo B
31C0-31EE   Small gap in CKJ
31F0-31FF   Katakana Phonetic Extensions
3200-32FF   Enclosed CJK Letters and Months
3300-33FF   CJK Compatibility
3400-4DBF   CJK Unified Ideographs Extension A
4DC0-4DFF   Yijing Hexagram Symbols
4E00-9FFF   CJK Unified Ideographs
A000-A48F   Yi Syllables
A490-A4CF   Yi Radicals

F900-FAFF   CJK Compatibility Ideographs
FE30-FE4F   CJK Compatibility Forms
1D300-1D35F  Tai Xuan Jing Symbols
20000-2A6DF  CJK Unified Ideographs Extension B
2F800-2FA1F  CJK Compatibility Ideographs Supplement

0600-06FF   Arabic A
0750-077F   Arabic B
08A0-08FF   Arabic C
FB50-FDFF   Arabic D
FE70-FEFF   Arabic E

0020-024F   Latin A
1E00-1EFF   Latin B
2C60-2C7F   Latin C
A720-A7FF   Latin D
AB30-AB6F   Latin E
0370-03FF   Greek A
1F00-1FFF   Greek B

0400-04FF   Cyrillic A
0500-052F   Cyrillic B
1C80-1C8F   Cyrillic C
1D80-1DBF   Cyrillic D
A640-A69F   Cyrillic E
1E030-1E08F   Cyrillic F

10A0-10FF   Georgian A
1C90-1CBF   Georgian B
2D00-2D2F   Georgian C

1200-139F   Ethiopic A
2D80-2DDE   Ethiopic B
AB00-AB2F   Ethiopic C

1000-109F   Myanmar A
AA60-AA7F   Myanmar B
A9E0-A9FF   Myanmar C

0900-097F   Devanagari A
A8E0-A8FF   Devanagari B

13A0-13FF   Cherokee A
AB70-ABBF   Cherokee B

0530-058F   Armenian
0590-05FF   Hebrew
0700-074F   Syriac
0780-07BF   Thaana
0980-09FF   Bengali
0A00-0A7F   Gurmukhi
3100-31BF   Bopomofo
0A80-0AFF   Gujarati
0B00-0B7F   Oriya
0B80-0BFF   Tamil
0C00-0C7F   Telugu
0C80-0CFF   Kannada
0D00-0D7F   Malayalam
0D80-0DFF   Sinhala  
07C0-07FF   Nkoo
0E00-0E7F   Thai
4DC0-4DFF   Yijing
0E80-0EFF   Lao
0F00-0FFF   Tibetan
1680-169F   Ogham
16A0-16FF   Runic
1700-171F   Tagalog
1720-173F   Hanunoo
1740-175F   Buhid
1760-177F   Tagbanwa
1800-18AF   Mongolian
1900-194F   Limbu
1980-19DF   New Tai Lue
1A00-1A1F   Buginese
1C50-1C7F   Ol Chiki
1950-197F   Tai Le
1A20-1AAD   Tai Tham
1CD0-1CF9   Vedic
2C00-2C5E   Glagolitic
2C80-2CFF   Coptic
2D30-2D7F   Tifinagh
A4D0-A4FF   Lisu
A500-A63F   Vai
A6A0-A6FF   Bamum
A980-A9DF   Javanese
A840-A87F   Phags-pa
ABC0-ABFF   Meetei Mayek
10330-1034F   Gothic
10380-1039F   Ugaritic
10100-1013F   Aegean
10300-1032F   Old Italic
10400-1044F   Deseret
10450-1047F   Shavian
10480-104AF   Osmanya
104B0-104FF   Osage
10800-1083F   Cypriot
10840-1085F   Imperial Aramaic
109A0-109FF   Meroitic Cursive
10A00-10A5F   Kharoshthi
10A60-10A7F   Old South Arabian
10B40-10B5F   Inscriptional Parthian
10B60-10B7F   Inscriptional Pahlavi
10C00-10C4F   Old Turkic
11000-1107F   Brahmi
110D0-110FF   Sora Sompeng
11100-1114F   Chakma
    '''.replace('\r\n','\n').replace(u'\xa0', u' ')
    pieces = [r.strip() for r in re.split('(  +|\n)', raw)]
    #print('Pieces:',pieces)
    pieces = list(filter(lambda s: s != '', pieces))
    ix = 0
    while ix<len(pieces):
        rng = pieces[ix]
        title = pieces[ix+1]
        lo_hi = [int('0x'+r.strip(),16) for r in rng.split('-')]
        if title in out:
            raise Exception('Duplicate entry: '+title)
        out[title] = lo_hi
        #if title=='2Latin':
        #    print('2latin')
        ix = ix+2
    return out

def cjk_blocks():
    # So many characters developed from a smashing together of.
    out = {}
    out['primary'] = [0x2F00, 0xA4CF]
    out['secondary'] = [0xF900, 0xFE4F]
    out['tertiary'] = [0x1D300, 0x1D35F]
    out['quaternary'] = [0x20000, 0x2A6DF]
    out['quinternary'] = [0x2F800, 0x2FA1F]
    return out

################################################################################

def str_hex(ix):
    out = str(hex(ix)).upper().replace('X','x')
    #while len(out)<7: # Always 5 digits.
    #    out = out.replace('0x','0x0')
    return out

def inside_range(jx, range_map):
    begin = False
    which_one = None
    for k in range_map.keys():
        if jx==range_map[k][0]:
            which_one = k
            begin = True
            break
        elif jx>range_map[k][0] and jx<=range_map[k][1]:
            which_one = k
            break
    return which_one, begin

def _python_valid(ix):
    valid = True; c = chr(ix)
    if c==' ' or c=='\n' or c=='\r' or c=='\t' or c=='\v' or c=='\f':
        return '(whitespace)'
    elif c=='=':
        return '(Python syntax)'
    elif ix<0x20:
        return ''
    try:
        exec(c+'=123123')
        return '(Python allowed)'
    except SyntaxError:
        try:
            exec('_'+c+'_=123123')
            return '(Python allowed, in-body)'
        except SyntaxError as e:
            if 'invalid non-printable character' in str(e):
                return '(unprintable)'
            elif 'invalid character' in str(e):
                return ''
            return '(Python syntax)'
        except (NameError, TypeError):
            return '(Python syntax)'
    except UnicodeEncodeError:
        return '(Python Unencodable)'

def python_valid(ix):
    out = _python_valid(ix)
    snake = chr(0x1f40d)
    happy = chr(0x1f60a)
    printr = chr(0x1f5b6)
    return out.replace('Python',snake).replace('allowed',happy).replace('unprintable','no '+printr).replace(' ','')

def canonical_wheretext(ix, txt0=None, chunk_size=512):
    if ix==0 and txt0=='':
        return ''
    if txt0 is None:
        txt0 = ''
    #numtxt = str_hex(ix)

    #Which block are we in?
    jxs = [ix, ix+chunk_size-1]
    num_txts = []
    range_map = ranges()
    for jx in jxs:
        which_one, begin = inside_range(jx, range_map)
        if which_one is None:
            which_one = '???'
        if begin:
            which_one = 'Begin: '+which_one
        pyv = ''
        #if jx==jxs[0]:
        pyv = python_valid(jx)
        accx = ''
        if 'Accents' in which_one:
            accx = 'x'
        txt = ' '.join([str_hex(jx), '('+accx+chr(jx)+')', which_one, pyv])
        num_txts.append(txt)

    # East asian special TODO:

    # Optional zeros after the 0x:
    out = num_txts[0]+' — '+num_txts[1]
    out = out.strip(); txt0 = txt0.strip()
    n_zero = 0; jx = 2 # Leading zeros are allowed and we try to preserve them.
    while jx<len(txt0):
        if txt0[jx]=='0':
            n_zero = n_zero+1
        else:
            break
        jx = jx+1
    if ix==0 and n_zero>0:
        n_zero = n_zero-1
    out = out.replace('0x','0x'+n_zero*'0')
    return out

def get_ix(txt):
    txt = txt.strip()
    if txt=='':
        return 0
    ix = None
    txt_autocorrect = txt

    txt = txt.strip()
    pieces = txt.split(' ')
    if pieces[0].startswith('0x') and len(pieces[0])>2:
        ix = int(pieces[0],16)

    elif len(pieces[0])==1 and ord(pieces[0])>255: # Single-char pieces (excluding ascii).
        ix = ord(pieces[0])
    elif 'CJK'.lower() in txt.lower() or 'Chinese'.lower() in txt.lower() or 'Japanese' in txt.lower() or 'Korean'.lower() in txt.lower():
        ix = cjk_blocks()['primary'][0]
    else:
        rngs = ranges()
        for k in list(rngs.keys()):
            rngs[k.lower()] = rngs[k]
        if txt.lower() in rngs:
            ix = rngs[txt.lower()][0]
    #print('ix is:', ix)
    return ix

def get_ix0(txt):
    # Greek => Greek A
    ix = get_ix(txt)
    if ix is None:
        return get_ix(txt.strip()+' A')
    return ix

def prev_group(ix):
    rngs = ranges()
    highest_below = 0
    jx = 0
    for k in rngs.keys():
        lohi = rngs[k]
        if lohi[0]>highest_below and lohi[0]<ix:
            jx = lohi[0]
            highest_below = jx
    if jx>0xE007F:
        return 0xE007F
    else:
        return jx

def next_group(ix):
    rngs = ranges()
    lowest_above = 0xFFFFFF
    jx = 0
    for k in rngs.keys():
        lohi = rngs[k]
        if lohi[0]<lowest_above and lohi[0]>ix:
            jx = lohi[0]
            lowest_above = lohi[0]
    if jx>0xE007F:
        return 0xE007F
    else:
        return jx

def prev_next_Sgroup(ix, isnext):
    range_map = ranges()
    which_one, begin = inside_range(ix, range_map)
    txt = 'ABCDEFGHIJKL'
    pairs = []
    for i in range(len(txt)-1):
        if isnext:
            pairs.append([' '+txt[i], ' '+txt[i+1]])
        else:
            pairs.append([' '+txt[i+1], ' '+txt[i]])
    #print('Old which one:', which_one)

    if which_one is not None:
        for p in pairs:
            which_one1 = which_one.replace(p[0],p[1])
            if which_one1 != which_one:
                which_one = which_one1
                break
        #print('New which one:', which_one)
        if which_one in range_map:
            if ix==range_map[which_one][0]:
                print('No more sister groups.')
            return range_map[which_one][0]
        else:
            print('No more sister groups.')
        return ix # No change.
    return ix # No change.

def prev_Sgroup(ix):
    return prev_next_Sgroup(ix, False)

def next_Sgroup(ix):
    return prev_next_Sgroup(ix, True)


def text_pieces(start_ix, end_ix):
    # Each piece is a differne group.
    r = ranges()
    vals = list(r.values())
    vals.sort()
    vals1 = []; actives = []
    for i in range(len(vals)-1):
        vals1.append([vals[i][0], vals[i][1]+1]); actives.append(True)
        vals1.append([vals[i][1]+1, vals[i+1][0]]); actives.append(False)

    txt = ''.join([chr(i) for i in range(start_ix, end_ix)])
    txt = txt.replace(chr(0),' ') #Problems with the zero char.

    out = []; actives1 = []
    for i in range(len(vals1)):
        vl = vals1[i]
        lo = max(vl[0], start_ix)
        hi = min(vl[1], end_ix)
        if hi>lo:
            out.append(txt[lo-start_ix:hi-start_ix])
            actives1.append(actives[i])
    return out, actives1
