
import logging, os, shutil, subprocess

log = logging.getLogger(__name__)


class Magick:
    def __init__(self, cmd=None):
        """
        for ImageMagick (default), the cmd is None, because it installs its subcommands as main.
        for GraphicsMagick, the cmd='gm' (or whatever the installed location of the gm command).
        """
        self.cmd = cmd

    def __call__(self, subcommand, filename, quiet=True, **params):
        args = []
        if self.cmd is not None:
            args += [self.cmd]
        args += [subcommand]
        if quiet == True and 'gm' not in (self.cmd or ''):  # GraphicsMagick doesn't support -quiet
            args += ['-quiet']
        for key in params.keys():
            args += ['-' + key]
            if str(params[key]) not in ["", None]:
                args += [str(params[key])]
        args += [filename]
        log.debug("%r" % args)
        return subprocess.check_output(args).decode('utf8')

    def mogrify(self, filename, **params):
        return self.__call__('mogrify', filename, **params)

    def identify(self, filename, **params):
        return self.__call__('identify', filename, **params)

    def convert(self, filename, outfilename=None, **params):
        """rather than using the 'convert' command, copy the file and use 'mogrify' (reliability)"""
        if outfilename is not None and os.path.normpath(outfilename) != os.path.normpath(filename):
            if not os.path.exists(os.path.dirname(outfilename)):
                os.makedirs(os.path.dirname(outfilename))
            shutil.copy(filename, outfilename)
        else:
            outfilename = filename
        return self.mogrify(outfilename, **params)
