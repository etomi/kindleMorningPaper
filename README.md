kindleMorningPaper
==================

KindleMorningPaper (KMP) delivers your rss feeds to your kindle.

The original idea was to have something like a newspaper every morning automatically deliverd to your kindle.

Install
=======

Requirements:

* Python 2.7
* calibre (http://calibre-ebook.com/)

KMP only needs the calibre commandline tools 'ebook-convert' and 'calibre-smtp'. There is no need for the graphical user interface of calibre.

Configuration
=============

KMP is configured with a small config file (default: kindleMorningPaper.cfg).  
The settings within this file should be self explaining.  

Kindle
------
Within the *kindle* section you can specify which email address should recive the KMP.  
You can specify more than one recipient by adding email addresses seperated by commas to *mail*.  

Calibre
-------
Within the *calibre* section the path to your calibre installation is specified.  
Also a temporary directory for the generated mobi file can be specified here.  
The setting *keepMobiFile* determines if the generated mobi file should be kept or deleted from the temporary directory after it was sent to your kindle.  
Another important setting is the *recipe*. This value determines which calibre recipe is used for downloading the rss feeds. Furhter information regarding recipes can be found on the calibre website.  

Mailserver
----------
The *mailserver* section is where you specify the configuration for you smtp mailserver, which will deliver the KMP.  

**IMPORTANT:** The email address you specify in the *mailserver* section must be authorized to send emails to your kindle's email address.  
This can onyl be done on the amazon website.  

Usage
=====

For help type: <code>kindleMorningPaper.py -h</code>

If you want your feeds delivered automatically, use a cronjob for executing KMP.
