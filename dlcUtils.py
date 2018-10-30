import pims
import pandas as pd


def load_tracked_whiskers(h5file):
    """
    Loads in a tracked whiskers h5 file and assumes only one scorer
    :param h5file:
    :return: pandas dataframe
    """
    points = pd.read_hdf(h5file)
    scorer = points.keys()[0][0]
    points=points[scorer]
    return(points)

def points2whisker(points,wid,num_pts_per_whisker=10):
    """
    takes the points from a loaded h5 file from DLC
    and outputs a dataframe structured with whisker id and frame numbers
    :param points: a pandas dataframe
    :return: whiskers - a pandas dataframe restructured for easy access to individual whiskers
    """
    body_part_labels = points.keys().levels[0]
    if len(body_part_labels) % num_pts_per_whisker != 0:
        raise ValueError('Number of Bodyparts is not divisible by number of points per whisker')

    pid = range(wid*num_pts_per_whisker,(wid+1)*num_pts_per_whisker)
    body_part_id = body_part_labels[pid]
    whisker = points[body_part_id]
    whisker.drop('likelihood',axis=1,level='coords',inplace=True)
    whisker = whisker.stack()
    return(whisker)










