from setuptools import setup

setup(
    name         = 'powerline-vcsh',
    description  = 'A Powerline segment for showing the current VCSH repo',
    version      = '0.0.1',
    keywords     = 'powerline vcsh prompt',
    license      = 'MIT',
    author       = 'Anthony DeChiaro',
    author_email = 'taintedkernel@gmail.com',
    url          = 'https://github.com/taintedkernel/powerline-vcsh',
    packages     = ['powerline_vcsh'],
    install_requires = ['powerline-status'],
    classifiers  = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Terminals'
    ]
)
