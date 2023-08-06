from setuptools import setup, Extension

def readme():
    with open('README.md') as f:
        return f.read()

x16r_hash_module = Extension('x16r_hash',
sources = ['x16r_module.c',
  'x16r.c',
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

setup (name = 'x16r_hash',
  version = '1.0.1',
  description = 'Bindings for proof of work used by X16R',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url = 'https://github.com/brian112358/x16r_hash',
  keywords = 'ravencoin, rvn',
  author = 'Brian Lee',
  author_email = 'brian112358@gmail.com',
  license = 'MIT',
  maintainer = 'Ravencoin community',
  ext_modules = [x16r_hash_module])
