import ctypes
CMPH_BMZ, CMPH_BMZ8, CMPH_CHM, CMPH_BRZ, CMPH_FCH, CMPH_BDZ, CMPH_BDZ_PH, CMPH_CHD_PH, CMPH_CHD, CMPH_COUNT = range(10)
libcmph = ctypes.cdll.LoadLibrary('libcmph.so')
libc = ctypes.cdll.LoadLibrary('libc.so.6')
libc.fopen.restype = ctypes.c_void_p

class CMPHashFile(object):
    '''
    hf = CMPHashFile(filename)

    hf.search(key)

    hf.close()
    '''
    def __init__(self, filename):
        '''
        hf = CMPHashFile(filename)

        Opens file `filename`, which must be a CMPH hash file.
        '''
        self.cmph_hash = None
        hashfile = libc.fopen(filename, 'rb')
        if hashfile is None:
            raise IOError("could not open %s" % filename)
        self.cmph_hash = libcmph.cmph_load(hashfile)
        libc.fclose(hashfile)

    def __del__(self):
        self.close()

    def close(self):
        '''
        hf.close()

        Closes the hash file.
        '''
        if self.cmph_hash is not None:
            libcmph.cmph_destroy(self.cmph_hash)
            self.cmph_hash = None

    def search(self, query):
        '''
        key = hf.search(query)

        Returns the numeric value for the `query`.
        '''
        assert self.cmph_hash is not None, \
            'cmph.CMPHashFile.search: cmph_hash is None.\n\nDid you previously close the file?'
        return libcmph.cmph_search(self.cmph_hash, query, len(query))

