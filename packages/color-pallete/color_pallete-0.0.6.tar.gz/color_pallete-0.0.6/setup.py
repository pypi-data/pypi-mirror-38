from setuptools import setup

setup(

    name="color_pallete",
    version='0.0.6',
    url='https://github.com/pytholabsbot1/k-means',
    author='Pytholabs',
    author_email='info@pytholabs.com',  
    description='Outputs the color pallete of the provided image..',
    py_modules=['color_pallete'],
    package_dir={'':'src'},

    install_requires=[
          'sklearn',
          'opencv-python',
          'numpy',
          'matplotlib',
          'Image'
      ],

    )
