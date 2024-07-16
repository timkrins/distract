import rumps
import requests
from distract_view import (
    CenteredButton,
    FullscreenWindow,
    DistractAppDelegate,
    ScreenFrame,
)
from distract_logic import (
    load_calendar_events,
    filter_future_events,
    format_date,
    is_in_next_minute,
)
import os

calendar_url = os.environ["CALENDAR_URL"]


class Distract(rumps.App):
    app_delegate = DistractAppDelegate()

    def __init__(self, *args, **kwargs):
        super(Distract, self).__init__(*args, **kwargs)
        self.load_calendar_items()
        self.create_menu_items()
        self.start_alert_timer()
        self.shown_alerts = []
        rumps.notification("Distract", "Now running", "Notifications will be shown one minute before event.")

    def format_event(self, event):
        return f"{format_date(event['begin'])} - {event['name']}"

    def load_calendar_items(self):
        calendar_events = load_calendar_events(calendar_url)
        next_events = filter_future_events(calendar_events)
        self.calendar_items = next_events[:10]

    def create_menu_items(self):
        print("create_menu_items...")
        for event in self.calendar_items:
            self.menu.add(
                rumps.MenuItem(
                    self.format_event(event), callback=self.menu_item_callback
                )
            )
        print("create_menu_items: done")

    def start_alert_timer(self):
        # Schedule the timer to check every ten seconds
        rumps.Timer(self.check_alerts, 10).start()

    def check_alerts(self, _):
        for event in self.calendar_items:
            if is_in_next_minute(event["begin"]):
                formatted = self.format_event(event)
                if not formatted in self.shown_alerts:
                    self.fullscreen_alert(formatted)
                    self.shown_alerts.append(formatted)

    def menu_item_callback(self, sender):
        self.fullscreen_alert(sender.title)

    def fullscreen_alert(self, text):
        # Get the main screen's frame
        screen_frame = ScreenFrame()
        # Create the window
        window = FullscreenWindow(screen_frame)
        # Set to the delegate
        self.app_delegate.window = window
        # Create a close button and set its properties
        button = CenteredButton(screen_frame, (300, 300))
        button.setTarget_(self.app_delegate)
        button.setAction_(self.app_delegate.closeWindowAction)
        button.setTitle_(text)
        window.contentView().addSubview_(button)
        # Show the window
        window.orderFrontRegardless()
        # Ensure the window is not released when closed
        window.setReleasedWhenClosed_(False)

    @rumps.clicked("URL")
    def show_url(self, _):
        rumps.alert(calendar_url)


if __name__ == "__main__":
    Distract("Distract", icon="icon.icns").run()
