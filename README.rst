zplgen
======

zplgen is a utility library to aid in generating ZPL2 code.

The core idiom is the `Command` class, which subclasses `bytes`. Another helper is the `Font` class.

Example usage
-------------

.. code:: python

  f_default = Font('V', height=30)

  label = bytes()

  label += Command.label_start()
  label += Command.label_home(30, 0)

  label += Command.graphic_circle(x=550, y=15, diameter=100, border=6)
  label += Command.field('?', x=560, y=50, font=f_default(45))

  label += Command.field(name, x=0, y=135, font=f_default)

  label += Command.label_end()

  send_to_printer(label)
