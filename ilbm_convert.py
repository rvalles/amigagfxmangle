#!/usr/bin/env python3
import sys, random
import pygame
import amigagfx
def main():
  pygame.init()
  filepath = sys.argv[1]
  srcpic = pygame.image.load(filepath)
  srcsize = srcwidth, srcheight = srcpic.get_width(), srcpic.get_height()
  screen = pygame.display.set_mode((srcwidth*2, srcheight*2))
  #screen = pygame.display.set_mode(srcsize)
  surface = pygame.Surface(srcsize)
  for posy in range(0, srcheight):
    srcrow = amigagfx.getrow(srcpic, posy, srcwidth)
    #amigagfx.drawrgb24row(surface, posy, srcrow)
  pygame.transform.scale2x(surface, screen)
  screen.blit(surface, (0, 0))
  pygame.display.flip()
  for posy in range(0, srcheight):
    srcrow = amigagfx.getrow(srcpic, posy, srcwidth)
    rgbrow = amigagfx.rgb24to12dithrnd(srcrow)
    #amigagfx.drawrgb12row(surface, posy, rgbrow)
    pygame.transform.scale2x(surface, screen)
    pygame.display.flip()
  srcrow = amigagfx.getrow(srcpic, 2, srcwidth)
  #ham6row = amigagfx.rgb24toham6md(srcrow)
  for posy in range(0, srcheight):
    srcrow = amigagfx.getrow(srcpic, posy, srcwidth)
    palette = []
    palette = [(x,x,x) for x in range(0,16)]
    #rgbrow = amigagfx.rgb24hamtest(srcrow)
    #amigagfx.drawrgb24row(surface, posy, rgbrow)
    srcrow = list(srcrow)
    rgbrow = amigagfx.rgb24to12(srcrow)
    #rgbrow = amigagfx.rgb24to12dithord(srcrow, posy%2)
    #rgbrow = amigagfx.rgb24to12dithrnd(srcrow)
    #palette = amigagfx.rgb12topalfreq(rgbrow)
    palette = amigagfx.rgb12topaldiff(rgbrow)
    #palette = rgb12topalydiff(rgbrow)
    #amigagfx.drawrgb12row(surface, posy, rgbrow)
    #grey4row = amigagfx.rgb24togrey4(srcrow)
    #grey4row = amigagfx.rgb24togrey4dithrnd(srcrow)
    #grey4row = amigagfx.rgb24togrey4dithord(srcrow, posy%2)
    #grey4row = amigagfx.rgb24togrey4dithhalf(srcrow, posy%2)
    #amigagfx.drawgrey4row(surface, posy, grey4row)
    #ham6row = amigagfx.rgb24toham6rr(srcrow)
    #ham6row = amigagfx.rgb24toham6md(srcrow, palette)
    ham6row = amigagfx.rgb24toham6mddithrnd(srcrow, palette)
    amigagfx.drawham6row(surface, posy, ham6row, palette)
    #amigagfx.drawham6maprow(surface, posy, ham6row)
    pygame.transform.scale2x(surface, screen)
    #screen.blit(surface, (0, 0))
    pygame.display.flip()
    #TODO: Write an ILBM
  done=False
  while not done:
    event = pygame.event.wait()
    if event.type==pygame.QUIT or event.type==pygame.MOUSEBUTTONDOWN:
      done=True
  pygame.quit()
if __name__ == "__main__":
  main()
