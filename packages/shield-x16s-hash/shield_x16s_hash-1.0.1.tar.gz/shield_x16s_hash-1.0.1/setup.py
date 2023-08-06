from distutils.core import setup, Extension

x16s_hash_module = Extension('shield_x16s_hash',
                               sources = ['x16s_module.c',
                                          'x16s.c',
                                          'sha3/blake.c',
                                          'sha3/bmw.c',
                                          'sha3/groestl.c',
                                          'sha3/jh.c',
                                          'sha3/keccak.c',
                                          'sha3/skein.c',
                                          'sha3/cubehash.c',
                                          'sha3/echo.c',
                                          'sha3/luffa.c',
                                          'sha3/simd.c',
                                          'sha3/hamsi.c',
                                          'sha3/hamsi_helper.c',
                                          'sha3/fugue.c',
                                          'sha3/shavite.c',
                                          'sha3/shabal.c',
                                          'sha3/whirlpool.c',
                                          'sha3/sha2big.c'],
                            include_dirs=['.', './sha3'])

with open("README.md", "r") as fh:
    long_description = fh.read()

setup (name = 'shield_x16s_hash',
       version = '1.0.1',
       author = "kimkkikki",
       author_email = "kimkkikki1@gmail.com",
       description = 'Bindings for the proof of work used by X16S for SHIELD (XSH)',
       long_description=long_description,
       long_description_content_type="text/markdown",
       ext_modules = [x16s_hash_module])
