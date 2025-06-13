# squixl_ui.py
import framebuf

# Configuration
TOUCH_PADDING = 5  # Extra pixels around each control for easier touching

# Helper: Convert 8-bit RGB to 16-bit RGB565
def rgb_to_565(r, g, b):
    """Convert 0–255 R,G,B to a 16-bit RGB565 value."""

    u16 = b >> 3
    u16 |= ((g >> 2) << 5)
    u16 |= ((r >> 3) << 11)
    return u16

    # return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

# Touch event types
TOUCH_TAP        = 0
TOUCH_DOUBLE     = 1
TOUCH_LONG       = 2
TOUCH_SWIPE_UP   = 3
TOUCH_SWIPE_RIGHT= 4
TOUCH_SWIPE_DOWN = 5
TOUCH_SWIPE_LEFT = 6
TOUCH_DRAG       = 7
TOUCH_DRAG_END   = 8
TOUCH_UNKNOWN    = 9

class TouchEvent:
    """Encapsulates a touch event."""
    def __init__(self, event_type, x, y):
        self.type = event_type
        self.x = x
        self.y = y

class UIControl:
    """Base class for all controls."""
    def __init__(self, x, y, w, h, title="", callback=None,
                 fg_color=0xFFFF, bg_color=0x0000, text_color=0xFFFF):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.callback = callback
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.text_color = text_color
        self.manager = None  # Set by UIManager

    def draw(self, buf: framebuf.FrameBuffer):
        raise NotImplementedError

    def within_bounds(self, x, y, w=None, h=None, pad=None):
        """Check if (x,y) is within padded bounds of this control."""
        w = w or self.w
        h = h or self.h
        pad = pad if pad is not None else TOUCH_PADDING
        return (self.x - pad <= x < self.x + w + pad) and (self.y - pad <= y < self.y + h + pad)

    def process_touch(self, evt: TouchEvent):
        """Handle touch event; return True if consumed."""
        return False

class UILabel(UIControl):
    """A simple text label."""
    def draw(self, buf,size=1):
        buf.large_text(self.title, self.x, self.y,size, self.text_color)

    def set_text(self, text):
        if self.manager:
            self.manager.buf.text(self.title, self.x, self.y, self.manager.current_screen.bg_color)

        self.title = text
        if self.manager:
            self.draw(self.manager.buf)

    def process_touch(self, evt: TouchEvent):
        # Labels don't consume touches, but log for debug
        # print(f"UILabel '{self.title}' touch at ({evt.x},{evt.y}) type={evt.type}")
        return False

class UIButton(UIControl):
    """A clickable button that flashes on tap."""
    def __init__(self, x, y, w, h, title="", callback=None,
                 fg_color=0xFFFF, bg_color=0x0000, text_color=0xFFFF):
        super().__init__(x, y, w, h, title, callback, fg_color, bg_color, text_color)
        self.flash = False

    def draw(self, buf):
        fill = self.fg_color if self.flash else self.bg_color
        border = self.text_color if self.flash else self.fg_color
        textcol = self.bg_color if self.flash else self.text_color
        buf.rect_round(self.x, self.y, self.w, self.h, 10, fill, True)
        buf.rect_round(self.x, self.y, self.w, self.h, 10, border)
        tw = len(self.title) * 8
        tx = self.x + (self.w - tw) // 2
        ty = self.y + (self.h - 8) // 2
        buf.text(self.title, tx, ty, textcol)

    def process_touch(self, evt: TouchEvent):
        # print(f"UIButton '{self.title}' touch at ({evt.x},{evt.y}) type={evt.type}")
        if evt.type == TOUCH_TAP and self.within_bounds(evt.x, evt.y):
            self.flash = True
            self.draw(self.manager.buf)
            if self.callback:
                self.callback()
            self.flash = False
            self.draw(self.manager.buf)
            return True
        return False

    def set_text(self, text):
        self.title = text
        if self.manager:
            self.draw(self.manager.buf)

class UISlider(UIControl):
    """A horizontal slider for selecting a value."""
    def __init__(self, x, y, w, h, min_val=0, max_val=100,
                 value=0, callback=None,
                 track_color=0xFFFF, knob_color=0xFFFF, bg_color=0x0000):
        super().__init__(x, y, w, h, "", callback,
                         track_color, bg_color, track_color)
        self.min = min_val
        self.max = max_val
        self.value = value
        self.knob_color = knob_color
        self.dragging = False

    def draw(self, buf):
        buf.rect_round(self.x, self.y, self.w, self.h, 5, self.bg_color, True)
        mid_y = self.y + self.h // 2
        buf.hline(self.x, mid_y, self.w, self.fg_color)
        rel = (self.value - self.min) / (self.max - self.min) if self.max != self.min else 0
        rel = max(0, min(1, rel))
        kx = self.x + int(rel * (self.w - 4))
        buf.fill_rect(kx, self.y + 1, 4, self.h - 2, self.knob_color)
        buf.rect_round(self.x, self.y, self.w, self.h, 5, self.fg_color)

    def process_touch(self, evt: TouchEvent):
        # print(f"UISlider touch at ({evt.x},{evt.y}) type={evt.type}")
        if evt.type in (TOUCH_TAP, TOUCH_DRAG) and self.within_bounds(evt.x, evt.y):
            rel = (evt.x - self.x) / float(self.w - 1 if self.w > 1 else 1)
            rel = max(0, min(1, rel))
            self.value = self.min + rel * (self.max - self.min)
            self.dragging = True
            self.draw(self.manager.buf)
            if self.callback:
                self.callback(self.value)
            return True
        if evt.type == TOUCH_DRAG_END and self.dragging:
            self.dragging = False
            self.draw(self.manager.buf)
            return True
        return False

    def set_value(self, val):
        self.value = max(self.min, min(self.max, val))
        self.draw(self.manager.buf)

