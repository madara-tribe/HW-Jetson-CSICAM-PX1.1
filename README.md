# Dual cameras for CSI camera on Jetson (Stereo Visison)

## item name 「waveshare IMX219-83」



It fix csicamera as dual one and plot more horizontaly.

it became more easy to modify its accuracy and calibrate parameters.

<img width="500" alt="TCP" src="https://github.com/madara-tribe/HW-Jetson-CSICAM-PX1.1/assets/48679574/5f8230ba-60d4-42f7-bcd5-88365200ac23">


# setup CSI camera (make image more clear)
```sh
#https://mirai-tec.hatenablog.com/entry/2021/08/09/175835
$ wget https://www.waveshare.com/w/upload/e/eb/Camera_overrides.tar.gz
$ tar zxvf Camera_overrides.tar.gz
$ sudo cp camera_overrides.isp /var/nvidia/nvcam/settings/
$ sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.isp
$ sudo chown root:root /var/nvidia/nvcam/settings/camera_overrides.isp
```


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
