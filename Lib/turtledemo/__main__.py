#!/usr/bin/env python3

"""
  ----------------------------------------------
      turtleDemo - Help
  ----------------------------------------------

  This document has two sections:

  (1) How to use the demo viewer
  (2) How to add your own demos to the demo repository


  (1) How to use the demo viewer.

  Select a demoscript from the example menu.
  The (syntax coloured) source code appears in the left
  source code window. IT CANNOT BE EDITED, but ONLY VIEWED!

  - Press START button to start the demo.
  - Stop execution by pressing the STOP button.
  - Clear screen by pressing the CLEAR button.
  - Restart by pressing the START button again.

  SPECIAL demos are those which run EVENTDRIVEN.
  (For example clock.py - or oldTurtleDemo.py which
  in the end expects a mouse click.):

      Press START button to start the demo.

      - Until the EVENTLOOP is entered everything works
      as in an ordinary demo script.

      - When the EVENTLOOP is entered, you control the
      application by using the mouse and/or keys (or it's
      controlled by some timer events)
      To stop it you can and must press the STOP button.

      While the EVENTLOOP is running, the examples menu is disabled.

      - Only after having pressed the STOP button, you may
      restart it or choose another example script.

   * * * * * * * *
   In some rare situations there may occur interferences/conflicts
   between events concerning the demo script and those concerning the
   demo-viewer. (They run in the same process.) Strange behaviour may be
   the consequence and in the worst case you must close and restart the
   viewer.
   * * * * * * * *


   (2) How to add your own demos to the demo repository

   - Place the file in the same directory as turtledemo/__main__.py
     IMPORTANT! When imported, the demo should not modify the system
     by calling functions in other modules, such as sys, tkinter, or
     turtle. Global variables should be initialized in main().

   - The code must contain a main() function which will
     be executed by the viewer (see provided example scripts).
     It may return a string which will be displayed in the Label below
     the source code window (when execution has finished.)

   - In order to run mydemo.py by itself, such as during development,
     add the following at the end of the file:

    if __name__ == '__main__':
        main()
        mainloop()  # keep window open

    python -m turtledemo.mydemo  # will then run it

   - If the demo is EVENT DRIVEN, main must return the string
     "EVENTLOOP". This informs the demo viewer that the script is
     still running and must be stopped by the user!

     If an "EVENTLOOP" demo runs by itself, as with clock, which uses
     ontimer, or minimal_hanoi, which loops by recursion, then the
     code should catch the turtle.Terminator exception that will be
     raised when the user presses the STOP button.  (Paint is not such
     a demo; it only acts in response to mouse clicks and movements.)
"""
import sys
import os

from tkinter import *
from idlelib.Percolator import Percolator
from idlelib.ColorDelegator import ColorDelegator
from idlelib.textView import view_text # TextViewer
from importlib import reload
from turtledemo import __doc__ as about_turtledemo

import turtle
import time

demo_dir = os.path.dirname(os.path.abspath(__file__))

STARTUP = 1
READY = 2
RUNNING = 3
DONE = 4
EVENTDRIVEN = 5

menufont = ("Arial", 12, NORMAL)
btnfont = ("Arial", 12, 'bold')
txtfont = ('Lucida Console', 8, 'normal')

def getExampleEntries():
    return [entry[:-3] for entry in os.listdir(demo_dir) if
            entry.endswith(".py") and entry[0] != '_']

help_entries = (  # (help_label,  help_doc)
    ('Turtledemo help', __doc__),
    ('About turtledemo', about_turtledemo),
    ('About turtle module', turtle.__doc__),
    )

