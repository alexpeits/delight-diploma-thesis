import numpy
#import re
#from watchdog.events import FileSystemEventHandler

#from ..config import *


def get_diff(v_list):
    """
    Takes an array containing multiple arrays as an
    argument, and constructs a new array, with the
    same number of sub-arrays, each one with an element
    less, that contains the difference between consecutive
    elements of each sub-array of the original argument.
    It is used as a step to create the weights for each
    LightSensor, corresponding to each light. v_list is
    each LightSensor's setup_table

    :type v_list: NxM list
    :rtype: (N-1)xM list

    """
    d_list = [range(10), range(10)]
    for i in xrange(len(v_list)):
        for j in xrange(len(v_list[i])-1):
            diff = v_list[i][j+1] - v_list[i][j]
            d_list[i][j] = diff if (diff >= 0) else 1

    return d_list

def get_mean(d_list):
    """
    Takes an array containing multiple arrays as an
    argument, and constructs a new array, with the
    same number of sub-arrays, each one containing a
    single value, the mean value of each sub-array.
    It is used to construct the weights for each
    LightSensor

    :type d_list: NxM list
    :rtype: 1xM list

    """
    m_list = []
    for i in xrange(len(d_list)):
        m_list.append(numpy.mean((d_list[i])))
    return m_list

def get_next_dim(m_list, s_list_func, thresh):
    """
    This function takes the arguments:
    m_list: contains the mean value of v_list
    s_list: current sensor values
    thresh: threshold light value
    and returns an array for the value to add
    to the light intensity. For a negative value,
    we subtract.

    :type m_list: 1xM list
    :type s_list_func: 1xM list
    :type thresh: int
    :rtype: 1xM list

    """

    s_list_lin = [(10.0*(thresh - i)) for i in s_list_func]
    try:
        l_add = list(numpy.linalg.solve(m_list, s_list_lin))
        return l_add
    except numpy.linalg.linalg.LinAlgError:
        # This exception is raised in case of Singular Matrix.
        # In this case we treat each sensor as if it only
        # depends on the nearest bulb.
        l_add = [(s_list_lin[i]/m_list[i][i]) for i in range(len(s_list_lin))]
        return l_add

'''
class GUIDataChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):

        #print event.src_path + " modified!"
        ch_file_obj = re.search(r"[\w0-9]+$", event.src_path)
        ch_file = ch_file_obj.group()
        with open(event.src_path, "r") as f:
            gui_data[ch_file] = f.read()
'''
