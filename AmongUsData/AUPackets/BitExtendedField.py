from scapy.compat import raw
from scapy.error import warning
from scapy.fields import Field


def _int2raw(i):
    sevens = []
    x = i
    while x >= 128:
        sevens.append(0x80 | (x & 0x7F))
        x = x >> 7
    sevens.append(x & 0x7F)
    return raw(sevens)


def _raw2int(b=""):
    o = i = 0
    while i < len(b) and b[i] & 0x80:
        o = o + ((b[i] & 0x7F) << 7*i)
        i += 1
    if o == len(b):
        warning("Broken Bit Extended: no ending byte")
    o = o + ((b[i] & 0x7F) << 7 * i)
    i += 1
    return b[i:], o



# def str2vlenq(s=""):
#     i = l = 0
#     while i < len(s) and ord(s[i]) & 0x80:
#         l = l << 7
#         l = l + (ord(s[i]) & 0x7F)
#         i = i + 1
#     if i == len(s):
#         warning("Broken vlenq: no ending byte")
#     l = l << 7
#     l = l + (ord(s[i]) & 0x7F)
#
#     return s[i+1:], l


class AUBitExtendedField(Field):
    def i2m(self, pkt, i):
        if i is None:
            i = 0
        return _int2raw(i)

    def m2i(self, pkt, m):
        if m is None:
            return None, 0
        return _raw2int(m)[1]

    def addfield(self, pkt, s, val):
        return s+self.i2m(pkt, val)

    def getfield(self, pkt, s):
        return _raw2int(s)

