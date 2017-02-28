# -*- coding: utf-8 -*-
from .interfaces import IRemoteProxySchema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import provider


@provider(IFormFieldProvider)
class IRemoteProxyBehavior(model.Schema, IRemoteProxySchema):
    """Behavior Interface for proxy behaviors.
    """
