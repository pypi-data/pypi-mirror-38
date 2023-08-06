# tools

import subprocess
import pprint
import os
import sys
import time

DEBUGGING = True

UNKNOWN = 0
DISPLAY = 1
CAPTURE = 2
IGNORE  = 3
APPEND  = 4
APPEND_TO_FILE = 4
OVERWRITE = 5
OVERWRITE_FILE = 5

pp = pprint.PrettyPrinter(indent=4)

def run_stdout_display_stderr_display(cmd):
    pass

def run_stdout_display_stderr_capture(cmd):
    pass

def run_stdout_capture_stderr_display(cmd):
    pass

# result = Engine('ls -l', Engine.CAPTURE, Engine.CAPTURE).run()
def run_stdout_capture_stderr_capture(cmd):

    return_code = -1
    stderr = ""
    try:
        PIPE = subprocess.PIPE
        # note: with shell=False, need to resolve binary to explicit path
        # delegating to the shell lets it locate it in PATH
        proc = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()

        # Wait until process terminates (without using p.wait())
        while proc.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.5)

        # Get return code from process
        return_code = proc.returncode
        if DEBUGGING:
            print "return code: {}".format(str(return_code))
            print "stderr =>"
            pp.pprint(stderr)

    except Exception, e:
        print "exception: {}".format(str(e))
        if DEBUGGING:
            sys.exit(1)

    return { 'code': return_code, 'stdout': stdout, 'stderr': stderr }

def run_stdout_display_stderr_append(cmd, stderr_filepath):
    pass

def run_stdout_append_stderr_display(cmd, stdout_filepath):
    pass

def run_stdout_append_stderr_append(cmd, stdout_filepath, stderr_filepath):
    pass

def run_stdout_display_stderr_overwrite(cmd, stderr_filepath):
    pass

def run_stdout_overwrite_stderr_display(cmd, stdout_filepath):
    pass

# result = Engine('ls -l', Engine.OVERWRITE_FILE, Engine.OVERWRITE_FILE, stdout_filepath='/tmp/cmd.stdout', stderr_filepath='/tmp/cmd.stderr').run()
def run_stdout_overwrite_stderr_overwrite(cmd, stdout_filepath, stderr_filepath):

    return_code = -1
    try:
        # note: with shell=False, need to resolve binary to explicit path
        # delegating to the shell lets it locate it in PATH
        with open(stdout_filepath, 'w') as outfile, open(stderr_filepath, 'w') as errfile:
            proc = subprocess.Popen(cmd, shell=True, stdout=outfile, stderr=errfile)

        # Wait until process terminates (without using p.wait())
        while proc.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.5)

        # Get return code from process
        return_code = proc.returncode
        if DEBUGGING:
            print "return code: {}".format(str(return_code))

    except Exception, e:
        print "exception: {}".format(str(e))
        if DEBUGGING:
            sys.exit(1)

    return { 'code': return_code }

def run_stdout_capture_stderr_append(cmd, stderr_filepath):
    pass

def run_stdout_append_stderr_capture(cmd, stdout_filepath):
    pass

def run_stdout_capture_stderr_overwrite(cmd, stderr_filepath):
    pass

# result = Engine('ls -l', Engine.OVERWRITE_FILE, Engine.CAPTURE, stdout_filepath='/tmp/cmd.stdout').run()
def run_stdout_overwrite_stderr_capture(cmd, stdout_filepath):

    return_code = -1
    stderr = ""
    try:
        PIPE = subprocess.PIPE
        # note: with shell=False, need to resolve binary to explicit path
        # delegating to the shell lets it locate it in PATH
        proc = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        with open(stdout_filepath, 'w') as stdout:
            stdout, stderr = proc.communicate()

        # Wait until process terminates (without using p.wait())
        while proc.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.5)

        # Get return code from process
        return_code = proc.returncode
        if DEBUGGING:
            print "return code: {}".format(str(return_code))
            print "stderr =>"
            pp.pprint(stderr)

    except Exception, e:
        print "exception: {}".format(str(e))
        if DEBUGGING:
            sys.exit(1)

    return { 'code': return_code, 'stderr': stderr }


# result = Engine('ls -l', Engine.DISPLAY, Engine.IGNORE).run()
def run_stdout_display_stderr_ignore(cmd):

    return_code = -1
    stderr = ""
    try:
        PIPE = subprocess.PIPE
        # note: with shell=False, need to resolve binary to explicit path
        # delegating to the shell lets it locate it in PATH
        proc = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()

        # Wait until process terminates (without using p.wait())
        while proc.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.5)

        # Get return code from process
        return_code = proc.returncode
        if DEBUGGING:
            print "return code: {}".format(str(return_code))
            print "stderr =>"
            pp.pprint(stderr)

        print stdout

    except Exception, e:
        print "exception: {}".format(str(e))
        if DEBUGGING:
            sys.exit(1)

    return { 'code': return_code }


def run_stdout_ignore_stderr_display(cmd):
    pass


