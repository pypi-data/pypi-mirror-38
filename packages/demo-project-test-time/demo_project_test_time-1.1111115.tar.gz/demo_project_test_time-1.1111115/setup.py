from setuptools import setup, find_packages
setup(
    name="demo_project_test_time",
    version="1.1111115",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["numpy",
                      "pandas",
                      "tornado",
                      "redis",
                      "sqlalchemy",
                      "kazoo",
                      "pika",
                      "ruamel_yaml",
                      "requests"
                      ]
)
