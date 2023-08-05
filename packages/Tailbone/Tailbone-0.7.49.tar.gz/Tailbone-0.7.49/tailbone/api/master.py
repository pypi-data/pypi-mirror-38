# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2018 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Tailbone Web API - Master View
"""

from __future__ import unicode_literals, absolute_import

from paginate_sqlalchemy import SqlalchemyOrmPage

from tailbone.api import APIView, api
from tailbone.db import Session


class APIMasterView(APIView):
    """
    Base class for data model REST API views.
    """

    @property
    def Session(self):
        return Session

    @classmethod
    def get_model_class(cls):
        if hasattr(cls, 'model_class'):
            return cls.model_class
        raise NotImplementedError("must set `model_class` for {}".format(cls.__name__))

    @classmethod
    def get_normalized_model_name(cls):
        if hasattr(cls, 'normalized_model_name'):
            return cls.normalized_model_name
        return cls.get_model_class().__name__.lower()

    @classmethod
    def get_object_key(cls):
        if hasattr(cls, 'object_key'):
            return cls.object_key
        return cls.get_normalized_model_name()

    @classmethod
    def get_collection_key(cls):
        if hasattr(cls, 'collection_key'):
            return cls.collection_key
        return '{}s'.format(cls.get_object_key())

    def _collection_get(self):
        cls = self.get_model_class()
        objects = self.Session.query(cls)

        sort = self.request.params.get('sort')
        if sort:
            # TODO: this is fragile, but what to do if bad params?
            sortkey, sortdir = sort.split('|')
            sortkey = getattr(cls, sortkey)
            objects = objects.order_by(getattr(sortkey, sortdir)())

            # NOTE: we only page results if sorting is in effect, otherwise
            # record sequence is "non-determinant" (is that the word?)
            page = self.request.params.get('page')
            per_page = self.request.params.get('per_page')
            if page.isdigit() and per_page.isdigit():
                page = int(page)
                per_page = int(per_page)
                objects = SqlalchemyOrmPage(objects, items_per_page=per_page, page=page)

        objects = [self.normalize(obj) for obj in objects]
        return {self.get_collection_key(): objects}

    def _get(self):
        uuid = self.request.matchdict['uuid']
        obj = self.Session.query(self.get_model_class()).get(uuid)
        if not obj:
            raise self.notfound()
        return {self.get_object_key(): self.normalize(obj)}
