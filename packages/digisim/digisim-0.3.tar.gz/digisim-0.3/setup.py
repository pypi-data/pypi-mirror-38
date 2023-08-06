from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'digisim',         # How you named your package folder (MyLib)
  packages = ['digisim'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Digital simulation library!',   # Give a short description about your library
  author = 'Kaif Khan,Pulak Sahoo,Tushar,Gaurav Singh',                   # Type in your name
  author_email = 'kaifkhan.khan0@gmail.com',      # Type in your E-Mail
  url = 'https://khanstark.github.io/DigiSim/',   # Provide either the link to your github or to your website
    # I explain this later on
  keywords = ['digital','electronics','logic gates','flip flops','test case','quine-mccluskey','minimization','voltage','boolean algebra','universal gates','sequential circuits','JK','Toggle','Delay'],   # Keywords that define your package best
  
  long_description=long_description,
long_description_content_type="text/markdown",
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
         #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 2'
  ],
)
