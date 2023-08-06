patch_issue
===========

.. image:: https://travis-ci.org/yakobu/patch-issue.svg?branch=master
    :target: https://travis-ci.org/yakobu/patch-issue
.. image:: https://coveralls.io/repos/github/yakobu/patch-issue/badge.svg?branch=master
    :target: https://coveralls.io/github/yakobu/patch-issue?branch=master
.. image:: https://badge.fury.io/py/patch-issue.svg
    :target: https://badge.fury.io/py/patch-issue
.. image:: https://img.shields.io/packagist/l/doctrine/orm.svg
    :alt: Packagist
    :target: https://github.com/yakobu/patch-issue



Patch manager for easy tracking with integration in jira.

Concept
-------

We've all put patches over patches in our code, for various reasons:

* Hot fixing a currently released version
* Temporary place-holder
* Or just because we felt like it - so we wouldn't have to design some 
  complex structure.

This is where ``patch-issue`` comes into play.
We wanted to have a way of notifying the programmer that the current code segment
is a part of a patch - using Jira issue tracking system and some kind of a logger.
Then, later on, ``patch-issue`` will notify the programmer (in runtime) that
the issue is closed and the programmer can remove the patch easily.

Important Note
++++++++++++++

We do not encourge the usage of patches in a code segment.  
This tool main purpose is to help programmers track their patches,  
so they won't forget the patch in their code (long term wise).  

How to install?
---------------

Simply run:

.. code-block:: console

    $ pip install patch-issue

And try to import:  

.. code-block:: python

    import patch_issue



Ok, So how do I start?
----------------------

First, you need to make a connection to Jira in your code,  
and just for that there is an awesome library called -   
yeah you guessed right - ``jira`` - [jira pypi link](https://pypi.org/project/jira/).

Here is how to make a simple connection:  
``connection.py``

.. code-block:: python

    from jira import JIRA
    jira_connection = JIRA(server="http://jira/", basic_auth=("username", "password"))

Now you can make a new patch class (``patches.py``):

.. code-block:: python

    import logging

    from patch_issue import JiraPatchIssue

    from connection import jira_connection  # from previously made connection


    class FixDBConnection(JiraPatchIssue):
       ISSUE_KEY = "APP-1"  # a must have class attribute
       DESCRIPTION = "Fixes db connection using a mocked password."
       WAY_TO_SOLVE = "Configure the right password."

    fix_connection = FixDBConnection(jira=jira_connection,
        logger=logging)  # there is also a default logger


Now you can use your patch freely in your code:

.. code-block:: python

    import .config
    from .db import DB

    from patches import fix_connection  # import your patch instance

    ##################################################################
    
    @fix_connection.patch_function  # use patch as a function decorator
    def new_connection():
        return DB.make_connection("user", "password")
    
    new_connection()
    
    ##################################################################
    
    usename = "someuser"
    password = config.get_password()
    
    with fix_connection.patch:  # use patch as a context manager
       password = "1234"
    
    db = DB.make_connection(username, password)

Now, when your code reaches to the patches,  
a message will be logged in your logger!  
You will never miss your patches again!  
