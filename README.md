# Dual cameras for CSI camera on Jetson (Stereo Visison)

## item name :waveshare IMX219-83



It fix csicamera as dual one and plot more horizontaly.

it became more easy to modify its accuracy and calibrate parameters.

<img width="664" alt="TCP" src="https://user-images.githubusercontent.com/48679574/204338150-34151466-100f-40da-9301-4bde6fe908a9.png">

# How to use (onlt on jetson)

```sh
# Use single CSI camera
$ python3 main.py --csi --plot

# Use dual CSI camera
$ python3 main.py --dual --plot

# Use dual camera and save as movie
$ python3 main.py --dual --mov
```




# References
- [OpenCV Face Detection Example](https://doc.qt.io/qtforpython/examples/example_external__opencv.html)
- [JetsonHacksNano/CSI-Camera](https://github.com/JetsonHacksNano/CSI-Camera)
