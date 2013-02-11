import gobject
import pygtk
pygtk.require('2.0')
from gtk import *

try:
    from sr import *
    dummy = False
except ImportError:
    print "Running as a dummy controller."
    dummy = True

from panels import create_panel_by_class_name, create_panel

UPDATE_FREQUENCY = 100

class Controller:

    ## Internal methods ##

    def display_panel(self, panel):
        if self.current_panel <> None:
            self.current_panel.hide_all()
            self.hpaned.remove(self.current_panel)

        self.hpaned.pack2(panel)
        panel.show_all()
        panel.emit("panel-update")
        self.current_panel = panel

    def select_prev_panel(self):
        def previous(model, tree_iter):
            prev = model.get_iter_first()
            if model.get_path(prev) == model.get_path(tree_iter):
                # This is the first item in the list
                return None

            while model.get_path(model.iter_next(prev)) <> model.get_path(tree_iter):
                prev = model.iter_next(prev)

            return prev

        sel = self.panel_list.get_selection()
        prev_iter = previous(self.panel_list_store, sel.get_selected()[1])
        if prev_iter != None:
            sel.select_path(self.panel_list_store.get_path(prev_iter))

    def select_next_panel(self):
        sel = self.panel_list.get_selection()
        next_iter = self.panel_list_store.iter_next(sel.get_selected()[1])
        if next_iter != None:
            sel.select_path(self.panel_list_store.get_path(next_iter))

    ## Event handlers ##

    def get_focus(self, widget, event, data=None):
        if not self.timer_on:
            self.start_timer()

    def lose_focus(self, widget, event, data=None):
        self.stop_timer()

    def key_press(self, widget, event):
        # I only managed to find the keysyms members by guessing from gdkkeysyms.h
        if event.keyval == keysyms.Left:
            self.select_prev_panel()

        elif event.keyval == keysyms.Right:
            self.select_next_panel()

        elif event.keyval == keysyms.space:
            self.stop_button.set_state(STATE_ACTIVE)
            # Stop all motors
            if self.robot != None:
                for i in range(len(self.robot.motors)):
                    self.robot.motors[i].target = 0

        else:
            self.current_panel.emit("key-press-event", event)

        return True  # stop the event from triggering stuff we don't want

    def key_release(self, widget, event):
        if event.keyval == keysyms.space:
           self.stop_button.set_state(STATE_NORMAL)

    def selected_panel_changed(self, tree_selection):
        sel_iter = self.panel_list.get_selection().get_selected()[1]
        panel = self.panel_list_store.get_value(sel_iter, 1)
        self.display_panel(panel)

    # Close event handler
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        main_quit()

    ## Update timer ##

    def start_timer(self):
        """Starts the timer that emits update signals at the current panel."""
        gobject.timeout_add(UPDATE_FREQUENCY, self.timer_tick)
        self.timer_on = True

    def timer_tick(self):
        """Emits an update signal at the current panel, and checks the number
           of running motors."""
        if not self.timer_on:
            return False

        self.current_panel.emit("panel-update")

        # Check to see whether motors are running
        if self.robot != None:
            motor_running = False
            for i in range(len(self.robot.motors)):
                if self.robot.motors[i].target != 0:
                    motor_running = True
                    break

            if motor_running:
                self.stop_button.show()
            else:
                self.stop_button.hide()

        return True

    def stop_timer(self):
        self.timer_on = False

    ## Constructor ##

    def __init__(self, R = None):
        window = Window(WINDOW_TOPLEVEL)

        window.set_events(gdk.KEY_PRESS_MASK)

        # Properties
        window.set_title("Manual Controller" if R != None else
                            "Manual Controller (dummy)")
        window.set_property("default-width", 480)
        window.set_property("default-height", 272)
        window.set_border_width(5)

        # Update timer (registering custom signal)
        gobject.signal_new("panel-update", Widget, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
        self.start_timer()

        # List data
        panel_list_store = ListStore(str, Widget)
        self.robot = R
        if R == None:
            panel_list_store.append(["IO Board 0", create_panel_by_class_name(self, "IOPanel")])
            panel_list_store.append(["Servo Board 0", create_panel_by_class_name(self, "ServoPanel")])
            panel_list_store.append(["Motor Board 0", create_panel_by_class_name(self, "MotorPanel")])

        else:
            for i in range(len(R.io)):
                panel_list_store.append(["IO Board " + str(i),
                                        create_panel(self, R.io[i])])

            for i in range(len(R.servos)):
                panel_list_store.append(["Servo Board " + str(i),
                                        create_panel(self, R.servos[i])])

            for i in range(len(R.motors)):
                panel_list_store.append(["Motor Board " + str(i),
                                        create_panel(self, R.motors[i])])

        # Panel list
        panel_list = TreeView(panel_list_store)
        tvcol = TreeViewColumn("Board")
        panel_list.append_column(tvcol)
        cell = CellRendererText()
        tvcol.pack_start(cell, True)
        tvcol.set_attributes(cell, text=0)
        first_path = panel_list_store.get_path(panel_list_store.get_iter_first())
        panel_list.get_selection().select_path(first_path)

        stop_button = Button("Press to stop")
        stop_button.modify_bg(STATE_NORMAL, gdk.Color(1.0, 0.2, 0.2))
        self.stop_button = stop_button

        left_table = Table(2, 1, False)
        left_table.attach(panel_list, 0, 1, 0, 1)
        left_table.attach(stop_button, 0, 1, 1, 2, yoptions=SHRINK)

        # Horizontal paning
        hpaned = HPaned()
        hpaned.pack1(left_table)
        hpaned.set_position(128)

        window.add(hpaned)
        window.show_all()
        stop_button.hide()

        # Event handlers
        window.connect("delete_event", self.delete_event)
        window.connect("destroy", self.destroy)
        window.connect("focus-in-event", self.get_focus)
        window.connect("focus-out-event", self.lose_focus)
        window.connect("key-press-event", self.key_press)
        window.connect("key-release-event", self.key_release)

        panel_list.get_selection().connect("changed", self.selected_panel_changed)

        # Set class variables
        self.panel_list_store = panel_list_store
        self.panel_list = panel_list
        self.window = window
        self.hpaned = hpaned

        self.current_panel = None

        # Display the first panel
        self.selected_panel_changed(panel_list.get_selection())

    def main(self):
        main()

if dummy:
    cont = Controller()
else:
    cont = Controller(Robot(init_vision = False))

cont.main()
