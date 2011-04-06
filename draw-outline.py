#!/usr/bin/env python
from optparse import OptionParser
import os.path
from pyPdf import PdfFileWriter, PdfFileReader
from outline import OutlineCreator, MM_TO_PT

# Option parsing
parser = OptionParser("Usage: %prog [options] filename")
parser.add_option("-c", "--crop-margin", type="float", dest="crop_margin", default=15.)
parser.add_option("-b", "--bleed-margin", type="float", dest="bleed_margin", default=5.)
parser.add_option("-o", "--output", type="string", dest="output_filename", default="outline.pdf")
parser.add_option("-n", "--no-bleed", action="store_true", dest="no_bleed")

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
      bleed=options.bleed_margin,
      crop=options.crop_margin,
      no_bleed=options.no_bleed
  )
  outline = outline_creator.create()

  # Merge the outline with the current page and add it to the output
  output.addPage(PdfFileReader(outline).getPage(0))
  offset = (outline_creator.crop if options.no_bleed else outline_creator.print_marks) * MM_TO_PT
  output.getPage(page_num).mergeTranslatedPage(page, offset, offset)


outputStream = file(options.output_filename, "wb")
output.write(outputStream)
outputStream.close()
