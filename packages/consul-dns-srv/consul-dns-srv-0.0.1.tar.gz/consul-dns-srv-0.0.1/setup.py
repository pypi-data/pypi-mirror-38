from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='consul-dns-srv',
      description='Consul DNS SRV Helper',
      long_description=long_description,
      long_description_content_type="text/markdown",
      version='0.0.1',
      url='https://github.com/hampsterx/consul-dns-srv',
      author='Tim van der Hulst',
      author_email='tim.vdh@gmail.com',
      license='Apache2',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2'
      ],
      packages=['consul_dns_srv'],
      install_requires=[
            'srvlookup==2.0.0',
      ]
)