import pygtk
pygtk.require('2.0')
from gtk import *


class Controller:
    ## Internal methods ##

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
        if prev_iter <> None:
            sel.unselect_all()
            sel.select_path(self.panel_list_store.get_path(prev_iter))

    def select_next_panel(self):
        sel = self.panel_list.get_selection()
        next_iter = self.panel_list_store.iter_next(sel.get_selected()[1])
        if next_iter <> None:
            sel.unselect_all()
            sel.select_path(self.panel_list_store.get_path(next_iter))


    ## Event handlers ##

    def get_focus(self, widget, event, data=None):
        print "get focus"

    def lose_focus(self, widget, event, data=None):
        print "lose focus"

    def key_press(self, widget, event):
        # I only managed to find the keysyms members in gdkkeysyms.h
        if event.keyval == keysyms.Up:
            print "Up"

        elif event.keyval == keysyms.Down:
            print "Down"

        elif event.keyval == keysyms.Left:
            self.select_prev_panel()

        elif event.keyval == keysyms.Right:
            self.select_next_panel()

        elif event.keyval == keysyms.Page_Up:
            print "Page up"

        elif event.keyval == keysyms.Page_Down:
            print "Page down"
        
        return True  # stop the event from triggering stuff we don't want

    # Close event handler
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        main_quit()

    def __init__(self):
        window = Window(WINDOW_TOPLEVEL)

        # Event handlers
        window.connect("delete_event", self.delete_event)
        window.connect("destroy", self.destroy)
        window.connect("focus-in-event", self.get_focus)
        window.connect("focus-out-event", self.lose_focus)
        window.connect("key-press-event", self.key_press)

        window.set_events(gdk.KEY_PRESS_MASK)

        # Properties
        window.set_property("default-width", 480)
        window.set_property("default-height", 272)
        window.set_border_width(5)

        # Sample list data
        panel_list_store = ListStore(str)
        panel_list_store.append(["Foo"])
        panel_list_store.append(["Bar"])
        panel_list_store.append(["Baz"])

        # Panel list
        panel_list = TreeView(panel_list_store)
        tvcol = TreeViewColumn("Board")
        panel_list.append_column(tvcol)
        cell = CellRendererText()
        tvcol.pack_start(cell, True)
        tvcol.set_attributes(cell, text=0)
        first_path = panel_list_store.get_path(panel_list_store.get_iter_first())
        panel_list.get_selection().select_path(first_path)
        panel_list.show()

        # Table
        table = Table(1, 2, False)
        table.attach(panel_list, 0, 1, 0, 1, SHRINK)

        window.add(table)
        window.show_all()
        
        # Set class variables
        self.panel_list_store = panel_list_store
        self.panel_list = panel_list
        self.window = window
        self.table = table

    def main(self):
        main()


cont = Controller()
cont.main()