# result = Engine('ls -l', Engine.IGNORE, Engine.IGNORE).run()
def run_stdout_ignore_stderr_ignore(cmd):

    return_code = -1
    try:
        PIPE = subprocess.PIPE
        # note: with shell=False, need to resolve binary to explicit path
        # delegating to the shell lets it locate it in PATH
        proc = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        with open(os.devnull, 'w') as devnull:
            devnull, devnull = proc.communicate()

        # Wait until process terminates (without using p.wait())
        while proc.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.5)

        # Get return code from process
        return_code = proc.returncode
        if DEBUGGING:
            print "return code: {}".format(str(return_code))
            print "ignoring stderr"

    except Exception, e:
        print "exception: {}".format(str(e))
        if DEBUGGING:
            sys.exit(1)

    return { 'code': return_code }

def run_stdout_capture_stderr_ignore(cmd):
    pass

def run_stdout_ignore_stderr_capture(cmd):
    pass

def run_stdout_append_stderr_ignore(cmd, stdout_filepath):
    pass

def run_stdout_ignore_stderr_append(cmd, stderr_filepath):
    pass

# result = Engine('ls -l', Engine.OVERWRITE, Engine.IGNORE, stdout_filepath=/tmp/cmd.stdout).run()
def run_stdout_overwrite_stderr_ignore(cmd, stdout_filepath):

    return_code = -1
    try:
        # note: with shell=False, need to resolve binary to explicit path
        # delegating to the shell lets it locate it in PATH
        #with open(stdout_filepath, 'w') as outfile, open(stderr_filepath, 'w') as errfile:
        with open(stdout_filepath, 'w') as outfile, open(os.devnull, 'w') as devnull:
            proc = subprocess.Popen(cmd, shell=True, stdout=outfile, stderr=devnull)
            #outfile, devnull = proc.communicate()

        # Wait until process terminates (without using p.wait())
        while proc.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.5)

        # Get return code from process
        return_code = proc.returncode
        if DEBUGGING:
            print "return code: {}".format(str(return_code))

    except Exception, e:
        print "exception: {}".format(str(e))
        if DEBUGGING:
            sys.exit(1)

    return { 'code': return_code }


def run_stdout_ignore_stderr_overwrite(cmd, stderr_filepath):
    pass


