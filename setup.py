from setuptools import setup, find_packages

setup(name = "app-init-auth",
   version = "1.0.0",
   description = "Authentication for webplatform",
   author = "Matthew Owens",
   author_email = "mowens@redhat.com",
   url = "https://github.com/app-init/auth",
   packages = find_packages(),
   include_package_data = True,
   install_requires = [
      "app-init-cli",
      "app-init-backend",
      'xmlsec',
      'python3-saml @ https://github.com/app-init/python3-saml/tarball/master#egg=python3_saml-1.2.2'
   ],
   # dependency_links = [
   #    'http://github.com/app-init/python3-saml/tarball/master#egg=python3_saml-1.2.2',
   # ],
   python_requires='>=3',
   license='MIT',
   long_description = """TODO""",
   classifiers = [
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   zip_safe = False
)
