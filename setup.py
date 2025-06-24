from setuptools import setup, find_packages

setup(
    name="QuanCryptor",
    version="4.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"client": ["*.html", "css/*.css", "css/*/*.css", "js/*.js"]},
    install_requires=[
        "cryptography==44.0.2",
        "platformdirs==4.3.8",
        "setuptools==80.8.0",
        "termcolor==3.1.0",
        "requests==2.32.3",
        "pywebview==5.4",
        "flask==3.1.1",
    ],
    entry_points={
        "console_scripts": [
            "client=client.main:main",
            "server=server.main:main",
        ],
    },
)
