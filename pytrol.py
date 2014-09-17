#!/usr/bin/python
import glob
import itertools
import numpy as np
import pynbody as pyn
import multiprocessing

def gasdir_iter(directory):
    """
    Return an iterator that spits out pynbody SimSnaps for each output.
    """
    dirglob = glob.glob(directory+'/*.[0-9]???*[0-9]')
    dirglob.sort()
    #remove charmrun files in case we are looking at a ChaNGa output
    dirglob = [i for i in dirglob if i[-14:-6] != 'charmrun']
    pynload = lambda x: pyn.load(x)
    return itertools.imap(pynload, dirglob.__iter__())

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

def parallel_process(function, directory, poolsize=64, pool=None):
    """
    Take a function with a single argument (a pynbody-loadable snapshot
    filename), and returns a list of that function run on each snapshot in
    directory. Uses the multiprocessing library to load and process the files
    in parallel.  You may want to pass a pool you've already created if you
    want to run many instances and are running into a limited number of
    processes. (this is also a reason you might want to pass a poolsize less
    than 64.
    """
    dirglob = glob.glob(directory+'/*.[0-9]???[0-9]')
    dirglob.sort()
    if pool==None:
        pool = multiprocessing.Pool(processes=poolsize)
    return np.array(pool.map(function, dirglob))
