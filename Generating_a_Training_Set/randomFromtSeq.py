import pims
import os
import sys
import numpy as np
import skimage.io as io
import glob


def extract_ims(seq,n_ims,p_save=None):
    """
    saves randomly distributed frames from the image to label
    param: seq - a filename of a seq file. This probably works on any video
    though
    param: m_ims - number of images to extract uniformly
    param: p_save - the path to save to
    """

    p_load,basename = os.path.split(seq)
    if p_save is None:
        p_save=p_load
    print('Saving to {}'.format(p_save))    
    V = pims.NorpixSeq(seq)
    nframes = V.header_dict['allocated_frames']
    print('Found {} frames'.format(nframes))
    num_pad = int(np.floor(np.log10(nframes)+1))
    frame_numbers = np.random.choice(np.arange(nframes),n_ims,replace=False)
    frame_numbers.sort()
    for frame_number in frame_numbers:
        print(frame_number)
        try:
            I = V.get_frame(frame_number)
            io.imsave(os.path.join(p_save,'{}_img{:0{num_pad}d}.png'.format(os.path.splitext(basename)[0],
                                                                            frame_number,
                                                                            num_pad=num_pad)),
                      I)
        except:
            print('failed at {}'.format(frame_number))
            continue
    return(0) 

if __name__=='__main__':
    """ First argument is either a seq file or a path with seq files. Second
    argument is the number of frames to extract
    """
    if len(sys.argv)==4:
        p_save=sys.argv[3]
        if not os.path.isdir(p_save):
            os.makedirs(p_save)
    else:
        p_save=None

    n_ims = int(sys.argv[2])
    if os.path.isdir(sys.argv[1]):
        print('Extracting {} images from {} videos in {}'.format(n_ims,len(sys.argv[1]),sys.argv[1]))
        for seq in glob.glob(os.path.join(sys.argv[1],'*.seq')):
            print('working on {}'.format(seq))
            extract_ims(seq,n_ims,p_save)
    else:
        print('Extracting {} images from {}'.format(n_ims,sys.argv[1]))            
        extract_ims(sys.argv[1],n_ims,p_save)
