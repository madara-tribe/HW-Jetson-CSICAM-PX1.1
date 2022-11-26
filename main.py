import argparse
import sys, os
import time
from tcp_utils import ImgServer, ImgClient
        
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--qt', action='store_true', help='Pyside for GUI')
    parser.add_argument('--usb', action='store_true', help='USB camera')
    parser.add_argument('--csi', action='store_true', help='1 frame of CSI camera: imx219 with v4l2 driver(example)')
    parser.add_argument('--dual', action='store_true', help='2 frame of CSI camera')
    parser.add_argument('--hyp', type=str, default='csicam_utils/hyp.csi.imx219.yaml', help='CSI IMX219 hyperparameters path')
    parser.add_argument('--height', type=int, default=640, help='height of movie')
    parser.add_argument('--width', type=int, default=840, help='width of of movie')
    parser.add_argument('--host', type=str, default='192.168.10.107', help='host url')
    parser.add_argument('--port', type=int, default=7000, help='port number')
    parser.add_argument('--video_path', type=str, default=None, help='video_path')
    opt = parser.parse_args()
    return opt
 
def main(opt):
    if opt.qt:
        from PySide6.QtWidgets import QApplication
        from qtWidgets.SingleCamWidget import SingleCamWidget
        server_sokect = ImgServer(opt.host, opt.port, protcol='ipv4', type='tcp')
        app = QApplication(sys.argv)
        try:
            w = SingleCamWidget(server_sokect=server_sokect)
            w.setWindowTitle("PySide Layout on QMainWindow")
            w.resize(opt.width, opt.height)
            w.show()
            sys.exit(app.exec_())
        except KeyboardInterrupt:
            app.shutdown()
    elif opt.usb or opt.csi or opt.dual:
        from jetson_utils.runner import jetson_main
        with open(opt.hyp, errors='ignore') as f:
            hyp = yaml.safe_load(f)  # load hyps dict
        client_ = ImgClient(opt.host, opt.port, protcol='ipv4', type='tcp')
        jetson_main(opt, client_)
        
if __name__ == '__main__':
    opt = get_parser()
    main(opt)

