from setuptools import setup

setup(
    name='mantle',
    version='0.1',
    description='Library of hardware primitives for programming FPGAs',
    packages=[
        "mantle",
        "mantle.common",
        "mantle.coreir",
        "mantle.lattice",
        "mantle.lattice.mantle40",
        "mantle.lattice.ice40",
        "mantle.verilog",
        "mantle.primitives",
        "mantle.util",
        "mantle.util.lfsr",
        "mantle.util.sort",
        "mantle.util.compressor",
        "mantle.util.lhca",
    ],

    install_requires=[
        "six",
        "fault>=0.20, <=0.28",
    ],
    url='https://github.com/phanrahan/mantle',
    maintainer='Leonard Truong',
    maintainer_email='lenny@cs.stanford.edu',
    python_requires='>=3.6'
)
