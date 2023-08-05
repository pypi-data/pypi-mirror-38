import setuptools

setuptools.setup(
        name='seleniumslicer',
        version='0.0.1',
        author='Feng Liu',
        author_email='feng3245@gmail.com',
        description='Given selenium drive and elements. Extract the element screen capture',
        long_description='Given a driver and an element on the page save the element to the file name of your chosing',
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",]
        )
