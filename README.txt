Introduction
============

Allow to view content of archive files into plone.

How it works
============

Add an File with zipped content, this will be marked with 'collective.archiveviewer.interfaces.IArchiveFile'.

Now you can access the content trough web by appending '@@contents/$filename' to the path of your file.

For instance, if you have a file 'foo.html' inside the archive you can view it by going to 'http://yourplone.com/yourzipfile/@@contents/foo.html'.

Supported archives
==================

- *.zip (application/zip)

Compatibility
==============

Tested on Plone 3.3.6

Authors
=======

Simone Orsi <simone.orsi@domsense.com> [simahawk]
Silvio Tomatis <silviot@gmail.com> [silviot]

Credits
=======

Developed with the support of `International Traning Center of the ILO`__.

.. image:: http://www.itcilo.org/logo_en.jpg
   :alt: ITCILO - Logo
   :target: http://www.itcilo.org/

__ http://www.itcilo.org/


This product was developed by Domsense in collaboration with Silvio Tomatis.

.. image:: http://domsense.com/logo-txt.png
   :alt: Domsense Website
   :target: http://www.domsense.com/
