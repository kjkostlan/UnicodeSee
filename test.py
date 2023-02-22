# Simple tests.
import layout, evt_check, codepoints

#print('Testing range:', codepoints.get_ix('0'), '|', codepoints.canonical_wheretext(0))
#print('Testing get_ix:', codepoints.inside_range(0x20, codepoints.ranges()))
#print('Testing get_ix2:', codepoints.inside_range(0x1790, codepoints.ranges())) #Khmer
#print('Testing get_ix3:', codepoints.inside_range(0x2C6D, codepoints.ranges())) #2C60-27CF   Latin C
print('Testing Annoy:', codepoints.python_valid(0xD800))
