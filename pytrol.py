#!/usr/bin/python
import glob
import itertools
import numpy as np
import pynbody as pyn

def gasdir_iter(directory):
    """
    Return an iterator that spits out pynbody SimSnaps for each output.
    """
    dirglob = glob.glob(directory+'/*.[0-9]???[0-9]')
    dirglob.sort()
    pynload = lambda x: pyn.load(x)
    return itertools.imap(pynload, dirglob.__iter__())
    #return itertools.imap(pynload, dirglob.__iter__())

def t_Myr(sim):
    return sim.properties['time'].in_units('Myr')

def time_sequence(function, directory):
    """
    Take a function that returns a single value and return a tuple containing ([times], [function @ times])
    """
    seqfunc = lambda x: (t_Myr(x), function(x))
    tmplist = []
    [tmplist.append(i) for i in itertools.imap(seqfunc, gasdir_iter(directory))]
    tmplist = np.array(tmplist)
    return (tmplist[:,0], tmplist[:,1])

