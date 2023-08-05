from setuptools import setup, find_packages

# with open('demo_project_test_time/requirements.txt') as f:
#     required = f.read().splitlines()

setup(
    name="demo_project2",
    version="1.001",
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

