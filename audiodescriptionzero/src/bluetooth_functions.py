import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

# Dicionário para mapear o estado do número de toques
touch_count = 0

def on_touch_received(sender, signal):
    global touch_count
    touch_count += 1
    print(f"Touch interaction occurred: {touch_count} touches")

    # Reset touch count after a short delay to differentiate between sequences of touches
    GLib.timeout_add_seconds(1, reset_touch_count)

def reset_touch_count():
    global touch_count
    touch_count = 0
    return False  # Return False to stop the timeout from repeating

if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    # Substitute 'your.service.name' and '/your/service/path' with your actual Bluetooth device's DBus service and path
    service = bus.get_object('your.service.name', '/your/service/path')
    iface = dbus.Interface(service, dbus_interface='your.interface.name')

    # Substitute 'TouchEvent' with the actual name of the touch event signal from your device
    iface.connect_to_signal('TouchEvent', on_touch_received)

    loop = GLib.MainLoop()
    loop.run()
