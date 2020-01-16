# Tools for manipulating Amiga images

The original intent was to write a bunch of trivial and less trivial algorithms to convert pictures to Amiga hold-and-modify (HAM6/HAM8) video mode, particularly sliced ham6 images (SHAM), where the indexed palette is changed dynamically in order to minimize HAM fringing.

Currently featuring:
* Methods to read and write ILBM files (and IFF files).
* Tool to display ILBM files.
* Several algorithms to convert any image pygame can read into 4bit greyscale, rgb12 with a few methods of dithering, sliced HAM6.

Writing sliced HAM6 images to ILBM is still pending, until I investigate the unofficial extensions to ILBM for dynamic palette changes. Some methods to make non-sliced HAM6 images will likely be written first.

Here's a sample SHAM picture, parrots from the Kodak test image set.
![kodak23 parrots sham](https://b.rvalles.net/unsorted/kodak23_parrots_sham.png)

Same SHAM parrots, but recovering some rgb24 detail via probability-based dithering done in HAM.
![kodak23 parrots sham](https://b.rvalles.net/unsorted/kodak23_parrots_sham_dither_rnd.png)