import glob
import json
import os
import shlex
import subprocess
import sys

import click
import yaml
import platform

__version__ = '1.0.2'


# Takes command, options, source and destination folders and creates a command from it
# Escapes the src/dst and removes any additional whitespace
def _buildCommand(command, options, sourceFilename, destFilename):
    """Build PyQt5 command line string based on the command, options and arguments

    String follows the syntax:
        <command> <options> -o destFilename sourceFilename
    """

    # Construct command string
    commandString = '%s %s -o %s %s' % (
        shlex.quote(command), options, shlex.quote(destFilename), shlex.quote(sourceFilename))

    # Split command string by spaces
    args = shlex.split(commandString)

    # Remove any blank arguments meaning there were double spaces in the command string and then rejoin the args
    return ' '.join([arg for arg in args if arg])


def _isOutdated(src, dst, isQRCFile):
    outdated = (not os.path.exists(dst) or
                (os.path.getmtime(src) > os.path.getmtime(dst)))

    if not outdated and isQRCFile:
        # For qrc files, we need to check each individual resources.
        # If one of them is newer than the dst file, the qrc file must be considered as outdated.
        # File paths are relative to the qrc file path
        qrcParentDir = os.path.dirname(src)

        with open(src, 'r') as f:
            lines = f.readlines()
            lines = [line for line in lines if '<file>' in line]

        cwd = os.getcwd()
        os.chdir(qrcParentDir)

        for line in lines:
            filename = line.replace('<file>', '').replace('</file>', '').strip()
            filename = os.path.abspath(filename)

            if os.path.getmtime(filename) > os.path.getmtime(dst):
                outdated = True
                break

        os.chdir(cwd)

    return outdated


@click.command(name='pyqt5ac')
@click.option('--rcc', 'rccPath', default='pyrcc5', envvar='PYQT5AC_RCC',
              type=click.Path(exists=False, file_okay=True, dir_okay=False),
              help='Path to resource compiler [default: pyrcc5]')
@click.option('--rcc_options', 'rccOptions', default='',
              help='Additional options to pass to resource compiler [default: none]')
@click.option('--uic', 'uicPath', default='pyuic5', envvar='PYQT5AC_UIC',
              type=click.Path(exists=False, file_okay=True, dir_okay=False),
              help='Path to UI compiler [default: pyuic5]')
@click.option('--uic_options', 'uicOptions', default='',
              help='Additional options to pass to UI compiler [default: none]')
@click.option('--config', '-c', default='', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='JSON or YAML file containing the configuration parameters')
@click.option('--force', default=False, is_flag=True, help='Compile all files regardless of last modification time')
@click.argument('iopaths', nargs=-1, required=False)
@click.version_option(__version__)
def cli(rccPath, rccOptions, uicPath, uicOptions, force, config, iopaths=()):
    """Compile PyQt5 UI/QRC files into Python

    IOPATHS argument is a space delineated pair of glob expressions that specify the source files to compile as the
    first item in the pair and the path of the output compiled file for the second item. Multiple pairs of source and
    destination paths are allowed in IOPAIRS.

    \b
    The destination path argument supports variables that are replaced based on the
    target source file:
        * %%FILENAME%% - Filename of the source file without the extension
        * %%EXT%% - Extension excluding the period of the file (e.g. ui or qrc)
        * %%DIRNAME%% - Directory of the source file

    Files that match a given source path expression are compiled if and only if the file has been modified since the
    last compilation unless the FORCE flag is set. If the destination file does not exist, then the file is compiled.

    A JSON or YAML configuration file path can be specified using the config option. See the GitHub page for example
    config files.

    \b
    Example:
    gui
    --->example.ui
    resources
    --->test.qrc

    \b
    Command:
    pyqt5ac gui/*.ui generated/%%FILENAME%%_ui.py resources/*.qrc generated/%%FILENAME%%_rc.py

    \b
    Results in:
    generated
    --->example_ui.py
    --->test_rc.py

    Author: Addison Elliott
    """

    # iopaths is a 1D list containing pairs of the source and destination file expressions
    # So the list goes something like this:
    # [sourceFileExpr1, destFileExpr1, sourceFileExpr2, destFileExpr2, sourceFileExpr3, destFileExpr3]
    #
    # When calling the main function, it requires that ioPaths be a 2D list with 1st column source file expression and
    # second column the destination file expression.
    ioPaths = list(zip(iopaths[::2], iopaths[1::2]))

    main(rccPath, rccOptions, uicPath, uicOptions, force, config, ioPaths)


