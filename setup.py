import os
import sys
from setuptools import setup
from setuptools import find_packages

about = {}
for package in find_packages():
    version_file = os.path.join(package, '__version__.py')
    if os.path.exists(version_file):
        with open(version_file, mode='rt') as f:
            exec(f.read(), about)
            break

setup(
    name="baseball-cli",
    version=about['__version__'],
    license="MIT",
    description="プロ野球の試合結果、順位表、個人成績をコマンドラインで確認できます。",
    author="ssato",
    url="https://github.com/buenaV1sta/baseball-cli",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "click>=7.1.2",
        "scrapy>=2.1.0",
    ] + (["colorama==0.3.3"] if "win" in sys.platform else []),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    entry_points={
        'console_scripts': [
            'npb = baseball.main:main'
        ],
    }
)
