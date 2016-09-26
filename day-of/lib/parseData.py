description = "module that standardizes data I/O"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

### standard packages
import numpy as np
import pickle
import time

#-------------------------------------------------
#               BASIC I/O

def load_data( pklNAME, verbose=False, timing=False ):
    """
    return h, d, kwargs
    """
    verbose = verbose or timing

    ### read in data
    if verbose:
        print "reading : %s"%pklNAME
        if timing:
            t0 = time.time()
    file_obj = open(pklNAME,'r')
    kwargs = pickle.load(file_obj)
    file_obj.close()

    h = kwargs.pop('headers')
    d = kwargs.pop('data')

    ### extract data shape
    ncol = len(h)
    nrow = len(d)
    assert np.shape(d) == (nrow, ncol), "bad data shape!\nnp.shape(h) = %s\nnp.shape(d) = %s"%(str(np.shape(h)), str(np.shape(d)))

    if verbose:
        print "found %d columns"%(ncol)
        print "found %d rows"%(nrow)
        if timing:
            print "    %.6f sec"%(time.time() - t0)

    return h, d, kwargs

def write_data( h, d, pklNAME, verbose=False, timing=False, **kwargs ):
    """
    writes h, d and **kwargs into standard format, saving to pklNAME
    """
    verbose = verbose or timing

    if verbose:
        print "writing : %s"%pklNAME
        if timing:
            t0 = time.time()

    outDATA = {'data':d, 'headers':h}
    outDATA.update( kwargs )

    file_obj = open(pklNAME, 'w')
    pickle.dump( outDATA, file_obj )
    file_obj.close()

    if timing:
        print "    %.6f sec"%(time.time() - t0)

def load_bool( pklNAME, verbose=False, timing=False ):
    """
    return b
    """
    verbose = verbose or timing

    ### read in data
    if verbose:
        print "reading : %s"%pklNAME
        if timing:
            t0 = time.time()
    file_obj = open(pklNAME,'r')
    b = pickle.load(file_obj)
    file_obj.close()

    if timing:
        print "    %.6f sec"%(time.time() - t0)

    return b

def write_model( h, model, pklNAME, verbose=False, timing=False ):
    """
    write model into pickle file
    """
    verbose = verbose or timing

    if verbose:
        print "writing : %s"%pklNAME
        if timing:
            t0 = time.time()

    file_obj = open(pklNAME, 'w')
    pickle.dump( {'headers':h, 'model':model}, file_obj)
    file_obj.close()

    if timing:
        print "    %.6f sec"%(time.time() - t0)

#-------------------------------------------------
#               PRECONDIDTIONING

def excludeCols( h, d, exclude, verbose=False, timing=False ):
    """
    return hsub, dsub
    """
    verbose = verbose or timing

    ### exclude columns
    if verbose:
        print "excluding unwanted columns"
        if timing:
            t0 = time.time()

    bad = np.zeros(len(h), dtype=int)
    for e in exclude:
        bad += h == e
    keep = (1-bad).astype(bool) ### invert and cast

    hsub = h[keep]
    dsub = d[:,keep]

    if verbose:
        print "retained %d columns"%len(hsub)
        if timing:
            print "    %.6f sec"%(time.time() - t0)

    return hsub, dsub  

#-------------------------------------------------
#              map data together

def map_data( hplyr, dplyr, hshot, dshot, verbose=False, timing=False, Verbose=False ):
    """
    associate data from (hply, dplyr) and (hshot, dshot) into a single array
    return h, d 
    """
    verbose = verbose or timing

    nrowPlyr, ncolPlyr = np.shape(dplyr)
    nrowShot, ncolShot = np.shape(dplyr)

    ### booleans for lookup
    truth_PID = hplyr=='PERSON_ID'
    truth_GID = hplyr=='GAME_ID'

    ### generate map from PERSON_ID, CLOSE_DEF_PERSON_ID -> dplyr_ROW
    if verbose:
        print "generating mapping from (PERSON_ID,GAME_ID) -> rowIND"
        if timing:
            t0 = time.time()
    mapping = dict()
    for i, row in enumerate(dplyr):
        pid = round(row[truth_PID][0], 0) ### want element, not array
        gid = round(row[truth_GID][0], 0) ### want element, not array
        mapping[ (pid, gid) ] = i

    if timing:
        print "    %.6f sec"%(time.time() - t0)

    ### map into total data
    if verbose:
        print "generating combined data product"
        if timing:
            t0 = time.time()

    truth_GID = hshot=='GAME_ID'
    truth_SID = hshot=='PERSON_ID'
    truth_DID = hshot=='CLOSE_DEF_PERSON_ID'

    h = np.array( list(hshot) + ["SHOOTER_%s"%_ for _ in hplyr] + ["DEFENDR_%s"%_ for _ in hplyr] )

    missed = 0
    found = 0

    missed_games = set()
    missed_players = set()

    d = []
    for row in dshot:
        gid = round(row[truth_GID][0], 0)
        sid = round(row[truth_SID][0], 0)
        did = round(row[truth_DID][0], 0)

        if not mapping.has_key((sid,gid)):
            if Verbose:
                print "KeyError:\n    (shooter) PERSON_ID\t: %d\n              GAME_ID\t: %d"%(sid, gid)
            missed += 1
            missed_games.add( gid )
            missed_players.add( sid )
            continue

        if not mapping.has_key((did,gid)):
            if Verbose:
                print "KeyError:\n    (defendr) PERSON_ID\t: %d\n              GAME_ID\t: %d"%(did, gid)
            missed += 1
            missed_games.add( gid )
            missed_players.add( did )
            continue

        row = list(row) + list(dplyr[mapping[(sid,gid)]]) + list(dplyr[mapping[(did,gid)]])
        d.append(row)

        found += 1

    if Verbose:
        print "missed : ", missed
        print "found  : ", found

        print "missed_games : ", missed_games
        print "missed_players : ", missed_players

        print "len(missed_gid) : ", len(missed_games)
        print "len(missed_pid) : ", len(missed_players)

    d = np.array(d)
    if timing:
        print "    %.6f sec"%(time.time() - t0)

    ### exclude PERSON_ID, CLOSE_DEF_PERSON_ID, SHOOTER_PERSON_ID, and DEFENDR_PERSON_ID
    exclude = ["GAME_ID", "PERSON_ID", "CLOSE_DEF_PERSON_ID", "SHOOTER_PERSON_ID", "DEFENDR_PERSON_ID"] ### these should NOT be used!
    h, d = excludeCols( h, d, exclude, verbose=verbose, timing=timing )

    return h, d
