name = "pretty_errors"

import sys, re, colorama, os, time

colorama.init()


FILENAME_COMPACT  = 0
FILENAME_EXTENDED = 1
FILENAME_FULL     = 2

location_expression = re.compile(r'.*File "([^"]*)", line ([0-9]+), in (.*)')


class PrettyErrors():
    def __init__(self):
        self._line_length         = 79
        self._filename_display    = FILENAME_COMPACT
        self._full_line_newline   = False
        self._display_timestamp   = False
        self._seperator_character = '-'
        self._seperator_color     = '\033[01;30m'
        self._timestamp_color     = '\033[01;30m'
        self._default_color       = '\033[02;37m'
        self._filename_color      = '\033[01;36m'
        self._line_number_color   = '\033[01;32m'
        self._function_color      = '\033[01;34m'


    def configure(self, line_length = None, filename_display = None, full_line_newline = None, display_timestamp = None,
                  seperator_character = None, seperator_color = None, default_color = None, timestamp_color = None,
                  filename_color = None, line_number_color = None, function_color = None):
        """Used to configure settings governing how exceptions are displayed."""
        if line_length         is not None: self._line_length         = line_length
        if filename_display    is not None: self._filename_display    = filename_display
        if full_line_newline   is not None: self._full_line_newline   = full_line_newline
        if display_timestamp   is not None: self._display_timestamp   = display_timestamp
        if seperator_character is not None: self._seperator_character = seperator_character
        if seperator_color     is not None: self._seperator_color     = seperator_color
        if default_color       is not None: self._default_color       = default_color
        if timestamp_color     is not None: self._timestamp_color     = timestamp_color
        if filename_color      is not None: self._filename_color      = filename_color
        if line_number_color   is not None: self._line_number_color   = line_number_color
        if function_color      is not None: self._function_color      = function_color


    def write(self, *args):
        """Replaces sys.stderr.write, outputing pretty errors."""
        for arg in args:
            for line in arg.split('\n'):
                if self.is_header(line):
                    self.write_header()
                else:
                    line = line.replace('\\', '/')
                    location = self.get_location(line)
                    if location:
                        path, line_number, function = location
                        self.write_location(path, line_number, function)
                    else:
                        self.write_body(line)


    def write_header(self):
        """Writes a header at the start of a traceback"""
        if self._display_timestamp:
            timestamp = str(time.perf_counter())
            seperator = (self._line_length - len(timestamp)) * self._seperator_character + timestamp
        else:
            seperator = self._line_length * self._seperator_character
        self.output_text('\n')
        self.output_text(self._seperator_color + seperator, wants_newline = True)


    def write_location(self, path, line_number, function):
        """Writes location of exception: file, line number and function"""
        line_number += " "
        wants_newline = False
        if self._filename_display == FILENAME_FULL:
            filename = path
            wants_newline = True
        elif self._filename_display == FILENAME_EXTENDED:
            filename = path[-(self._line_length - len(line_number) - len(function) - 4):]
            if filename != path: filename = '...' + filename
            filename += " "
        else:
            filename = os.path.basename(path) + " "
        self.output_text('\n')
        self.output_text(self._filename_color    + filename, wants_newline = wants_newline)
        self.output_text(self._line_number_color + line_number)
        self.output_text(self._function_color    + function, wants_newline = True)


    def write_body(self, body):
        """Writes any text other than location identifier or traceback header."""
        self.output_text(self._default_color)
        body = body.strip()
        while len(body) > self._line_length:
            c = self._line_length - 1
            while c > 0 and body[c] not in (" ", "\t"):
                c -= 1
            if c == 0: c = self._line_length
            self.output_text(body[:c], wants_newline = True)
            body = body[c:].strip()
        if body:
            self.output_text(body, wants_newline = True)


    def output_text(self, text, wants_newline = False):
        """Helper function to output text while trying to only insert 1 newline when outputing a line of maximum length."""
        sys.pretty_errors_stderr.write(text)
        if wants_newline and (len(text) < self._line_length or self._full_line_newline):
            sys.pretty_errors_stderr.write('\n')


    def get_location(self, text):
        """Helper function to extract location of exception.  If it returns None then text was not a location identifier."""
        location = location_expression.match(text)
        if location:
            return (location.group(1), location.group(2), location.group(3))
        else:
            return None


    def is_header(self, text):
        """Returns True if text is a traceback header."""
        return text.startswith('Traceback')


if not getattr(sys, 'pretty_errors_stderr', False):
    sys.pretty_errors_stderr = sys.stderr
    sys.stderr = PrettyErrors()


def configure(line_length = None, filename_display = None, full_line_newline = None, display_timestamp = None,
              seperator_character = None, seperator_color = None, default_color = None, timestamp_color = None,
              filename_color = None, line_number_color = None, function_color = None):
    """Used to configure settings governing how exceptions are displayed."""
    sys.stderr.configure(line_length, filename_display, full_line_newline, display_timestamp, seperator_character,
                         seperator_color, default_color, timestamp_color, filename_color, line_number_color, function_color)
