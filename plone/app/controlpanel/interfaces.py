# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import controlpanel


class IPloneControlPanelView(controlpanel.IPloneControlPanelView):
    """BBB class
    DONT USE UNLESS YOU RUN INTO BACKWARD COMPATIBILITY PROBLEMS
    """


class IPloneControlPanelForm(controlpanel.IPloneControlPanelForm):
    """BBB class
    DONT USE UNLESS YOU RUN INTO BACKWARD COMPATIBILITY PROBLEMS
    """


class IConfigurationChangedEvent(controlpanel.IConfigurationChangedEvent):
    """BBB class
    DONT USE UNLESS YOU RUN INTO BACKWARD COMPATIBILITY PROBLEMS
    """
