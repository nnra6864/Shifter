import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GtkLayerShell, GdkPixbuf, GLib, Gdk
import subprocess
import signal

class ScreenshotOverlay(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_namespace(self, "Transitioner")
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.EXCLUSIVE)
        self.set_app_paintable(True)
        self.connect("draw", self.on_draw)
        self.connect("destroy", Gtk.main_quit)
        self.opacity = 1.0
        self.screenshot = None

    def take_screenshot(self):
        process = subprocess.Popen(["grim", "-t", "ppm", "-"], stdout=subprocess.PIPE)
        screenshot_data, _ = process.communicate()
        loader = GdkPixbuf.PixbufLoader.new_with_type('pnm')
        loader.write(screenshot_data)
        loader.close()
        self.screenshot = loader.get_pixbuf()
        self.show_all()

    def on_draw(self, widget, cr):
        if self.screenshot:
            Gdk.cairo_set_source_pixbuf(cr, self.screenshot, 0, 0)
            cr.paint_with_alpha(self.opacity)
        return False

    def fade_out(self):
        self.opacity -= 0.025
        if self.opacity <= 0:
            self.destroy()
            return False
        self.queue_draw()
        return True

    def start_fade_out(self):
        GLib.timeout_add(16, self.fade_out)

def handle_signal(signum, frame):
    if signum == signal.SIGUSR1:
        overlay.start_fade_out()

def main():
    global overlay
    overlay = ScreenshotOverlay()
    overlay.take_screenshot()
    signal.signal(signal.SIGUSR1, handle_signal)
    Gtk.main()

if __name__ == "__main__":
    main()
