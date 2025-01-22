from setuptools import setup, find_packages

setup(
    name="IN450M6",
    version="1.0",
    license="GNU Free Documentation License",
    description="Postgresql database GUI for IN450M6 final project",
    author_email="mrholocker@gmail.com",
    packages=find_packages(),  # This will automatically include all packages and modules
    include_package_data=True,
    install_requires=[
        "psycopg2",
    ],

    entry_points={
        'console_scripts': [
            'IN450M6 = IN450M6.main'
        ],
    },
)