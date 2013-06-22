#!/usr/bin/env python

import argparse
import ConfigParser
import subprocess
import os
import sys
import os.path
from subprocess import PIPE
import logging
import datetime


class MorningPaper:
    """Kindle morning paper

    Fetch rss feeds with the help of calibre recipes
    and send the genrated mobi file to a kindle email
    """

    def __init__(self, args):
        """Initializes the MorningPaper object

        creates a python logger and reads all values
        from the config into class attributes.

        Args:
            args: command line arguments.
                Must at least contain config and verbose attributes
        """

        self.config = ConfigParser.SafeConfigParser()

        # init logging
        frm = logging.Formatter("%(asctime)s %(levelname)s: %(message)s",
                                "%d.%m.%Y %H:%M:%S")
        shandler = logging.StreamHandler()
        shandler.setFormatter(frm)
        self.log = logging.getLogger("MorningPaper")
        self.log.addHandler(shandler)
        if args.verbose:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)

        # init config
        if len(self.config.read(args.config)) is 0:
            self.log.error("config file does not exist: " + args.config)
            sys.exit(1)

        self.log.debug("Initializing MorningPaper with config " + args.config)
        self.tempDownloadDir = self.config.get('calibre', 'tempDownloadDir')
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d:%H:%M:%S")

        # mail config
        self.mailhost = self.config.get('mailserver', 'host')
        self.mailuser = self.config.get('mailserver', 'username')
        self.mailpwd = self.config.get('mailserver', 'password')
        self.mailport = self.config.get('mailserver', 'port')
        kindlemails = self.config.get('kindle', 'mail')
        self.kindlemails = kindlemails.split(", ")

        # init paths for calibre
        self.calibredir = self.config.get('calibre', 'path')
        self.ebook_convert = os.path.join(self.calibredir, 'ebook-convert')
        self.calibre_smtp = os.path.join(self.calibredir, 'calibre-smtp')
        self.recipe = self.config.get('calibre', 'recipe')
        mobifname = "morningPaper_" + self.timestamp + ".mobi"
        self.mobifile = os.path.join(self.tempDownloadDir, mobifname)

    def download_feeds(self):
        """ Get rss feeds and convert them to mobi

        Uses calibres ebook-convert to download and convert
        rss feeds specified by a calibre recipe.
        """

        self.log.info("Downloading RSS feeds")
        calibre_rss_download_cmd = [self.ebook_convert, self.recipe,
                                    self.mobifile]
        self.log.debug(calibre_rss_download_cmd)
        process = subprocess.Popen(calibre_rss_download_cmd,
                                   stdout=PIPE, stderr=PIPE)
        pstream = process.communicate()
        self.log.debug(pstream)
        if process.returncode:
            self.log.error("Couldn't download RSS feeds")
            sys.exit(1)
        else:
            self.log.info("Finished downloading RSS feeds")

    def send_to_kindle(self):
        """Send the created mobi file to the specified email addresses.

        Uses calibre-smtp to send the downloaded and converted rss feeds
        to a (kindle) email address.
        """

        self.log.info("Sending papers")
        for kindle in self.kindlemails:
            self.log.debug("Sending papter to: " + kindle)
            calibre_send_cmd = [self.calibre_smtp, '-r', self.mailhost, '-p',
                                self.mailpwd, '-e', 'TLS', '-u', self.mailuser,
                                '--port', self.mailport, '-a', self.mobifile,
                                self.mailuser, kindle, ""]
            self.log.debug(calibre_send_cmd)
            process = subprocess.Popen(calibre_send_cmd,
                                       stdout=PIPE, stderr=PIPE)
            pstream = process.communicate()
            self.log.debug(pstream)
            if process.returncode:
                self.log.error("Error sending the paper to " + kindle)
            else:
                self.log.debug("Morning paper to " + kindle +
                               " successfully sent")
        self.log.info("Morning papers sent")
        if self.config.getboolean('calibre', 'keepMobiFile') is False:
            self._remove_mobi()

    def _remove_mobi(self):
        """Remove the mobi file from the temporary directory

        Gets only called if keepMobiFile config value is false
        """

        os.remove(self.mobifile)
        self.log.debug("Removed mobifile: " + self.mobifile)


def main(argv):
    """main function"""

    # Build the command line options
    parser = argparse.ArgumentParser(description="Kindle Morning Paper")
    parser.add_argument('-c', '--config', default='kindleMorningPaper.cfg',
                        required=False)
    parser.add_argument('--verbose', '-v', action='count')
    args = parser.parse_args()

    mpaper = MorningPaper(args)
    mpaper.download_feeds()
    mpaper.send_to_kindle()

if __name__ == "__main__":
    argv = None
    main(argv)
