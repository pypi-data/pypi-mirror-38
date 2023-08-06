from distutils.core import setup

if __name__== '__main__':
    setup(include_package_data=True,
          description='util functions written by Av',
          long_description="""Util functions written by Av Shrikumar""",
          url='https://github.com/kundajelab/avutils',
          version='0.2.2.0',
          packages=['avutils', 'avutils.yaml_data_import'],
          setup_requires=[],
          install_requires=[],
          scripts=["scripts/make_hdf5", "scripts/shuffle_corresponding_lines"],
          name='avutils')
