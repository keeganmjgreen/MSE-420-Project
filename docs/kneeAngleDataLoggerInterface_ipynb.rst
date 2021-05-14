
``kneeAngleDataLoggerInterface.ipynb``
======================================

.. raw:: html
    :file: kneeAngleDataLoggerInterface_ipynb.html

The following fully-assembled Python module/script runs a very simple Windows UI for interfacing with an RC car, all made by me.

::

    from serial import Serial
    from win10toast import ToastNotifier
    from time import time
    from threading import Thread
    import ctypes
    import tkinter as tk
    toaster = ToastNotifier()
    port = 'COM4' # 'COM3'
    try:
        ser = Serial(port, baudrate = 115_200)
    except:
        while True:
            if toaster.show_toast('Connect the BLE link via USB', ' ',
                                  icon_path = 'ico/connect.ico',
                                  threaded = True):
                break
            try:
                ser = Serial(port, baudrate = 115_200)
                break
            except:
                pass
        try:
            ser
        except:
            while True:
                try:
                    ser = Serial(port, baudrate = 115_200)
                    break
                except:
                    pass
    connected_notified = False
    def connected_notifier():
        global connected_notified
        connected_tick = time()
        while True:
            connected_tock = time()
            connected_time = connected_tock - connected_tick
            if toaster.show_toast('BLE link connected',
                                  '%.1f seconds ago' % connected_time,
                                  icon_path = 'ico/connected.ico',
                                  threaded = True):
                connected_notified = True
                break
            print('connected_notifier waiting')
    Thread(target = connected_notifier).start()
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    window = tk.Tk()
    #window.resizable(False, False)
    window.configure(bg = 'white')
    window.iconbitmap('ico/window.ico')
    window.title('RC Car Interface')
    with open('rc_car_interface_instructions.txt') as file:
        instructions = ''.join(file.readlines())
    label = tk.Label(text = instructions, justify = tk.LEFT, font = ('Segoe UI Semilight', 12))
    label.config(bg = 'white')
    label.pack(padx = 100, pady = 100)
    def disconnected_notifier():
        disconnected_tick = time()
        while True:
            disconnected_tock = time()
            if connected_notified:
                disconnected_time = disconnected_tock - disconnected_tick
                if toaster.show_toast('BLE link disconnected',
                                      '%.1f seconds ago' % disconnected_time,
                                      icon_path = 'ico/disconnected.ico',
                                      threaded = True):
                    break
            print('disconnected_notifier waiting')
    disconnected = False
    closed = False
    def disconnected_checker():
        global disconnected
        while True:
            if not closed:
                try:
                    ser.read()
                except:
                    disconnected = True
                    try:
                        window.destroy()
                        window.quit()
                    except:
                        pass
                    disconnected_notifier()
                    break
            else:
                break
            print('disconnected_checker waiting')
    Thread(target = disconnected_checker).start()
    commands = ['v', 'l', 'B', 'r', 'a', 's', 'b', 'L', 'F', 'R']
    with open('rc_car_interface_actions.txt') as file:
        actions = file.readlines()
    def keypress_handler(event):
        try:
            index = int(event.char)
            command = commands[index]
            action = actions[index]
            ser.write(command.encode())
            print(action[:-1])
        except:
            try:
                ser.write(b's')
                window.destroy()
                window.quit()
            except:
                pass
        print('keypress_handler called')
    window.bind('<Key>', keypress_handler)
    window.mainloop()
    closed = True
    if not disconnected:
        def closed_notifier():
            closed_tick = time()
            while True:
                closed_tock = time()
                if connected_notified:
                    closed_time = closed_tock - closed_tick
                    if toaster.show_toast('BLE link interface closed',
                                          '%.1f seconds ago' % closed_time,
                                          icon_path = 'ico/closed.ico',
                                          threaded = True):
                        break
                print('closed_notifier waiting')
        Thread(target = closed_notifier).start()
    ser.__del__()    

----
