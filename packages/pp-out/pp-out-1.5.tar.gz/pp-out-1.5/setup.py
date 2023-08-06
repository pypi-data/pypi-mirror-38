from setuptools import setup, find_packages

with open("README.md") as f:
    file = f.read()

setup(
    name='pp-out',
    version='1.5',
    packages=find_packages(),
    author="Chang Hao",
    author_email="mixpplus@gmail.com",
    description=("视频运维平台适用于不同规模的视频监控系统的日常运维管理"),
    long_description = file,
    long_description_content_type = "text/markdown",
    keywords = ("demo", "out", "test"),
    entry_points={
            'console_scripts':
                [
                    'run = pp_out.command_line:main',
                    'go = pp_out.command_line:go',
                ],
        },
    zip_safe=False,
)