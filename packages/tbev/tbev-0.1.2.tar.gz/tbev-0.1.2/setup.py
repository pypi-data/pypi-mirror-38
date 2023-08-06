import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tbev",
    version="0.1.2",
    author="Tushar Pawar",
    author_email="gmail@tusharpawar.com",
    description="Embedding Visualizer Using Tensorboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Backalla/tbev",
    packages=setuptools.find_packages(),
    install_requires=[
        'colorama',
        'docopt'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'tbev = tbev.visualize:main',
        ],
    },
    package_data={
        "tbev": ['demo_word2vec_embeddings_zen.pkl','invalid.png','not_found.png']
    }
)