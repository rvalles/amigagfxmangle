#!/usr/bin/env python3
import sys
import iff
import ilbm
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
  f = iff.iffwriter("test.iff", "ILBM")
  #for ctype, cdata in chunks.items():
    #f.writechunk(ctype, cdata)
  (width, height, numPlanes, mask, compression) = ilbm.decodeBMHD(chunks["BMHD"])
  f.writechunk("BMHD", ilbm.encodeBMHD(width, height, numPlanes, mask, False))
  palette = ilbm.decodeCMAP(chunks["CMAP"])
  f.writechunk("CMAP", ilbm.encodeCMAP(palette))
  f.writechunk("CAMG", chunks["CAMG"])
  rowsize=((width+15)//16)*2
  body = chunks["BODY"]
  if compression == 1:
    body = ilbm.uncompressBODY(rowsize, body)
  #body = ilbm.compressBODY(rowsize, body)
  f.writechunk("BODY", body)
  f.close()
if __name__ == "__main__":
  main()
