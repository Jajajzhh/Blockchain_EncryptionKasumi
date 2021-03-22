#!/usr/bin/env python
#Examples of irreductible polynomes 16 degree
#x^16 + x^9 + x^8 + x^7 + x^6 + x^4 + x^3 + x^2 + 1
#x^16 + x^12 + x^3 + x^1 + 1
#x^16 + x^12 + x^7 + x^2 + 1
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_gcdex, gf_strip
def gf_inv(a):  # irriducible polynomial  
    # mod = 0x18f57 => x^16 + x^15 + x^11 + x^10 + x^9 + x^8 + x^6 + x^4 + x^2 + x^1 + 1 Polynome irreductible
    mod = [1,1,0,0,0,1,1,1,1,0,1,0,1,0,1,1,1]
    a = hextolist(a)
    s, t, g = gf_gcdex(ZZ.map(gf_strip(a)), ZZ.map(mod), 2 , ZZ)
    return listtohex(s)
def gf_degree(a) :
  res = 0
  a >>= 1
  while (a != 0) :
    a >>= 1
    res += 1
  return res

def gf_invert(a, mod) :
  v = mod
  g1 = 1
  g2 = 0
  j = gf_degree(a) - 8

  while (a != 1) :
    if (j < 0) :
       a, v = v, a
       g1, g2 = g2, g1
       j = -j

    a ^= v << j
    g1 ^= g2 << j

    a %= 256  # Emulating 8-bit overflow
    g1 %= 256 # Emulating 8-bit overflow

    j = gf_degree(a) - gf_degree(v)

  return g1

def hextolist(num) :
    outlist = [1 if num & (1 << (15-n)) else 0 for n in range(16)]
    return outlist

def listtohex(bitlist) :
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out

if __name__ == '__main__':
    a = 0xf48  
    s = gf_inv(a)
    print(hex(s))
    b = 0x4ccd
    s = gf_inv(b)
    print(hex(s))
