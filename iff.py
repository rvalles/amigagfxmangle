import struct
class iffreader(object):
  def __init__(self,path):
    self.path=path
    self.fd=open(path, "rb")
    self.ftype=self.fd.read(4)
    if self.ftype!=b"FORM":
      raise Exception()
    self.ftype=self.ftype.decode("ascii")
    self.fsize=struct.unpack(">i",self.fd.read(4))[0]
    self.form=self.fd.read(4).decode("ascii")
    return
  def getchunk(self):
    f=self.fd
    while True:
      ctype=f.read(4).decode("ascii")
      if not ctype:
        break
      csize=struct.unpack(">i",f.read(4))[0]
      cdata=f.read(csize)
      if csize%2:
        f.read(1)
      yield [ctype, csize, cdata]
  def close(self):
    self.fd.close()
  def __del__(self):
    if not self.fd.closed:
      self.close()
class iffwriter(object):
  def __init__(self,path,form):
    self.path=path
    self.fd=open(path, "wb")
    f=self.fd
    f.write(b"FORM")
    f.write(struct.pack(">i",int(12)))
    if len(form)!=4:
      raise Exception()
    f.write(form.encode("ascii"))
    return
  def writechunk(self, ctype, cdata):
    f=self.fd
    f.write(ctype.encode("ascii"))
    f.write(struct.pack(">i",len(cdata)))
    f.write(cdata)
    if len(cdata)%2:
      f.write(b"\0")
  def close(self):
    f=self.fd
    fsize=f.tell()
    f.seek(4)
    f.write(struct.pack(">i",fsize))
    self.fd.close()
  def __del__(self):
    if not self.fd.closed:
      self.close()
