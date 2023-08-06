# raise ValueError('Please configure setup.py first.')
PACKAGE_NAME='pep440nz'
PACKAGE_AUTHOR='Clement'

if __name__=='__main__':
    import setuptools,sys,os.path
    if os.path.exists('version.py'):
        import version
        vstring = version.vstring
    else:
        from importlib import import_module
        version = import_module('{}.__version__'.format(PACKAGE_NAME))
        vstring = version.VERSION
    if len(sys.argv) < 2:
        dist = 'dist'
        wheel = '-'.join([
            PACKAGE_NAME.replace('-','_'),
            vstring,
            'py3','none','any']) + '.whl'
        print(os.path.join(dist,wheel))
        sdist = '-'.join([
            PACKAGE_NAME,
            vstring]) + '.tar.gz'
        print(os.path.join(dist,sdist))
    else:
        with open('README.rst','r') as f:
            long_description = f.read()
        setuptools.setup(
            name=PACKAGE_NAME,
            version=vstring,
            author=PACKAGE_AUTHOR,
            author_email='neze+pypi@melix.org',
            description='',
            long_description=long_description,
            long_description_content_type='text/x-rst',
            url='',
            packages=setuptools.find_packages(),
            classifiers=[
                "Programming Language :: Python :: 3",
            ],
            entry_points={
                'console_scripts': [],
            },
            install_requires=[],
        )
