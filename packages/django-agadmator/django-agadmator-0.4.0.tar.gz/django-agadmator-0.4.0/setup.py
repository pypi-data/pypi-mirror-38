from setuptools import setup, find_packages

setup(
    name="django-agadmator",
    author='Jaco du Plessis',
    author_email='jaco@jacoduplessis.co.za',
    version="0.4.0",
    packages=find_packages(),
    package_data={
        'agadmator': [
            'templates/agadmator/*.html',
            'static/agadmator/*',
            'static/agadmator/chessground/*',
            'static/agadmator/chessground/images/board/*',
            'static/agadmator/chessground/images/pieces/merida/*',
        ]
    },
    install_requires=[
        'django',
        'requests',
        'lxml',
        'cssselect',
        'feedparser',
        'python-chess',
    ]
)
