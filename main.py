import argparse
import yaml
from jetson_utils.csicam_single import run_csicam
from jetson_utils.dual_camera import run_dual_cam
        
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csi', action='store_true', help='use 1 CSI camera: imx219 with v4l2 driver(example)')
    parser.add_argument('--dual', action='store_true', help='use 2 CSI cameras')
    parser.add_argument('--plot', action='store_true', help='just plot and not TCP socket trasmission to pyside')
    parser.add_argument('--mov', action='store_true', help='save 2 CSI camera frames was movie')
    parser.add_argument('--hyp', type=str, default='csicam_utils/hyp.csi.imx219.yaml', help='CSI IMX219 hyperparameters path')
    parser.add_argument('--video_path', type=str, default=None, help='video_path')
    opt = parser.parse_args()
    return opt
 
    
def main(opt, hyp):
    if opt.csi:
        run_csicam(hyp, plot=opt.plot)
    elif opt.dual:
        run_dual_cam(opt, hyp)
        
if __name__ == '__main__':
    opt = get_parser()
    # load hyps dict
    with open(opt.hyp, errors='ignore') as f:
        hyp = yaml.safe_load(f)
    main(opt, hyp)

