from PIL import Image
import argparse
import glob
import os

from dataset import *

CROP_SIZE = 128
# strange scale in the depth data
DEPTH_SCALE_FACTOR = 1e40

parser = argparse.ArgumentParser()
parser.add_argument('dataset_path')
parser.add_argument('processed_dataset_path')

args = parser.parse_args()

# set up folders
try:
    os.mkdir(args.processed_dataset_path)
except:
    pass
try:
    os.mkdir('%s/pos' % args.processed_dataset_path)
    os.mkdir('%s/neg' % args.processed_dataset_path)
except:
    pass

# file format string
# <pos|neg>/<original image id>-<bounding box id>.<png|tiff>
filename_format = '%s-%03i'

xid = 0
for path in glob.glob('%s/*/pcd*[0-9].txt' % args.dataset_path):
    print path
    sample_id = path[-len('1234.txt'):-len('.txt')]
    dim = convert_pcd(path)
    with Image.open(path[:-len('.txt')]+'r.png') as cimg:
        # positive grasps
        for i, box in enumerate(read_label_file(path[:-len('.txt')]+'cpos.txt')):
            filename = filename_format % (sample_id, i)
            crop_image(cimg, box, CROP_SIZE).save('%s/pos/%s.png' % (args.processed_dataset_path, filename))
            dimg = Image.new('F', (RAW_WIDTH, RAW_HEIGHT))
            dimg.putdata(dim.flatten() * DEPTH_SCALE_FACTOR)
            # crop_image(dimg, box, CROP_SIZE).save('%s/pos/%s.tiff' % (args.processed_dataset_path, filename))
            np.save('%s/pos/%s.npy' % (args.processed_dataset_path, filename), np.reshape(crop_image(dimg, box, CROP_SIZE).getdata(), (CROP_SIZE, CROP_SIZE)))

        # negative grasps
        for i, box in enumerate(read_label_file(path[:-len('.txt')]+'cneg.txt')):
            filename = filename_format % (sample_id, i)
            crop_image(cimg, box, CROP_SIZE).save('%s/neg/%s.png' % (args.processed_dataset_path, filename))
            dimg = Image.new('F', (RAW_WIDTH, RAW_HEIGHT))
            dimg.putdata(dim.flatten() * DEPTH_SCALE_FACTOR)
            # crop_image(dimg, box, CROP_SIZE).save('%s/neg/%s.tiff' % (args.processed_dataset_path, filename))
            np.save('%s/neg/%s.npy' % (args.processed_dataset_path, filename), np.reshape(crop_image(dimg, box, CROP_SIZE).getdata(), (CROP_SIZE, CROP_SIZE)))