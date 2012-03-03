# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

archiveviewerMessageFactory = MessageFactory('collective.archiveviewer')

_ = archiveviewerMessageFactory


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