class UICheckBox(UIControl):
    """A checkbox with a label; dark style with clear on/off indication."""
    def __init__(self, x, y, title, size=20, checked=False, callback=None,
                 fg_color=0xFFFF, bg_color=0x0000, check_color=0xFFFF,
                 label_color=0xFFFF):
        super().__init__(x, y, size, size, title, callback,
                         fg_color, bg_color, label_color)
        self.checked = checked
        self.check_color = check_color

    def draw(self, buf):
        buf.rect_round(self.x, self.y, self.w, self.h, 5, self.bg_color, True)
        buf.rect_round(self.x, self.y, self.w, self.h, 5, self.fg_color)
        if self.checked:
            # Draw inner box
            pad = max(3, self.w // 5)
            buf.rect_round(self.x + pad, self.y + pad,
                          self.w - 2 * pad, self.h - 2 * pad, 3,
                          self.check_color, True)
        # Center label vertically
        ly = self.y + (self.h - 8) // 2
        buf.text(self.title, self.x + self.w + 6, ly, self.text_color)

    def process_touch(self, evt: TouchEvent):
        # print(f"UICheckBox '{self.title}' touch at ({evt.x},{evt.y}) type={evt.type}")
        ext_w = self.w + 6 + len(self.title) * 8
        if evt.type == TOUCH_TAP and self.within_bounds(evt.x, evt.y, ext_w, self.h):
            self.checked = not self.checked
            self.draw(self.manager.buf)
            if self.callback:
                self.callback(self.checked)
            return True
        return False

    def set_checked(self, checked):
        self.checked = checked
        self.draw(self.manager.buf)

class UIProgressBar(UIControl):
    """A non-interactive progress bar."""
    def __init__(self, x, y, w, h, min_val=0, max_val=100,
                 value=0, track_color=0xFFFF,
                 fill_color=0xFFFF, bg_color=0x0000):
        super().__init__(x, y, w, h, "", None,
                         track_color, bg_color, track_color)
        self.min = min_val
        self.max = max_val
        self.value = value
        self.fill_color = fill_color

    def draw(self, buf):
        buf.rect_round(self.x, self.y, self.w, self.h, 5, self.bg_color, True)
        rel = (self.value - self.min) / (self.max - self.min) if self.max != self.min else 0
        rel = max(0, min(1, rel))
        fill_w = int(rel * (self.w - 2))
        buf.rect_round(self.x + 1, self.y + 1, fill_w, self.h - 2, 5, self.fill_color, True)
        buf.rect_round(self.x, self.y, self.w, self.h, 5, self.fg_color)

    def set_value(self, val):
        self.value = max(self.min, min(self.max, val))
        self.draw(self.manager.buf)

class UIScreen:
    """A container for grouping controls with a background color."""
    def __init__(self, name, bg_color=0x0000):
        self.name = name
        self.bg_color = bg_color
        self.controls = []
        self.manager = None

    def add_control(self, ctrl: UIControl):
        ctrl.manager = self.manager
        self.controls.append(ctrl)

class UIManager:
    """Manages multiple UIScreens and dispatches touch events."""
    def __init__(self, buf: framebuf2.FrameBuffer):
        self.buf = buf
        self.screens = {}
        self.current_screen = None

    def add_screen(self, screen: UIScreen):
        screen.manager = self
        self.screens[screen.name] = screen
        if self.current_screen is None:
            self.current_screen = screen

    def set_screen(self, name):
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' not found.")
        self.current_screen = self.screens[name]
        self.draw_all()

    def add(self, ctrl: UIControl):
        if self.current_screen is None:
            default = UIScreen("default")
            self.add_screen(default)
        self.current_screen.add_control(ctrl)

    def draw_all(self):
        if self.current_screen is None:
            return
        self.buf.fill(self.current_screen.bg_color)
        for ctrl in self.current_screen.controls:
            ctrl.draw(self.buf)

    def process_touch(self, evt: TouchEvent):
        if self.current_screen is None:
            return False
        for ctrl in self.current_screen.controls:
            if ctrl.process_touch(evt):
                return True
        return False
