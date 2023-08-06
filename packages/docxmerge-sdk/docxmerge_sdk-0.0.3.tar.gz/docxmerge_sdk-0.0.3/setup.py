import setuptools

setuptools.setup(
    name="docxmerge_sdk",
    version="0.0.3",
    author="David viejo pomata",
    author_email="davidviejopomata@gmail.com",
    description="Sdk for docxmerge",
    url="https://github.com/Docxmerge/docxmerge-sdk",
    # packages=setuptools.find_packages("./docxmerge"),
    packages=['docxmerge_sdk', 'docxmerge_sdk.swagger_client', 'docxmerge_sdk.swagger_client.api',
              'docxmerge_sdk.swagger_client.models'],
    package_dir={
        'docxmerge_sdk': 'docxmerge_sdk',
        'docxmerge_sdk/swagger_client': 'docxmerge_sdk.swagger_client',
        'docxmerge_sdk/swagger_client/api': 'docxmerge_sdk.swagger_client.api',
        'docxmerge_sdk/swagger_client/models': 'docxmerge_sdk.swagger_client.models',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
