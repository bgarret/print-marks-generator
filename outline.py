import cairo
import math
import StringIO
from units import *
import defaults

class OutlineCreator:

  def __init__(self, width, height, bleed=defaults.bleed, crop=defaults.crop):
    self.bleed, self.crop, self.width, self.height = bleed, crop, width, height

    self.print_marks = crop - bleed

    self.total_width = width + self.print_marks * 2
    self.total_height = height + self.print_marks * 2

    self.output = StringIO.StringIO()
    self.surface = cairo.PDFSurface(
        self.output,
        self.total_width * MM_TO_PT,
        self.total_height * MM_TO_PT
    )

  def create_context(self):
    context = cairo.Context(self.surface)
    context.set_source_rgb(0, 0, 0)
    context.set_line_width(0.2)

    # Allow drawing on the context using human-friendly units
    context.scale(MM_TO_PT, MM_TO_PT)

    return context

  def print_mark(self, x, y, margin):
    size = margin * 3. / 4.
    context = self.create_context()
    context.translate(x, y)

    # Circles
    context.arc(0, 0, 1./3. * margin, 0, math.pi * 2)
    context.arc(0, 0, 1./6. * margin, 0, math.pi * 2)

    # Vertical line
    context.move_to(0, -size / 2)
    context.line_to(0, size / 2)

    # Horizontal line
    context.move_to(-size / 2, 0)
    context.line_to(size / 2, 0)

    context.stroke()

  def print_line(self, x1, y1, x2, y2):
    context = self.create_context()
    context.move_to(x1, y1)
    context.line_to(x2, y2)
    context.stroke()

  def crop_width(self):
    return self.crop * 3. / 4.

  def create(self):
    # Top mark
    self.print_mark(
        self.total_width / 2,
        self.print_marks / 2,
        self.print_marks
    )
    # Bottom mark
    self.print_mark(
        self.total_width / 2,
        self.total_height - self.print_marks / 2,
        self.print_marks
    )
    # Left mark
    self.print_mark(
        self.print_marks / 2,
        self.total_height / 2,
        self.print_marks
    )
    # Right mark
    self.print_mark(
        self.total_width - self.print_marks/ 2,
        self.total_height / 2,
        self.print_marks
    )

    # Top cut
    self.print_line(
        0,
        self.crop,
        self.crop_width(),
        self.crop
    )
    self.print_line(
        self.total_width,
        self.crop,
        self.total_width - self.crop_width(),
        self.crop
    )
    # Bottom cut
    self.print_line(
        0,
        self.total_height - self.crop,
        self.crop_width(),
        self.total_height - self.crop
    )
    self.print_line(
        self.total_width,
        self.total_height - self.crop,
        self.total_width - self.crop_width(),
        self.total_height - self.crop
    )
    # Left cut
    self.print_line(
        self.crop,
        0,
        self.crop,
        self.crop_width()
    )
    self.print_line(
        self.crop,
        self.total_height,
        self.crop,
        self.total_height - self.crop_width()
    )
    # Right cut
    self.print_line(
        self.total_width - self.crop,
        0,
        self.total_width - self.crop,
        self.crop_width()
    )
    self.print_line(
        self.total_width - self.crop,
        self.total_height,
        self.total_width - self.crop,
        self.total_height - self.crop_width()
    )

    self.surface.flush()
    self.surface.finish()

    return self.output
