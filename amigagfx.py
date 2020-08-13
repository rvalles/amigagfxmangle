import random
import pygame
HAM_SET = 0
HAM_MODIFY_RED = 2
HAM_MODIFY_GREEN = 3
HAM_MODIFY_BLUE = 1
def getrow(surface, posy, width):
  for posx in range(0, width):
    yield surface.get_at((posx, posy))
#draw stuff
def draw1bitrow(surface, posy, pixels):
  posx=0
  for c in pixels:
    surface.set_at((posx,posy),(c*255,c*255,c*255))
    posx+=1
def drawrgb12row(surface, posy, pixels):
  posx=0
  for c in pixels:
    surface.set_at((posx,posy),((c.r<<4)+c.r,(c.g<<4)+c.g,(c.b<<4)+c.b))
    posx+=1
def drawgrey4row(surface, posy, pixels):
  posx=0
  for y in pixels:
    surface.set_at((posx,posy),((y<<4)+y,(y<<4)+y,(y<<4)+y))
    posx+=1
def drawrgb24row(surface, posy, pixels):
  posx=0
  for c in pixels:
    surface.set_at((posx,posy),(c.r,c.g,c.b))
    posx+=1
def draw12bitpaletterow(surface, posy, pixels, palette):
  posx=0
  for c in pixels:
    surface.set_at((posx,posy),((palette[c][0]<<4)+palette[c][0], (palette[c][1]<<4)+palette[c][1], (palette[c][2]<<4)+palette[c][2]))
    posx+=1
def draw24bitpaletterow(surface, posy, pixels, palette):
  posx=0
  for c in pixels:
    surface.set_at((posx,posy),(palette[c][0], palette[c][1], palette[c][2]))
    posx+=1
def drawham6row(surface, posy, pixels, palette):
  posx = 0
  r = g = b = 0
  for (mode, value) in pixels:
    if mode==HAM_SET:
        (r,g,b) = palette[value]
    elif mode==HAM_MODIFY_RED:
        r = value
    elif mode==HAM_MODIFY_GREEN:
        g = value
    elif mode==HAM_MODIFY_BLUE:
        b = value
    surface.set_at((posx,posy),((r<<4)+r, (g<<4)+g, (b<<4)+b))
    posx+=1
def drawham6maprow(surface, posy, pixels):
  posx = 0
  for (mode, value) in pixels:
    if mode==HAM_SET:
        surface.set_at((posx,posy),(255, 255, 255))
    elif mode==HAM_MODIFY_RED:
        surface.set_at((posx,posy),((value<<4)+value, 0, 0))
    elif mode==HAM_MODIFY_GREEN:
        surface.set_at((posx,posy),(0, (value<<4)+value, 0))
    elif mode==HAM_MODIFY_BLUE:
        surface.set_at((posx,posy),(0, 0, (value<<4)+value))
    posx+=1
#conversion stuff
def rgb24to12(pixels):
  for sc in pixels:
    r=sc.r>>4
    g=sc.g>>4
    b=sc.b>>4
    yield pygame.Color(r,g,b)
def rgb24to1bit(pixels):
  for sc in pixels:
    yield 1 if random.randrange(255) < sc.hsla[2]*2.55 else 0
def rgb24togrey4(pixels):
  for sc in pixels:
    sy=sc.hsla[2]*2.55
    yield int(sy)>>4
def rgb24togrey4dithrnd(pixels):
  for sc in pixels:
    sy=sc.hsla[2]*2.55
    y=int(sy)//17
    if random.randrange(17) < sy%17:
      y=min(y+1,15)
    yield int(y)
def rgb24togrey4dithord(pixels, odd):
  posx=0
  for sc in pixels:
    #sy = sc.hsla[2]*2.55
    sy = sc.g
    y = int(sy)>>4
    mr = (sy%16)//4
    if mr==1 and (posx+odd*2)%4==0:
      y=min(y+1,15)
    if mr==2 and (posx+odd)%2==1:
      y=min(y+1,15)
    if mr==3 and (posx+odd*2)%4!=2:
      y=min(y+1,15)
    yield int(y)
    posx+=1
def rgb24togrey4dithhalf(pixels, odd):
  posx=0
  for sc in pixels:
    #sy = sc.hsla[2]*2.55
    sy = sc.g
    y = int(sy)>>4
    mr = int(sy)&0b1000
    if mr and y<=7 and (posx+odd)%2!=0:
      y+=1
    if not mr and y>7 and (posx+odd)%2!=0:
      y-=1
    yield int(y)
    posx+=1
