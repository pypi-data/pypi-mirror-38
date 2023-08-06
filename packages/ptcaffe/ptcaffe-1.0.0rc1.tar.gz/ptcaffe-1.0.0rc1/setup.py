from setuptools import setup, find_packages 

NAME = "ptcaffe"
PACKAGES = find_packages()
setup(
    name = NAME,
    version = "1.0.0.rc1",
    description = 'pytorch caffe',
    long_description = 'the caffe framework which works on pytorch',
    license = "MIT Licence", 
    url = "http://github.com/orion/ptcaffe",
    author = "xiaohang",
    author_email = "xiaohang@ainirobot.com",
    packages = PACKAGES,
    #include_package_data = True,
    platforms = "any", 

    install_requires=[
        'easydict',
        'nose',      # for test 
        'packaging', # for version compare
        'torch>=0.4.0',
        'torchvision>=0.2.1',
        'opencv-python',
	'protobuf',
        'tqdm',
        'setuptools>=16.0',
    ],
    scripts = [],
    entry_points={'console_scripts': [
        'ptcaffe     = ptcaffe.tools.main:main',
    ]},
    test_suite='test'
)

