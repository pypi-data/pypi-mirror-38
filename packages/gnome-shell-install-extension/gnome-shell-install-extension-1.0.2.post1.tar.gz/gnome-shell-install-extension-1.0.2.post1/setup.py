from setuptools import setup

with open('README.adoc') as f:
    long_description = f.read()

setup(
    name='gnome-shell-install-extension',
    version='1.0.2.post1',
    description="Install Gnome Shell extension from zip files.",
    long_description=long_description,
    url='https://github.com/zakora/gnome-shell-install-extension',
    author='zakora',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Gnome',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Desktop Environment :: Gnome',
    ],
    python_requires='~=3.5',
    package_dir={'': 'src'},
    packages=['gnome_shell_install_extension'],
    entry_points={
        'console_scripts': ['gnome-shell-install-extension=gnome_shell_install_extension:main']
    },
)