def main(rccPath='pyrcc5', rccOptions='', uicPath='pyuic5', uicOptions='', force=False, config='', ioPaths=()):
    if config:
        with open(config, 'r') as fh:
            if config.endswith('.yml'):
                # Load YAML file
                configData = yaml.load(fh)
            else:
                # Assume JSON file
                configData = json.load(fh)

            # configData variable is a dictionary where the keys are the names of the configuration
            # Load the keys and use the default value if nothing is specified
            rccPath = configData.get('rcc', rccPath)
            rccOptions = configData.get('rcc_options', rccOptions)
            uicPath = configData.get('uic', uicPath)
            uicOptions = configData.get('uic_options', uicOptions)
            force = configData.get('force', force)
            ioPaths = configData.get('ioPaths', ioPaths)

    # Loop through the list of io paths
    for sourceFileExpr, destFileExpr in ioPaths:
        foundItem = False

        # Find files that match the source filename expression given
        for sourceFilename in glob.glob(sourceFileExpr, recursive=True):
            # If the filename does not exist, not sure why this would ever occur, but show a warning
            if not os.path.exists(sourceFilename):
                click.secho('Skipping target %s, file not found' % sourceFilename, fg='yellow')
                continue

            foundItem = True

            # Split the source filename into directory and basename
            # Then split the basename into filename and extension
            #
            # Ex: C:/Users/addis/Documents/PythonProjects/PATS/gui/mainWindow.ui
            #   dirname = C:/Users/addis/Documents/PythonProjects/PATS/gui
            #   basename = mainWindow.ui
            #   filename = mainWindow
            #   ext = .ui
            dirname, basename = os.path.split(sourceFilename)
            filename, ext = os.path.splitext(basename)

            # Replace instances of the variables with the actual values from the source filename
            destFilename = destFileExpr.replace('%%FILENAME%%', filename) \
                .replace('%%EXT%%', ext[1:]) \
                .replace('%%DIRNAME%%', dirname)

            # Retrieve the absolute path to the source and destination filename
            sourceFilename, destFilename = os.path.abspath(sourceFilename), os.path.abspath(destFilename)

            if ext == '.ui':
                isQRCFile = False
                command = uicPath
                options = uicOptions
            elif ext == '.qrc':
                isQRCFile = True
                command = rccPath
                options = rccOptions
            else:
                click.secho('Unknown target %s found' % sourceFilename, fg='yellow')
                continue

            # Create all directories to the destination filename and do nothing if they already exist
            os.makedirs(os.path.dirname(destFilename), exist_ok=True)

            # If we are force compiling everything or the source file is outdated, then compile, otherwise skip!
            if force or _isOutdated(sourceFilename, destFilename, isQRCFile):
                # Builds command string to be run in terminal
                commandString = _buildCommand(command, options, sourceFilename, destFilename)

                # Let's try to run the command now!
                try:
                    # On Windows, shell must be set to True to search through the PATH environment variable when
                    # searching for a program. See here:
                    # https://stackoverflow.com/questions/3022013/windows-cant-find-the-file-on-subprocess-call
                    subprocess.check_call(commandString, shell=(platform.system() == 'Windows'))
                except subprocess.CalledProcessError as e:
                    if e.output:
                        click.secho(commandString, fg='yellow')
                        click.secho(e.output.decode(sys.stdout.encoding), fg='red')
                    else:
                        click.secho(commandString, fg='red')
                except OSError as e:
                    click.secho(commandString, fg='yellow')
                    click.secho(str(e), fg='red')
                else:
                    click.secho(commandString, fg='green')
            else:
                click.secho('Skipping %s, up to date' % filename)

        if not foundItem:
            click.secho('No items found in %s' % sourceFileExpr)

if __name__ == '__main__':
    cli()
