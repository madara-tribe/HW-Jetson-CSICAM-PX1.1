# TCP ImageCompression from Jetson CSI or USB camera to Pyside(GUI)

It trasmit image from jetson to other PC (such as Mac) and plot GUI(Pyside).

It plot iage and calcurate how much it take time

・<b>CSI camera type</b> is 「SainSmart IMX219」


# How to use

## TCP Fast Retransmission and camera plot on GUI
<b>jetson side</b>
```sh
# Use USB camera
$ python3 main.py --usb -- port <optional port> 

# Use single CSI camera
$ python3 main.py --csi -- port <optional port> 

# Use dual CSI camera
$ python3 main.py --dual -- port <optional port> 
```

<b>the other side</b>
```sh
$ python3 main.py --qt -- port <optional port> 
```

## If only camera plot on GUI (No TCP)

add option [--plot] and rename "qtWidgets/VideoTread.py" fuction name.
```
$ python3 main.py --usb --plot -- port <optional port> <code>
```




# References
- [OpenCV Face Detection Example](https://doc.qt.io/qtforpython/examples/example_external__opencv.html)
