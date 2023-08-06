from setuptools import setup, find_packages

setup(
    name='pp-out',
    version='1.3',
    packages=find_packages(),
    author="Chang Hao",
    author_email="mixpplus@gmail.com",
    description=("This is a tools by changhao maked"),
    entry_points={
            'console_scripts':
                [
                    'run = pp_out.command_line:main',
                    'go = pp_out.command_line:go',
                ],
        },
    zip_safe=False,
)