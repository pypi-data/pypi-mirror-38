'''

Copyright (C) 2017-2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

__version__ = "0.0.10"
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsochat@stanford.edu'
NAME = 'repofish'
PACKAGE_URL = "http://www.github.com/vsoch/repofish"
KEYWORDS = 'search repositories for functions and generate data structures for them'
DESCRIPTION = "Command line tool for working with container storage"
LICENSE = "LICENSE"

################################################################################
# Global requirements

INSTALL_REQUIRES = (
    ('pandas', {'min_version': '0.22.0'}),
    ('textblob', {'min_version': '0.15.1'}),
    ('nltk', {'min_version': '3.2.5'}),
)

################################################################################
# Submodule Requirements

INSTALL_WIKIPEDIA = (
    ('wikipedia', {'min_version': '1.4.0'}),
)

INSTALL_GITHUB = (
    ('gitpython', {'min_version': '2.1.11'}),
)

#INSTALL_ZENODO = (
#    ('beautifulsoup4', {'min_version': '4.6.0'}),
#)

INSTALL_PUBMED = (
    ('biopython', {'min_version': '1.72'}),
)


INSTALL_ALL = (INSTALL_WIKIPEDIA +
               INSTALL_GITHUB +
               #INSTALL_ZENODO +
               INSTALL_PUBMED)

# Add the base

INSTALL_WIKIPEDIA = INSTALL_REQUIRES + (
    ('wikipedia', {'min_version': '1.4.0'}),
)

INSTALL_GITHUB = INSTALL_REQUIRES + (
    ('gitpython', {'min_version': '2.1.11'}),
)

#INSTALL_ZENODO = INSTALL_REQUIRES + (
#    ('beautifulsoup4', {'min_version': '4.6.0'}),
#)

INSTALL_PUBMED = INSTALL_REQUIRES + (
    ('biopython', {'min_version': '1.72'}),
)

