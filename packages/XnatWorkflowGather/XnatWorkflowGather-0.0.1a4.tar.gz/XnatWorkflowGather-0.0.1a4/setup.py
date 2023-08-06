from setuptools import setup

setup(
    name='XnatWorkflowGather',
    version='0.0.1a4',
    description='Tool for gathering workflow data from xnat postgres db and posting metrics to datadog using local '
                'statsd',
    packages=['XnatWorkflowGather'],
    scripts=['scripts/xnat-workflow-gather'],
    author='Brian Holt',
    author_email='brian@radiologics.com',
    license='BSD 3-Clause License',
    keywords='xnat',
    python_requires='>=2.6',
    classifiers=[
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2',
    ],
    url='https://bitbucket.org/beholt-radiologics/radiologics-workflow-metric-gatherer',
    install_requires=[
        "psycopg2-binary",
        "ConfigArgParse>=0.13.0",
        "ConfigParser",
        "datadog"
    ]
)
