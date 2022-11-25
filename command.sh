#/bin/sh
#https://mirai-tec.hatenablog.com/entry/2021/08/09/175835
wget https://www.waveshare.com/w/upload/e/eb/Camera_overrides.tar.gz
tar zxvf Camera_overrides.tar.gz
sudo cp camera_overrides.isp /var/nvidia/nvcam/settings/
sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.ispsudo chown root:root /var/nvidia/nvcam/settings/camera_overrides.isp
