from setuptools import setup
from src import __version__

setup(
    name="irma-shared",
    version=__version__,
    author="Quarkslab",
    author_email="irma-dev@quarkslab.com",
    description="Schemas and constants of the IRMA software",
    packages=(
        "irma.shared",
        "irma.shared.schemas",
    ),
    package_dir={
        "irma.shared": "src",
    },
    namespace_packages=(
        "irma",
    ),
    install_requires=(
        # FIXME: this version includes a bug that make it unusable. Upgrade
        # to next version as soon as it is available.
        # 'marshmallow==3.0.0b20',
        'marshmallow@https://github.com/marshmallow-code/marshmallow/tarball/dev',
    ),
    test_suite='nose.collector',
    tests_require=(
        'nose',
        'coverage',
    )
)