def rgb24togrey4dithord6(pixels, odd):
  posx=0
  for sc in pixels:
    #sy = sc.hsla[2]*2.55
    sy = sc.g
    y = int(sy)//17
    mr = (sy%17)//4
    if mr==1 and (posx+odd*3)%5==0:
      y=min(y+1,15)
    if mr==2 and (posx+odd)%5==0 or (posx+odd)%5==3:
      y=min(y+1,15)
      y=15
    if mr==3:
      if not odd and (posx)%2==0:
        y=min(y+1,15)
      elif posx%5!=0 and posx%5!=4:
        y=min(y+1,15)
      #y=15
    if mr==4 and (posx+odd*3)%5!=3:
      y=min(y+1,15)
    #if mr==4 and (posx+odd)%2==1:
    yield int(y)
    posx+=1
def rgb24to12dithrnd(pixels):
  for sc in pixels:
    r=sc.r//17
    if random.randrange(17) < sc.r%17:
      r=min(r+1,15)
    g=sc.g//17
    if random.randrange(17) < sc.g%17:
      g=min(g+1,15)
    b=sc.b//17
    if random.randrange(17) < sc.b%17:
      b=min(b+1,15)
    yield pygame.Color(r,g,b)
def rgb24to12dithord(pixels, odd):
  posx=0
  for sc in pixels:
    r = sc.r//16
    mr = (sc.r%16)//4
    if mr==1 and (posx+odd*2)%4==0:
      r=min(r+1,15)
    if mr==2 and (posx+odd)%2==1:
      r=min(r+1,15)
    if mr==3 and (posx+odd*2)%4!=2:
      r=min(r+1,15)
    g = sc.g//16
    mg = (sc.g%16)//4
    if mg==1 and (posx+odd*2)%4==0:
      g=min(g+1,15)
    if mg==2 and (posx+odd)%2==1:
      g=min(g+1,15)
    if mg==3 and (posx+odd*2)%4!=2:
      g=min(g+1,15)
    b = sc.b//16
    mb = (sc.b%16)//4
    if mb==1 and (posx+odd*2)%4==0:
      b=min(b+1,15)
    if mb==2 and (posx+odd)%2==1:
      b=min(b+1,15)
    if mb==3 and (posx+odd*2)%4!=2:
      b=min(b+1,15)
    yield pygame.Color(r,g,b)
    posx+=1
def rgb24toham6rr(pixels):
  mode = HAM_MODIFY_GREEN
  for sc in pixels:
    if mode==HAM_MODIFY_RED:
      value = sc.r>>4
    if mode==HAM_MODIFY_GREEN:
      value = sc.g>>4
    if mode==HAM_MODIFY_BLUE:
      value = sc.b>>4
    yield (mode, value)
    if mode==HAM_MODIFY_RED:
      mode = HAM_MODIFY_BLUE
    elif mode==HAM_MODIFY_GREEN:
      mode = HAM_MODIFY_RED
    elif mode==HAM_MODIFY_BLUE:
      mode = HAM_MODIFY_GREEN
def rgb24toham6md(pixels, palette):
  hc = pygame.Color(0,0,0)
  for sc in pixels:
    tr = sc.r>>4
    tg = sc.g>>4
    tb = sc.b>>4
    dr = abs(tr-hc.r)
    dg = abs(tg-hc.g)
    db = abs(tb-hc.b)
    dm = max(dr, dg, db)
    dc = [(1 if x else 0) for x in [dr,dg,db]].count(1)
    if dc > 1 and (tr,tg,tb) in palette:
      mode = HAM_SET
    elif dm == dg:
      mode = HAM_MODIFY_GREEN
    elif dm == dr:
      mode = HAM_MODIFY_RED
    else:
      mode = HAM_MODIFY_BLUE
    #return the color we selected
    if mode==HAM_MODIFY_RED:
      value = tr
      hc = pygame.Color(value, hc.g, hc.b)
    if mode==HAM_MODIFY_GREEN:
      value = tg
      hc = pygame.Color(hc.r, value, hc.b)
    if mode==HAM_MODIFY_BLUE:
      value = tb
      hc = pygame.Color(hc.r, hc.g, value)
    if mode==HAM_SET:
      value = palette.index((tr,tg,tb))
      hc = pygame.Color(tr,tg,tb)
    #print(mode, value)
    yield (mode, value)
