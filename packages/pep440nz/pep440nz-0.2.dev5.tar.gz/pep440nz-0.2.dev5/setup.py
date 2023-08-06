# raise ValueError('Please configure setup.py first.')
PACKAGE_NAME='pep440nz'
PACKAGE_AUTHOR='Clement'

if __name__=='__main__':
    import setuptools,sys,os.path
    try:
        from sphinx.setup_command import BuildDoc
        cmdclass = { 'doc': BuildDoc, 'cov': BuildDoc }
    except ImportError:
        cmdclass = {}
    if os.path.exists('version.py'):
        import version
        vstring = version.vstring
        rstring = version.rstring
    else:
        from importlib import import_module
        version = import_module('{}.__version__'.format(PACKAGE_NAME))
        vstring = version.VERSION
        rstring = vstring
    doc_opt = {
        'project': ('setup.py',PACKAGE_NAME),
        'version': ('setup.py',vstring),
        'release': ('setup.py',vstring),
        'source_dir': ('setup.py','docs'),
    }
    cov_opt = dict(doc_opt)
    cov_opt.update({
        'builder': ('setup.py','coverage'),
    })
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
            cmdclass=cmdclass,
            command_options={
                'doc': doc_opt,
                'cov': cov_opt,
            }
        )
