from setuptools import setup

setup(
    name='google_cloud_logging_handler',
    version='1.1',
    descrition='Logs directly to google cloud',
    license='MIT',
    author='Alex Chaplianka',
    url="https://github.com/aclowkey",
    author_email='alexettelis@gmail.com',
    download_url='https://github.com/aclowkey/google-cloud-logging-handler/archive/v1.1.tar.gz',
    keywords=['google-cloud','logging'],
    packages=['google_cloud_logging_handler'],
    install_requires=['google-cloud-logging']
)
