from setuptools import setup, find_packages

with open("readme.md") as f:
    file = f.read()

setup(
    name='pp-new',
    version='1.3',
    packages=find_packages(),
    author="Chang Hao",
    author_email="mixpplus@gmail.com",
    description="视频运维平台适用于不同规模的视频监控系统的日常运维管理",
    long_description=file,
    long_description_content_type="text/markdown",
    keywords=("demo", "new", "test"),
    entry_points={
            'console_scripts':
                [
                    'pp-run = new.line:print_out',
                ],
        },
    zip_safe=False,
)