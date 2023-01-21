import argparse
import sys, os
import time
import yaml
import signal
from tcp_utils import ImgServer, ImgClient
from jetson_utils.main import jetson_main
        
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--qt', action='store_true', help='Pyside for GUI')
    parser.add_argument('--usb', action='store_true', help='USB camera')
    parser.add_argument('--csi', action='store_true', help='use 1 CSI camera: imx219 with v4l2 driver(example)')
    parser.add_argument('--dual', action='store_true', help='use 2 CSI cameras')
    parser.add_argument('--plot', action='store_true', help='just plot and not TCP socket trasmission to pyside')
    parser.add_argument('--mov', action='store_true', help='save 2 CSI camera frames was movie')
    parser.add_argument('--hyp', type=str, default='csicam_utils/hyp.csi.imx219.yaml', help='CSI IMX219 hyperparameters path')
    parser.add_argument('--height', type=int, default=840, help='height of movie')
    parser.add_argument('--width', type=int, default=840, help='width of of movie')
    parser.add_argument('--host', type=str, default='*************', help='host ip adress')
    parser.add_argument('--port', type=int, default=7000, help='port number')
    parser.add_argument('--video_path', type=str, default=None, help='video_path')
    opt = parser.parse_args()
    return opt
 
def run_pyside_gui(opt):
    from PySide6.QtWidgets import QApplication
    from qtWidgets.SingleCamWidget import SingleCamWidget
    server_ = ImgServer(opt.host, opt.port, protcol='ipv4', type='tcp')
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    try:
        w = SingleCamWidget(server=server_, opt=opt)
        w.setWindowTitle("PySide Layout on QMainWindow")
        w.resize(opt.width, opt.height)
        w.show()
        app.exec_()
    except KeyboardInterrupt:
        app.shutdown()
    sys.exit()
    
def main(opt, hyp):
    if opt.qt:
        run_pyside_gui(opt)
    elif opt.usb or opt.csi or opt.dual:
        if opt.plot or opt.mov:
            client_ = None
            jetson_main(opt, client_, hyp, plot=True)
        else:
            client_ = ImgClient(opt.host, opt.port, protcol='ipv4', type='tcp')
            jetson_main(opt, client_, hyp , plot=None)
        
if __name__ == '__main__':
    opt = get_parser()
    # load hyps dict
    with open(opt.hyp, errors='ignore') as f:
        hyp = yaml.safe_load(f)
    main(opt, hyp)

