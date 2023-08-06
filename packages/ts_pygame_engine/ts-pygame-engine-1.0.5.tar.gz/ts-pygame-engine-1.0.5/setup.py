from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='ts-pygame-engine',
    version='1.0.5',
    description='Simple engine for pygame',
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=[
        'ts_pygame_engine.ui',
        'ts_pygame_engine.ui.core',
        'ts_pygame_engine.ui.containers',
        'ts_pygame_engine.core',
        'ts_pygame_engine.core.events',
        'ts_pygame_engine.primitives',
        'ts_pygame_engine.coordinates'
    ],
    install_requires=[
        'pygame',
    ],
    url='https://gitlab.informatics.ru/TechnoStrife/pygame/',
    license='Mozilla Public License 2.0',
    author='TechnoStrife',
    author_email='plotnikov7rodion@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Education',
        'Topic :: Education',
    ],
)