def rgb24toham6mddithrnd(pixels, palette):
  hc = pygame.Color(0,0,0)
  for sc in pixels:
    tr = sc.r>>4
    tg = sc.g>>4
    tb = sc.b>>4
    dr = abs(tr-hc.r)
    dg = abs(tg-hc.g)
    db = abs(tb-hc.b)
    dm = max(dr, dg, db)
    dc = [(1 if x else 0) for x in [dr,dg,db]].count(1)
    if dc > 1 and (tr,tg,tb) in palette:
      mode = HAM_SET
    elif dm == dg:
      mode = HAM_MODIFY_GREEN
    elif dm == dr:
      mode = HAM_MODIFY_RED
    else:
      mode = HAM_MODIFY_BLUE
    #return the color we selected
    if mode==HAM_MODIFY_RED:
      value = sc.r//17
      if random.randrange(17) < sc.r%17:
        value=min(value+1,15)
      hc = pygame.Color(value, hc.g, hc.b)
    if mode==HAM_MODIFY_GREEN:
      value = sc.g//17
      if random.randrange(17) < sc.g%17:
        value=min(value+1,15)
      hc = pygame.Color(hc.r, value, hc.b)
    if mode==HAM_MODIFY_BLUE:
      value = sc.b//17
      if random.randrange(17) < sc.b%17:
        value=min(value+1,15)
      hc = pygame.Color(hc.r, hc.g, value)
    if mode==HAM_SET:
      value = palette.index((tr,tg,tb))
      hc = pygame.Color(tr,tg,tb)
    yield (mode, value)
def rgb24hamtest(pixels):
  c0 = c1 = c2 = c3 = 0
  hc = pygame.Color(0,0,0)
  for sc in pixels:
    dr = abs(sc.r//16-hc.r)
    dg = abs(sc.g//16-hc.g)
    db = abs(sc.b//16-hc.b)
    dm = [(1 if x else 0) for x in [dr,dg,db]].count(1)
    #print(dr, dg, db, dm)
    hc = pygame.Color(sc.r//16,sc.g//16,sc.b//16)
    if dm==0:
      ac = pygame.Color(0,0,0)
      c0+=1
    elif dm==1:
      ac = pygame.Color(0,0,255)
      c1+=1
    elif dm==2:
      ac = pygame.Color(255,0,0)
      c2+=1
    else:
      ac = pygame.Color(255,255,255)
      c3+=1
    yield ac
  print(c0, c1, c2, c3)
def rgb12topalfreq(pixels):
  c = []
  count = []
  for sc in pixels:
    if (sc.r, sc.g, sc.b) in c:
      count[c.index((sc.r, sc.g, sc.b))][0] += 1
    else:
      c.append((sc.r, sc.g, sc.b))
      count.append([1, len(c)-1])
  count.sort(reverse=True)
  count = count[:16]
  palette = [c[x] for (i,x) in count]
  print([(i,c[x]) for (i,x) in count])
  return palette
def rgb12topaldiffxx(pixels):
  hc = pygame.Color(0,0,0)
  palette_score = {}
  for sc in pixels:
    dr = abs(sc.r-hc.r)
    dg = abs(sc.g-hc.g)
    db = abs(sc.b-hc.b)
    dextra = sorted([dr,dg,db])
    hc = pygame.Color(sc.r,sc.g,sc.b)
    if any(dextra[:2]):
      palette_score[(sc.r, sc.g, sc.b)] = max(sum(dextra), palette_score.get((sc.r, sc.g, sc.b), 0))
  palette = [c for c, score in sorted(palette_score.items(), key=lambda x:x[1], reverse=True)[:16]]
  print([(score, c) for c, score in sorted(palette_score.items(), key=lambda x:x[1], reverse=True)[:16]])
  return palette
def rgb12topaldiff(pixels):
  hc = pygame.Color(0,0,0)
  c = []
  count = []
  for sc in pixels:
    dr = abs(sc.r-hc.r)
    dg = abs(sc.g-hc.g)
    db = abs(sc.b-hc.b)
    dm = 3-[dr, dg, db].count(0)
    hc = pygame.Color(sc.r,sc.g,sc.b)
    if dm > 1:
      if (sc.r, sc.g, sc.b) in c:
        idx = c.index((sc.r, sc.g, sc.b))
        count[idx][0] = max(count[idx][0], dr+dg+db)
      else:
        c.append((sc.r, sc.g, sc.b))
        count.append([dr+dg+db, len(c)-1])
  count.sort(reverse=True)
  count = count[:16]
  palette = [c[x] for (i,x) in count]
  print([(i,c[x]) for (i,x) in count])
  return palette
def rgb12topalydiff(pixels):
  #c0 = c1 = c2 = c3 = 0
  hc = pygame.Color(0,0,0)
  c = []
  count = []
  for sc in pixels:
    dr = abs(sc.r-hc.r)
    dg = abs(sc.g-hc.g)
    db = abs(sc.b-hc.b)
    dm = [(1 if x else 0) for x in [dr,dg,db]].count(1)
    if dm > 1 and not (sc.r, sc.g, sc.b) in c:
      dy = abs(sc.hsla[2]-hc.hsla[2])
      c.append((sc.r, sc.g, sc.b))
      count.append([dy, len(c)-1])
    hc = pygame.Color(sc.r,sc.g,sc.b)
  count.sort(reverse=True)
  count = count[:16]
  palette = [c[x] for (i,x) in count]
  print([(i,c[x]) for (i,x) in count])
  return palette
