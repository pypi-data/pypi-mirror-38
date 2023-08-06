1. Generate and upload the data file
  - Create data tar file
      - Go to [pandeia_data](https://github.com/STScI-SSB/pandeia_data), and click on the "Releases" link. Look for the latest release and download the source code (in tar.gz format).
  - Go to the folder you had downloaded the tar file located.
  - Make a directory named `/eng/ssb/websites/ssbpublic/pandeia/engine/X.Y.Z` where X.Y.Z is the name of the release.
  - Move the tar file just downloaded into that directory.
      
  
2. Follow instruction [here](http://peterdowns.com/posts/first-time-with-pypi.html) to generate and upload the source code to the https://pypi.python.org/pypi/pandeia.engine
  - In section 'Create a .pypirc configuration file' if the .pypirc file does not exist.
  - In a fresh checkout of pandeia vX.Y.Z
    - `cd engine/`
    - Generate source distribution and upload to pypi: `python setup.py sdist upload -r pypi`
    
3. Test 
 - Go to https://pypi.python.org/pypi/pandeia.engine to see if the package is sucessfully uploaded.
 - Install a fresh version of the latest third party software and load that environment by typing `source /path/to/third/party pandeia_<third_party_version>`.
 - `pip freeze | grep pandeia.engine` (note the version, e.g. 1.2.1dev0)
 - `pip install pandeia.engine --upgrade`
 - test it by running the `pip freeze | grep pandeia.engine` command again and note the version should have changed (e.g. v1.2.2)
 - Follow the usage instruction in [pypi](https://pypi.python.org/pypi/pandeia.engine) to check if the users can follow the instruction as well.
 - Ask the engine dev to do a simple test and see if the new changes apply.
 
 4. Email the person who is responsible for updating the jwst website
 - Notify Both Swara and Klaus that the engine is on pypi and the [jwst docs](https://jwst.stsci.edu/science-planning/proposal-planning-toolbox/exposure-time-calculator-etc) need to be updated.
 
