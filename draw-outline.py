#!/usr/bin/env python
from optparse import OptionParser
import os.path
from pyPdf import PdfFileWriter, PdfFileReader
from outline import OutlineCreator
from units import *
import defaults

# Option parsing
parser = OptionParser("Usage: %prog [options] filename\n\nAll lengths are expressed in millimeters")
parser.add_option("-c", "--crop-margin", type="float", dest="crop_margin", default=defaults.crop, help="crop margin, defaults to %s" % defaults.crop)
parser.add_option("-b", "--bleed-margin", type="float", dest="bleed_margin", default=defaults.bleed, help="bleed margin, defaults to %s" % defaults.bleed)
parser.add_option("-o", "--output", type="string", dest="output_filename", default=defaults.output, help="output filename, defaults to %s" % defaults.output)
parser.add_option("-n", "--no-bleed", action="store_true", dest="no_bleed", help="set this if the document doesn't have bleed margins, equivalent to setting the bleed margin to 0")

(options, args) = parser.parse_args()

if len(args) != 1 or not os.path.isfile(args[0]):
  parser.print_help()
  exit()

# Read the input and prepare the output document
filename = args[0]
document = PdfFileReader(file(filename, "rb"))
output = PdfFileWriter()

for page_num in range(document.getNumPages()):
  # Get the page dimensions
  page = document.getPage(page_num)
  box = page.mediaBox
  # PDF dimensions are in points
  width = round(float(box[2]) / MM_TO_PT)
  height = round(float(box[3]) / MM_TO_PT)

  # Create the outline
  outline_creator = OutlineCreator(
      width,
      height,
      bleed=(0 if options.no_bleed else options.bleed_margin),
      crop=options.crop_margin
  )
  outline = outline_creator.create()

  # Merge the outline with the current page and add it to the output
  output.addPage(PdfFileReader(outline).getPage(0))
  offset = outline_creator.print_marks * MM_TO_PT
  output.getPage(page_num).mergeTranslatedPage(page, offset, offset)


outputStream = file(options.output_filename, "wb")
output.write(outputStream)
outputStream.close()
