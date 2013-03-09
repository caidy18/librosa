#!/usr/bin/env python
# CREATED:2013-03-08 15:25:18 by Brian McFee <brm2132@columbia.edu>
#  unit tests for librosa core (__init__.py)
#
# Run me as follows:
#   cd tests/
#   nosetests -v

import librosa
import os, glob
import numpy, scipy.io

from nose.tools import nottest

#-- utilities --#
def files(pattern):
    test_files = glob.glob(pattern)
    test_files.sort()
    return test_files

def load(infile):
    DATA = scipy.io.loadmat(infile, chars_as_strings=True)
    return DATA
#--           --#

#-- Tests     --#
def test_hz_to_mel():
    def __test_to_mel(infile):
        DATA    = load(infile)
        z       = librosa.hz_to_mel(DATA['f'], DATA['htk'])

        assert numpy.allclose(z, DATA['result'])
    
    for infile in files('data/hz_to_mel-*.mat'):
        yield (__test_to_mel, infile)

    pass

def test_mel_to_hz():

    def __test_to_hz(infile):
        DATA    = load(infile)
        z       = librosa.mel_to_hz(DATA['f'], DATA['htk'])

        assert numpy.allclose(z, DATA['result'])
    
    for infile in files('data/mel_to_hz-*.mat'):
        yield (__test_to_hz, infile)

    pass

def test_hz_to_octs():
    def __test_to_octs(infile):
        DATA    = load(infile)
        z       = librosa.hz_to_octs(DATA['f'])

        assert numpy.allclose(z, DATA['result'])

    for infile in files('data/hz_to_octs-*.mat'):
        yield (__test_to_octs, infile)

    pass

def test_load():
    # Note: this does not test resampling.
    # That is a separate unit test.

    def __test(infile):
        DATA    = load(infile)
        (y, sr) = librosa.load(DATA['wavfile'][0], target_sr=None, mono=DATA['mono'])

        # Verify that the sample rate is correct
        assert sr == DATA['sr']

        assert numpy.allclose(y, DATA['y'])

    for infile in files('data/load-*.mat'):
        yield (__test, infile)
    pass

@nottest
def test_resample():

    def __test(infile):
        DATA    = load(infile)
        
        # load the wav file
        (y_in, sr_in) = librosa.load(DATA['wavfile'][0], target_sr=None, mono=True)

        # Resample it to the target rate
        y_out = librosa.resample(y_in, DATA['sr_in'], DATA['sr_out'])

        # Are we the same length?
        if len(y_out) == len(DATA['y_out']):
            # Is the data close?
            assert numpy.allclose(y_out, DATA['y_out'])
        elif len(y_out) == len(DATA['y_out']) - 1:
            assert (numpy.allclose(y_out, DATA['y_out'][:-1,0]) or
                    numpy.allclose(y_out, DATA['y_out'][1:,0]))
        elif len(y_out) == len(DATA['y_out']) + 1:
            assert (numpy.allclose(y_out[1:], DATA['y_out']) or
                    numpy.allclose(y_out[:-2], DATA['y_out']))
        else:
            assert False
        pass


    for infile in files('data/resample-*.mat'):
        yield (__test, infile)
    pass

def test_stft():

    def __test(infile):
        DATA    = load(infile)

        # Load the file
        (y, sr) = librosa.load(DATA['wavfile'][0], target_sr=None, mono=True)

        # Compute the STFT
        D       = librosa.stft(y, sr,   n_fft       =   DATA['nfft'][0].astype(int),
                                        hann_w      =   DATA['hann_w'][0].astype(int),
                                        hop_length  =   DATA['hop_length'][0].astype(int))

        assert  numpy.allclose(D, DATA['D'])   


    for infile in files('data/stft-*.mat'):
        yield (__test, infile)
    pass

def test_istft():
    def __test(infile):
        DATA    = load(infile)

        Dinv    = librosa.istft(DATA['D'],  n_fft       = DATA['nfft'][0].astype(int),
                                            hann_w      = DATA['hann_w'][0].astype(int),
                                            hop_length  = DATA['hop_length'][0].astype(int))
        assert numpy.allclose(Dinv, DATA['Dinv'])

    for infile in files('data/istft-*.mat'):
        yield (__test, infile)
    pass

@nottest
def test_melfb():

    def __test(infile):
        DATA    = load(infile)

        wts = librosa.melfb(    DATA['sr'], 
                                DATA['nfft'], 
                                nfilts  =   DATA['nfilts'],
                                width   =   DATA['width'],
                                fmin    =   DATA['fmin'],
                                fmax    =   DATA['fmax'],
                                use_htk =   DATA['htk'])
                                
        assert numpy.allclose(wts, DATA['wts'])

    for infile in files('data/melfb-*.mat'):
        yield (__test, infile)
    pass