class DemoWindow(object):

    def __init__(self, filename=None):
        self.root = root = turtle._root = Tk()
        root.title('Python turtle-graphics examples')
        root.wm_protocol("WM_DELETE_WINDOW", self._destroy)

        if sys.platform == 'darwin':
            import subprocess
            # Make sure we are the currently activated OS X application
            # so that our menu bar appears.
            p = subprocess.Popen(
                    [
                        'osascript',
                        '-e', 'tell application "System Events"',
                        '-e', 'set frontmost of the first process whose '
                              'unix id is {} to true'.format(os.getpid()),
                        '-e', 'end tell',
                    ],
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                )

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, minsize=90, weight=1)
        root.grid_columnconfigure(2, minsize=90, weight=1)
        root.grid_columnconfigure(3, minsize=90, weight=1)

        self.mBar = Menu(root, relief=RAISED, borderwidth=2)
        self.mBar.add_cascade(menu=self.makeLoadDemoMenu(self.mBar),
                              label='Examples', underline=0, font=menufont)
        self.mBar.add_cascade(menu=self.makeHelpMenu(self.mBar),
                              label='Help', underline=0, font=menufont)
        root['menu'] = self.mBar

        pane = PanedWindow(orient=HORIZONTAL, sashwidth=5,
                           sashrelief=SOLID, bg='#ddd')
        pane.add(self.makeTextFrame(pane))
        pane.add(self.makeGraphFrame(pane))
        pane.grid(row=0, columnspan=4, sticky='news')

        self.output_lbl = Label(root, height= 1, text=" --- ", bg="#ddf",
                                font=("Arial", 16, 'normal'), borderwidth=2,
                                relief=RIDGE)
        self.start_btn = Button(root, text=" START ", font=btnfont,
                                fg="white", disabledforeground = "#fed",
                                command=self.startDemo)
        self.stop_btn = Button(root, text=" STOP ", font=btnfont,
                               fg="white", disabledforeground = "#fed",
                               command=self.stopIt)
        self.clear_btn = Button(root, text=" CLEAR ", font=btnfont,
                                fg="white", disabledforeground="#fed",
                                command = self.clearCanvas)
        self.output_lbl.grid(row=1, column=0, sticky='news', padx=(0,5))
        self.start_btn.grid(row=1, column=1, sticky='ew')
        self.stop_btn.grid(row=1, column=2, sticky='ew')
        self.clear_btn.grid(row=1, column=3, sticky='ew')

        Percolator(self.text).insertfilter(ColorDelegator())
        self.dirty = False
        self.exitflag = False
        if filename:
            self.loadfile(filename)
        self.configGUI(NORMAL, DISABLED, DISABLED, DISABLED,
                       "Choose example from menu", "black")
        self.state = STARTUP


    def onResize(self, event):
        cwidth = self._canvas.winfo_width()
        cheight = self._canvas.winfo_height()
        self._canvas.xview_moveto(0.5*(self.canvwidth-cwidth)/self.canvwidth)
        self._canvas.yview_moveto(0.5*(self.canvheight-cheight)/self.canvheight)

    def makeTextFrame(self, root):
        self.text_frame = text_frame = Frame(root)
        self.text = text = Text(text_frame, name='text', padx=5,
                                wrap='none', width=45)

        self.vbar = vbar = Scrollbar(text_frame, name='vbar')
        vbar['command'] = text.yview
        vbar.pack(side=LEFT, fill=Y)
        self.hbar = hbar = Scrollbar(text_frame, name='hbar', orient=HORIZONTAL)
        hbar['command'] = text.xview
        hbar.pack(side=BOTTOM, fill=X)

        text['font'] = txtfont
        text['yscrollcommand'] = vbar.set
        text['xscrollcommand'] = hbar.set
        text.pack(side=LEFT, fill=BOTH, expand=1)
        return text_frame

    def makeGraphFrame(self, root):
        turtle._Screen._root = root
        self.canvwidth = 1000
        self.canvheight = 800
        turtle._Screen._canvas = self._canvas = canvas = turtle.ScrolledCanvas(
                root, 800, 600, self.canvwidth, self.canvheight)
        canvas.adjustScrolls()
        canvas._rootwindow.bind('<Configure>', self.onResize)
        canvas._canvas['borderwidth'] = 0

        self.screen = _s_ = turtle.Screen()
        turtle.TurtleScreen.__init__(_s_, _s_._canvas)
        self.scanvas = _s_._canvas
        turtle.RawTurtle.screens = [_s_]
        return canvas

    def configGUI(self, menu, start, stop, clear, txt="", color="blue"):
        self.mBar.entryconfigure(0, state=menu)

        self.start_btn.config(state=start,
                              bg="#d00" if start == NORMAL else "#fca")
        self.stop_btn.config(state=stop,
                             bg="#d00" if stop == NORMAL else "#fca")
        self.clear_btn.config(state=clear,
                              bg="#d00" if clear == NORMAL else"#fca")
        self.output_lbl.config(text=txt, fg=color)

    def makeLoadDemoMenu(self, master):
        menu = Menu(master)

        for entry in getExampleEntries():
            def loadexample(x):
                def emit():
                    self.loadfile(x)
                return emit
            menu.add_command(label=entry, underline=0,
                             font=menufont, command=loadexample(entry))

        return menu

    def makeHelpMenu(self, master):
        menu = Menu(master)

        for help_label, help_file in help_entries:
            def show(help_label=help_label, help_file=help_file):
                view_text(self.root, help_label, help_file)
            menu.add_command(label=help_label, font=menufont, command=show)

        return menu

    def refreshCanvas(self):
        if self.dirty:
            self.screen.clear()
            self.dirty=False

    def loadfile(self, filename):
        self.clearCanvas()
        turtle.TurtleScreen._RUNNING = False
        modname = 'turtledemo.' + filename
        __import__(modname)
        self.module = sys.modules[modname]
        with open(self.module.__file__, 'r') as f:
            chars = f.read()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", chars)
        self.root.title(filename + " - a Python turtle graphics example")
        reload(self.module)
        self.configGUI(NORMAL, NORMAL, DISABLED, DISABLED,
                       "Press start button", "red")
        self.state = READY

    def startDemo(self):
        self.refreshCanvas()
        self.dirty = True
        turtle.TurtleScreen._RUNNING = True
        self.configGUI(DISABLED, DISABLED, NORMAL, DISABLED,
                       "demo running...", "black")
        self.screen.clear()
        self.screen.mode("standard")
        self.state = RUNNING

        try:
            result = self.module.main()
            if result == "EVENTLOOP":
                self.state = EVENTDRIVEN
            else:
                self.state = DONE
        except turtle.Terminator:
            self.state = DONE
            result = "stopped!"
        if self.state == DONE:
            self.configGUI(NORMAL, NORMAL, DISABLED, NORMAL,
                           result)
        elif self.state == EVENTDRIVEN:
            self.exitflag = True
            self.configGUI(DISABLED, DISABLED, NORMAL, DISABLED,
                           "use mouse/keys or STOP", "red")

    def clearCanvas(self):
        self.refreshCanvas()
        self.screen._delete("all")
        self.scanvas.config(cursor="")
        self.configGUI(NORMAL, NORMAL, DISABLED, DISABLED)

    def stopIt(self):
        if self.exitflag:
            self.clearCanvas()
            self.exitflag = False
            self.configGUI(NORMAL, NORMAL, DISABLED, DISABLED,
                           "STOPPED!", "red")
        turtle.TurtleScreen._RUNNING = False

    def _destroy(self):
        self.root.destroy()


def main():
    demo = DemoWindow()
    demo.root.mainloop()

if __name__ == '__main__':
    main()
