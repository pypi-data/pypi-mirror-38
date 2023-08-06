import unittest

from gi.repository import Gtk

import time

# http://unpythonic.blogspot.com/2007/03/unit-testing-pygtk.html
def refresh_gui(delay=0):
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)
    time.sleep(delay)

import _importer
import gtkmvc3


class M(gtkmvc3.Model):
    store = 2.0
    __observables__ = ("store",)

class C(gtkmvc3.Controller):
    def register_adapters(self):
        self.adapt()

    def property_store_value_change(self, model, old, new):
        self.store = (old, new)


class T(unittest.TestCase):
    def setUp(self):
        self.m = M()
        self.v = gtkmvc3.View(builder="adapter20.ui")

    def testBuilder(self):
        # https://bugzilla.gnome.org/show_bug.cgi?id=629640
        self.assertEqual(1.0, self.v["store"].get_value())

    def testOutput(self):
        # https://bugzilla.gnome.org/show_bug.cgi?id=627468
        self.assert_(self.v["store"])
        c = C(self.m, self.v)
        refresh_gui()
        self.assertEqual(2.0, self.v["store"].get_value())
        return c

    def testInput(self):
        c = self.testOutput()
        self.v["spinner"].spin(Gtk.SpinType.STEP_FORWARD, 1)
        self.assertEqual(3.0, self.m.store)
        self.assertEqual((2.0, 3.0), c.store)

if __name__ == "__main__":
    unittest.main()
