# -*- coding: utf-8 -*-
#
#   oauthkit-google: OAuthKit for Google
#   Copyright (C) 2015-2018 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from jsonable_objects.proxy import proxy
from jsonable_objects.proxy import Field
from zope.interface import implementer

from .interfaces import IGoogleClientSecret
from .interfaces import IGoogleTokenResponse


@implementer(IGoogleClientSecret)
@proxy(dict)
class GoogleClientSecret(object):

    client_id = Field(type=str)
    client_secret = Field(type=str)
    auth_uri = Field(type=str)
    token_uri = Field(type=str)
    redirect_uris = Field(type=list)
    client_email = Field(type=str, optional=True)
    auth_provider_x509_cert_url = Field(type=str, optional=True)
    client_x509_cert_url = Field(type=str, optional=True)


@implementer(IGoogleTokenResponse)
@proxy(dict)
class GoogleTokenResponse(object):

    access_token = Field(type=str)
    expires_in = Field(type=int)
    token_type = Field(type=str)
    refresh_token = Field(type=str, optional=True)
