
from codecs import open

from setuptools import setup




REQUIREMENTS = [
    'webob>=1.2.0',
    'six>=1.10.0'
]

EXTRA_REQUIREMENTS = {
    'jinja2>=2.4',
    'Babel>=2.2',
    'pytz>=2015.7'
}

setup(
    name='amanwa31',
    version='1.0.3',
    license='Apache Software License',
    description="testing wa3 custom",
    long_description='LONG_DESCRIPTION',
    author='a',
    author_email='angrish_aman@yahoo.com',
    zip_safe=False,
    platforms='any',
    py_modules=[
        'amanwa31',
    ],
    packages=[
        'amanwa31',
        'amanwa31.webapp3_extras',
        'amanwa31.webapp3_extras.appengine',
        'amanwa31.webapp3_extras.appengine.auth',
    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extras_require={'extras': EXTRA_REQUIREMENTS},
    classifiers=[
       
    ]
)
