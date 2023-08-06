Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer. 

Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

Neither the name of Paul Scherrer Institut nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description-Content-Type: UNKNOWN
Description: Brightway2 parameters
        =====================
        
        |Coverage Status| |Build status| |Documentation Status|
        
        Library for storing, validating, and calculating with parameters.
        Designed to work with the `Brightway2 life cycle assessment
        framework <https://brightwaylca.org>`__, but is generic enough to work
        in other use cases.
        
        ::
        
            In [1]: from bw2parameters import ParameterSet
        
            In [2]: parameters = {
               ...:        'Deep_Thought': {'amount': 42},
               ...:        'East_River_Creature': {'formula': '2 * Deep_Thought + 16'},
               ...:        'Elders_of_Krikkit': {'formula': 'sqrt(East_River_Creature)'},
               ...: }
        
            In [3]: ParameterSet(parameters).evaluate()
            Out[3]: {'Deep_Thought': 42, 'East_River_Creature': 100, 'Elders_of_Krikkit': 10.0}
        
        Compatible with Python 2.7, 3.3, and 3.4. 100% test coverage. `Source
        code on
        bitbucket <https://bitbucket.org/cmutel/brightway2-parameters>`__,
        documentation on `Read the
        Docs <https://brightway2-parameters.readthedocs.io/>`__.
        
        .. |Coverage Status| image:: https://coveralls.io/repos/bitbucket/cmutel/brightway2-parameters/badge.svg?branch=master
           :target: https://coveralls.io/bitbucket/cmutel/brightway2-parameters?branch=master
        .. |Build status| image:: https://ci.appveyor.com/api/projects/status/9ynu6gd9nk26mx2i?svg=true
           :target: https://ci.appveyor.com/project/cmutel/brightway2-parameters
        .. |Documentation Status| image:: https://readthedocs.org/projects/brightway2-parameters/badge/?version=latest
           :target: http://brightway2-parameters.readthedocs.io/?badge=latest
        
Platform: UNKNOWN
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: BSD License
Classifier: Operating System :: MacOS :: MacOS X
Classifier: Operating System :: Microsoft :: Windows
Classifier: Operating System :: POSIX
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: 3.6
