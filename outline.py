import cairo
import math
import StringIO
from units import *

class OutlineCreator:

  def __init__(self, width, height, bleed=5., crop=15., no_bleed=False):
    self.bleed, self.crop, self.width, self.height = bleed, crop, width, height

    self.print_marks = crop - bleed

    offset = self.crop if no_bleed else self.print_marks
    self.total_width = width + offset * 2
    self.total_height = height + offset * 2

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

    context.scale(MM_TO_PT, MM_TO_PT)

    return context

  def put_circle(self, context, x, y, radius):
    context.arc(x, y, radius, 0, math.pi * 2)
    context.stroke()

  def print_mark(self, x, y, margin):
    context = self.create_context()
    context.translate(x, y)

    self.put_circle(context, 0, 0, 1./3. * margin)
    self.put_circle(context, 0, 0, 1./6. * margin)

    context.move_to(0, -3./8. * margin)
    context.line_to(0, 3./8. * margin)

    context.move_to(-3./8. * margin, 0)
    context.line_to(3./8. * margin, 0)

    context.stroke()

  def print_line(self, x1, y1, x2, y2):
    context = self.create_context()
    context.move_to(x1, y1)
    context.line_to(x2, y2)
    context.stroke()

  def crop_width(self):
    return self.crop * 3. / 4.

  def create(self):
    # Top
    self.print_mark(
        self.total_width / 2,
        self.print_marks / 2,
        self.print_marks
    )
    # Bottom
    self.print_mark(
        self.total_width / 2,
        self.total_height - self.print_marks / 2,
        self.print_marks
    )
    # Left
    self.print_mark(
        self.print_marks / 2,
        self.total_height / 2,
        self.print_marks
    )
    # Right
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