class Engine(object):
    """
    A simple and powerful python API for running external commands.

    Create an Engine object like this.

    e = Engine(cmd, stdout_control, stderr_control)

    or

    e = Engine(cmd, stdout_control, stderr_control, stdout_filepath=FILEPATH)

    or

    e = Engine(cmd, stdout_control, stderr_control, stderr_filepath=FILEPATH)

    or

    e = Engine(cmd, stdout_control, stderr_control, stdout_filepath=FILEPATH, stderr_filepath=FILEPATH)

    where stdout_control and stderr_control are one of these:

    DISPLAY
    CAPTURE
    IGNORE
    APPEND_TO_FILE
    OVERWRITE_FILE

    Run the command in the desired manner like this:

    e.run()

    In every case, the result is a dictionary that contains a 'code' property,
    the value of which is the command's return code.

    If CAPTURE is specified, the result dictionary contains a FILE
    property, where FILE is either 'stdout' or 'stderr'.
    """

    UNKNOWN = 0
    DISPLAY = 1
    CAPTURE = 2
    IGNORE  = 3
    APPEND  = 4
    APPEND_TO_FILE = 4
    OVERWRITE = 5
    OVERWRITE_FILE = 5

    def __init__(self, cmd, stdout_control, stderr_control, **kwargs):

        self.cmd = cmd
        self.stdout_control = stdout_control
        self.stderr_control = stderr_control

        self.stdout_filepath = None
        self.stderr_filepath = None
        if 'stdout_filepath' in kwargs:
            self.stdout_filepath = kwargs['stdout_filepath']

        if 'stderr_filepath' in kwargs:
            self.stderr_filepath = kwargs['stderr_filepath']


    def __repr__(self):

        s = '\n'
        for k in self.__dict__:
                s += "%5s%20s: %s\n" % (' ',k, self.__dict__[k])

        return s

    def run(self):

        if self.stdout_control == DISPLAY and self.stderr_control == DISPLAY:
            return run_stdout_display_stderr_display(self.cmd)

        if self.stdout_control == DISPLAY and self.stderr_control == CAPTURE:
            return run_stdout_display_stderr_capture(self.cmd)

        if self.stdout_control == CAPTURE and self.stderr_control == DISPLAY:
            return run_stdout_capture_stderr_display(self.cmd)

        if self.stdout_control == CAPTURE and self.stderr_control == CAPTURE:
            return run_stdout_capture_stderr_capture(self.cmd)

        # display, append
        if self.stdout_control == DISPLAY and self.stderr_control == APPEND_TO_FILE:
            return run_stdout_display_stderr_append(self.cmd, self.stderr_filepath)

        if self.stdout_control == APPEND_TO_FILE and self.stderr_control == DISPLAY:
            return run_stdout_append_stderr_display(self.cmd, self.stdout_filepath)

        if self.stderr_control == APPEND_TO_FILE and self.stderr_control == APPEND_TO_FILE:
            return run_stdout_append_stderr_append(self.cmd, self.stdout_filepath, self.stderr_filepath)

        # display, overwrite
        if self.stdout_control == DISPLAY and self.stderr_control == OVERWRITE_FILE:
            return run_stdout_display_stderr_overwrite(self.cmd, self.stderr_filepath)

        if self.stdout_control == OVERWRITE_FILE and self.stderr_control == DISPLAY:
            return run_stdout_overwrite_stderr_display(self.cmd, self.stdout_filepath)

        if self.stdout_control == OVERWRITE_FILE and self.stderr_control == OVERWRITE_FILE:
            return run_stdout_overwrite_stderr_overwrite(self.cmd, self.stdout_filepath, self.stderr_filepath)

        # capture, append
        if self.stdout_control == CAPTURE and self.stderr_control == APPEND_TO_FILE:
            return run_stdout_capture_stderr_append(self.cmd, self.stderr_filepath)

        if self.stdout_control == APPEND_TO_FILE and self.stderr_control == CAPTURE:
            return run_stdout_append_stderr_capture(self.cmd, self.stdout_filepath)

        # capture, overwrite
        if self.stdout_control == CAPTURE and self.stderr_control == OVERWRITE_FILE:
            return run_stdout_capture_stderr_overwrite(self.cmd, self.stderr_filepath)

        if self.stdout_control == OVERWRITE_FILE and self.stderr_control == CAPTURE:
            return run_stdout_overwrite_stderr_capture(self.cmd, self.stdout_filepath)

        # display, ignore
        if self.stdout_control == DISPLAY and self.stderr_control == IGNORE:
            return run_stdout_display_stderr_ignore(self.cmd)

        if self.stdout_control == IGNORE and self.stderr_control == DISPLAY:
            return run_stdout_ignore_stderr_display(self.cmd)

        if self.stdout_control == IGNORE and self.stderr_control == IGNORE:
            return run_stdout_ignore_stderr_ignore(self.cmd)

        # capture, ignore
        if self.stdout_control == CAPTURE and self.stderr_control == IGNORE:
            return run_stdout_capture_stderr_ignore(self.cmd)

        if self.stdout_control == IGNORE and self.stderr_control == CAPTURE:
            return run_stdout_ignore_stderr_capture(self.cmd)

        # append, ignore
        if self.stdout_control == APPEND_TO_FILE and self.stderr_control == IGNORE:
            return run_stdout_append_stderr_ignore(self.cmd, self.stdout_filepath)

        if self.stdout_control == IGNORE and self.stderr_control == APPEND_TO_FILE:
            return run_stdout_ignore_stderr_append(self.cmd, self.stderr_filepath)

        # overwrite, ignore
        if self.stdout_control == OVERWRITE_FILE and self.stderr_control == IGNORE:
            return run_stdout_overwrite_stderr_ignore(self.cmd, self.stdout_filepath)

        if self.stdout_control == IGNORE and self.stderr_control == OVERWRITE_FILE:
            return run_stdout_ignore_stderr_overwrite(self.cmd, self.stderr_filepath)


if __name__ == '__main__':

    print
    print "capture/capture ->"

    result = Engine(
        'ls -l', 
        Engine.CAPTURE, 
        Engine.CAPTURE).run()

    pp.pprint(result)
    print 

    print "overwrite/overwrite ->"

    result = Engine(
        '/usr/local/bin/stderrout.sh', 
        Engine.OVERWRITE_FILE, 
        Engine.OVERWRITE_FILE, 
        stdout_filepath='/tmp/cmd.stdout', 
        stderr_filepath='/tmp/cmd.stderr').run()

    print "cmd stdout ->"
    os.system('cat /tmp/cmd.stdout')
    print "cmd stderr ->"
    os.system('cat /tmp/cmd.stderr')
    pp.pprint(result)
    print

    print "overwrite/capture ->"

    result = Engine(
        'ls -l', 
        Engine.OVERWRITE_FILE, 
        Engine.CAPTURE, 
        stdout_filepath='/tmp/cmd.stdout').run()

    print "cmd stdout ->"
    os.system('cat /tmp/cmd.stdout')
    pp.pprint(result)
    print

    print "display/ignore ->"

    result = Engine(
        'ls -l', 
        Engine.DISPLAY, 
        Engine.IGNORE).run()

    pp.pprint(result)
    print

    print "ignore/ignore ->"

    result = Engine(
        'ls -l', 
        Engine.IGNORE, 
        Engine.IGNORE).run()

    print

    print "overwrite/ignore ->"

    result = Engine(
        'ls -l', 
        Engine.OVERWRITE, 
        Engine.IGNORE, 
        stdout_filepath='/tmp/cmd.stdout').run()

    print "cmd stdout ->"
    os.system('cat /tmp/cmd.stdout')
    pp.pprint(result)
    print
