from setuptools import setup, find_packages

setup(
    name="devlabs_recommender_system",
    version="0.1",
    description="A recommendation system for DevLabs.",
    author="Muhammad Rieza Fachrezi",
    author_email="riezaf51@gmail.com",
    packages=find_packages(),
    install_requires=[
        'flask',
        'pandas',
        'scikit-learn',
        'numpy',
        'python-dotenv',
        'waitress',
    ],
    entry_points={
        'console_scripts': [
            'start-server=devlabs_recommender_system.run:main',
        ],
    },
)
