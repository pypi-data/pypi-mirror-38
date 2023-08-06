from setuptools import setup

setup(
    name='xonsh-docker-tabcomplete',
    version='0.1.5',
    license='MIT',
    url='https://github.com/xsteadfastx/xonsh-docker-tabcomplete',
    description='docker tabcomplete support for the Xonsh shell',
    author='Marvin Steadfast',
    author_email='marvin@xsteadfastx.org',
    packages=['xontrib', 'docker_tabcomplete'],
    package_dir={'xontrib': 'xontrib'},
    package_data={'xontrib': ['*.xsh']},
    install_requires=['docker-py'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ]
)
