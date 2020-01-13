#!/usr/bin/env python3
import sys
import iff
import ilbm
import amigagfx
import pygame
def main():
  filepath = sys.argv[1]
  f = iff.iffreader(filepath)
  print(f"Type: {f.ftype}, Size: {f.fsize}, Form: {f.form}")
  chunks=dict()
  for chunktype, chunksize, chunkdata in f.getchunk():
    print(f"Chunk: {chunktype}, Size: {chunksize}")
    if chunktype in chunks:
      print("Dupe!")
    chunks[chunktype] = chunkdata
  if f.form != "ILBM":
    print("File is not ILBM.")
    sys.exit(1)
  if "ANNO" in chunks:
    print("Annotation found:", {chunks["ANNO"]})
  (width, height, numPlanes, mask, compression) = ilbm.decodeBMHD(chunks["BMHD"])
  if "CAMG" in chunks:
    ehb, ham6, hires, lace, pal, ntsc = ilbm.decodeCAMG(chunks["CAMG"])
  else:
    ehb = False
    ham6 = False
    hires = False
    lace = False
    pal = False
    ntsc = False
  palette = ilbm.decodeCMAP(chunks["CMAP"])
  print("Mode: ", end='')
  if hires:
    print("HIRES ", end='')
  if lace:
    print("LACE ", end='')
  if ham6:
    print("HAM6 ", end='')
  if ehb:
    print("EHB ", end='')
  if pal:
    print("PAL ", end='')
  if ntsc:
    print("NTSC ", end='')
  print("")
  palette = ilbm.getrgb12fromfake24(palette)
  print(f"palette: {len(palette)} colors.")
  rowsize=((width+15)//16)*2
  if compression > 1:
    print("Unsupported compression type.")
    sys.exit(1)
  if compression == 1:
    chunks["BODY"] = ilbm.uncompressBODY(rowsize, chunks["BODY"])
  print("BODY size:", len(chunks["BODY"]))
  plane=[]
  for i in range(numPlanes):
    plane.append([])
  for posy in range(0, height*numPlanes):
    plane[posy%numPlanes]+=chunks["BODY"][posy*rowsize:posy*rowsize+rowsize]
  pixels=ilbm.getchunkyfromplanar(plane)
  if ham6:
      pixels=ilbm.gethamfromchunky(pixels)
  #print(plane[0][0:320])
  #print(pixels[0:320])
  #Display
  #pixels=[int(x) for x in ''.join([format(x,"08b") for x in plane[0]])]
  pygame.init()
  srcsize = width, height
  screen = pygame.display.set_mode((width*2, height*2))
  #screen = pygame.display.set_mode((width, height))
  surface = pygame.Surface(srcsize)
  for posy in range(0, height):
    posx=0
    srcrow=pixels[posy*width:posy*width+width]
    #draw1bitrow(surface, posy, srcrow)
    if ham6:
      amigagfx.drawham6row(surface, posy, srcrow, palette)
      #ilbm.drawham6maprow(surface, posy, srcrow)
    else:
      amigagfx.draw12bitpaletterow(surface, posy, srcrow, palette)
    #draw24bitpaletterow(surface, posy, srcrow, palette)
    pygame.transform.scale2x(surface, screen)
    #screen.blit(surface, (0, 0))
    pygame.display.flip()
  done=False
  while not done:
    event = pygame.event.wait()
    if event.type==pygame.QUIT or event.type==pygame.MOUSEBUTTONDOWN:
      done=True
  pygame.quit()
if __name__ == "__main__":
  main()
