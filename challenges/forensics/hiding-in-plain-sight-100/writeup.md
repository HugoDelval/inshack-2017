# Solution

The challenge consists of a single PNG file: the flag is hidden inside, we hence need to analyze its content.

A good resource to understand what's going on is the [PNG specification](http://www.libpng.org/pub/png/spec/1.2/), more specifically the part about the [overall structure](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html) of a PNG file.

You'll learn that a PNG file is divided in chunks: the first one is named the IHDR and contains info about the file (width, height etc), and its is typically followed by one or many IDAT chunks containing the actual image data.

PNG lets users create their own custom chunks: you just have to follow some naming conventions given in the above pages to specify if the chunk is standard, optional, etc. If a chunk is specified as optional, any PNG file reader will simply ignore it if it doesn't know what to do with it.

In this case, examining the chunks of the PNG shows the usual (IHDR, IDAT, IEND chunks), plus a weird inSa chunk. Extracting that chunk yields a binary file. Using the `file` command shows that it's a standard JPG file, and opening it with an image viewer shows the flag!

