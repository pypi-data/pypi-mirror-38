from distutils.core import setup

setup(
    name          = 'linearCounter',
    packages      = ['linearCounter'], # this must be the same as the name above
    version       = '0.51',
    description   = 'A trivial extension to collections.Counter that enables linear operations.',
    long_description = 'This is a sparse infinitely dimensional vector, indexed by whatever you want. OK, not infinite in as much as the entries can take no more than the RAM you have. So do have some spare RAM, and you will be rewarded.',
    author        = 'Mateusz Lacki',
    author_email  = 'matteo.lacki@gmail.com',
    url           = 'https://github.com/MatteoLacki/linearCounter',
    download_url  = 'https://github.com/MatteoLacki/linearCounter.git',
    keywords      = ['linear operations', 'abstract linear spaces', 'Counter'],
    classifiers   = [],
)
