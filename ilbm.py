import struct
import io
HAM_SET = 0
HAM_MODIFY_RED = 2
HAM_MODIFY_GREEN = 3
HAM_MODIFY_BLUE = 1
def decodeBMHD(h):
  (width, height, xOrigin, yOrigin, numPlanes, mask, compression, pad1, transClr, xAspect, yAspect, pageWidth, pageHeight) = struct.unpack(">HHhhBBBBHBBhh",h)
  print(f"{width}x{height}, {numPlanes} planes, compression: {compression}, mask: {mask}, aspect: {xAspect}:{yAspect}")
  return (width, height, numPlanes, mask, compression)
def encodeBMHD(width, height, numPlanes, mask, compression):
  return struct.pack(">HHhhBBBBHBBhh", width, height, 0, 0, numPlanes, mask, compression, 0, 0, 1, 1, width, height)
def decodeCMAP(c):
  palette=struct.iter_unpack(">BBB",c)
  return list(palette)
def encodeCMAP(palette):
  buf=b""
  for color in palette:
    buf+=struct.pack(">BBB",*color)
  return buf
def decodeCAMG(c):
  i = struct.unpack(">I",c)[0]
  print("CAMG: ", format(i, '#0x'))
  monitor = i&0xFFFF1000
  pal = monitor==0x21000
  ntsc = monitor==0x11000
  ehb = i&0x80
  ham6 = i&0x800
  lace = i&0x4
  hires = i&0x8000
  superhires = i&0x20
  return (ehb, ham6, hires, lace, pal, ntsc)
def uncompressBODY(rowsize, cbuf):
  fi = io.BytesIO(cbuf)
  fo = io.BytesIO()
  while True:
    a=fi.read(1)
    if a==b"":
      break
    a=a[0]
    if a > 128:
      b=fi.read(1)[0]
      fo.write(bytes([b]*(257-a)))
      continue
    if a < 128:
      fo.write(fi.read(a+1))
      continue
  return bytes(fo.getbuffer())
def getchunkyfromplanar(binplane):
  plane=[]
  for i in range(len(binplane)):
    plane.append([int(x) for x in ''.join([format(x,"08b") for x in binplane[i]])])
  return [sum([plane[n][x]<<n for n in range(len(plane))]) for x in range(len(plane[0]))]
def gethamfromchunky(pixels):
  return [(pixel>>4, pixel&0b1111) for pixel in pixels]        
def getrgb12fromfake24(p):
  return [(x>>4,y>>4,z>>4) for x,y,z in p]
