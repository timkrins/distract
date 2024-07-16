import objc
from Cocoa import (
    NSApplication,
    NSApp,
    NSWindow,
    NSBackingStoreBuffered,
    NSApplicationActivationPolicyRegular,
    NSMakeRect,
    NSScreen,
    NSAppearance,
    NSAppearanceNameAqua,
    NSAppearanceNameDarkAqua,
    NSTextField,
    NSButton,
    NSBezelStyleRounded,
    NSColor,
    NSFont,
    NSTextAlignmentCenter,
    NSObject,
)
from AppKit import (
    NSWindowStyleMaskBorderless,
    NSWindowStyleMaskClosable,
    NSWindowStyleMaskTitled,
    NSWindowCollectionBehaviorCanJoinAllSpaces,
    NSFloatingWindowLevel,
)


def ScreenFrame():
    # Get the main screen's frame
    return NSScreen.mainScreen().frame()


def Label(origin, size):
    t = NSTextField.alloc().initWithFrame_((origin, size))
    t.setFont_(NSFont.systemFontOfSize_(14))
    t.setAlignment_(NSCenterTextAlignment)
    t.setDrawsBackground_(False)
    t.setBordered_(False)
    t.setEditable_(False)
    t.setSelectable_(True)
    return t


def CenteredButton(screen_frame, size):
    button_x = screen_frame.size.width / 2 - size[0] / 2
    button_y = screen_frame.size.height / 2 - size[1] / 2
    b = NSButton.alloc().initWithFrame_(((button_x, button_y), size))
    b.setBezelStyle_(NSBezelStyleRounded)
    return b


def FullscreenWindow(screen_frame):
    # Define the window size and position (full width, full height)
    window_rect = NSMakeRect(
        0, 0, screen_frame.size.width, screen_frame.size.height
    )  # (x, y, width, height)
    # Create the window
    window = NSWindow.alloc()
    window.initWithContentRect_styleMask_backing_defer_(
        window_rect,
        NSWindowStyleMaskBorderless
        | NSWindowStyleMaskClosable
        | NSWindowStyleMaskTitled,
        NSBackingStoreBuffered,
        False,
    )
    # Set window level to floating (always on top)
    window.setLevel_(NSFloatingWindowLevel)
    # Make the window borderless and always on top
    window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)
    # Respect Dark Mode
    if NSAppearance.currentAppearance().name() == NSAppearanceNameDarkAqua:
        window.setAppearance_(NSAppearance.appearanceNamed_(NSAppearanceNameDarkAqua))
    else:
        window.setAppearance_(NSAppearance.appearanceNamed_(NSAppearanceNameAqua))
    return window


class AppDelegate(NSObject):
    window = objc.IBOutlet()

    @objc.IBAction
    def closeWindow_(self, sender):
        self.window.performClose_(None)

    @property
    def closeWindowAction(self):
        return "closeWindow:"


def DistractAppDelegate():
    return AppDelegate.alloc().init()
