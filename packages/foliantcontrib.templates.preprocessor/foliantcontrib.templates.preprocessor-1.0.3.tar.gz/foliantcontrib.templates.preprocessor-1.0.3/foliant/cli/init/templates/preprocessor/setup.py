from setuptools import setup


SHORT_DESCRIPTION = 'Short description.'

try:
    with open('README.md', encoding='utf8') as readme:
        LONG_DESCRIPTION = readme.read()

except FileNotFoundError:
    LONG_DESCRIPTION = SHORT_DESCRIPTION


setup(
    name='foliantcontrib.$slug',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    version='1.0.0',
    author='Your Name',
    author_email='your@email.com',
    url='https://example.com',
    packages=['foliant.preprocessors'],
    license='MIT',
    platforms='any',
    install_requires=[
        'foliant>=1.0.8'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Utilities",
    ]
)
