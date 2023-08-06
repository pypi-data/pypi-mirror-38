# DriveFiller(dot)py
A python library that creates very large files very quickly.
Please DO NOT use in any malicious form. This has been made for the sole purpose of testing on systems you have the
permission to break. We (Conor and Ben) accept no responsibility for any consequences you may recieve or damage you
may cause.

## Examples
To write 500 lines in the file 'text.txt' stored in 'C:\Documents\' with the text 'Hello World!' and check size in bytes:
```
import drivefiller as df
Filler_Object = df.filler('C:\Documents\', 'text', 'Hello World!', 500)
Filler_Object.fill()
print(Filler_Object.checkSize())
```