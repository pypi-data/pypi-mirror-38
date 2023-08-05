# -*- coding: utf-8 -*-
from plone.app.uuid.utils import uuidToURL
from zope.interface import implementer
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound


@implementer(IPublishTraverse)
class RedirectToUUIDView(BrowserView):
    """A browser view that will cause a redirect to a given UUID,
    given via sub-path traversal.
    """

    uuid = None

    def publishTraverse(self, request, name):
        self.uuid = name
        return self

    def __call__(self):
        if self.uuid is None:
            raise KeyError(
                'No UUID given in sub-path. Use .../@@redirect-to-uuid/<uuid>'
            )

        url = uuidToURL(self.uuid)
        if url is None:
            raise NotFound(self, self.uuid)

        self.request.response.redirect(url)
        return u''
