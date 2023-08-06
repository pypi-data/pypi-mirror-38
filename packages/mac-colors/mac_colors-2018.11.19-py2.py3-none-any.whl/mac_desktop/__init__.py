#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import applescript
from public import public


def _frontmost():
    return applescript.tell.app("System Events", "name of (first process whose frontmost is true)").out


@public
def show():
    """show Desktop (hide apps windows)"""
    hide()
    time.sleep(0.2)
    applescript.tell.app("System Events", "key code 103")


@public
def hide():
    """hide Desktop (show apps windows)"""
    frontmost = _frontmost()
    applescript.tell.app("Dock", "activate")
    applescript.tell.app(frontmost, "activate")
