#!/usr/bin/env python
import os

colors = {
    'black': '\x1b[30m',
    'red': '\x1b[31m',
    'green': '\x1b[32m',
    'yellow': '\x1b[33m',
    'blue': '\x1b[34m',
    'pink': '\x1b[35m',
    'skyblue': '\x1b[36m',
    'white': '\x1b[37m'
}

def color(selcolor, text):
    color = colors.get(selcolor, None)
    if not color:
        return text
    return color+text+'\x1b[0m'

class base_object(object):
    def __init__(self):
        # Horizonal line character
        self.chr_horizontal = '='
        # Vertical line character
        self.chr_vertical = '|'
        # Separator columns character
        self.chr_separator = '|'
        # General color
        self.color = None
        # Text color
        self.color_text = None
        # Horizonal line color
        self.color_line = None
        # Vertical line color
        self.color_vertical = None
        # Column separator color
        self.color_separator = None

    def set_colors(self, **kwargs):
        # General color
        self.color = kwargs.get('color', self.color)
        # Text color
        self.color_text = kwargs.get('text', self.color_text)
        # Horizonal line color
        self.color_line = kwargs.get('line', self.color_line)
        # Vertical line color
        self.color_vertical = kwargs.get('vertical', self.color_vertical)
        # Column separator color
        self.color_separator = kwargs.get('separator', self.color_separator)

    def set_color(self, color):
        self.color = color

    def set_color_text(self, color):
        self.color_text = color

    def set_color_line(self, color):
        self.color_line = color

    def set_color_vertical(self, color):
        self.color_vertical = color

    def set_color_separator(self, color):
        self.color_separator = color

    def draw_line(self):
        line = self.chr_horizontal * self.width()
        
        if self.color_line:
            line = color(self.color_line, line)
        elif self.color:
            line = color(self.color, line)
        
        print line

    def print_text(self, text):
        text = get_text(text)
        print text

    def get_text(self, text):
        if self.color_text:
            text = color(self.color_text, text)
        elif self.color:
            text = color(self.color, text)

        return text

    def get_clean_text(self, text):
        for k, v in colors.iteritems():
            text = text.replace(v, '')
        text = text.replace('\x1b[0m', '')
        
        return text

    def get_chr_vertical(self):
        char = self.chr_vertical
        
        if self.color_vertical:
            char = color(self.color_vertical, char)
        elif self.color:
            char = color(self.color, char)

        return char

    def get_chr_horizontal(self):
        char = self.chr_horizontal
        
        if self.color_line:
            char = color(self.color_line, char)
        elif self.color:
            char = color(self.color, char)

        return char

    def get_separator(self):
        char = self.chr_separator

        if self.color_separator:
            char = color(self.color_separator, char)
        elif self.color:
            char = color(self.color, char)

        return char

class table(base_object):
    def __init__(self):
        super(table, self).__init__()
        self.rows = []

    def add_head(self, data):
        if isinstance(data, list):
            self.rows.append(head(data))
        elif isinstance(data, head):
            self.rows.append(data)

    def get_head(self):
        ret = None

        for r in self.rows:
            if isinstance(r, head):
                ret = r
                break

        return ret

    def add_row(self, data):
        if isinstance(data, list):
            self.rows.append(row(data))
        elif isinstance(data, row):
            self.rows.append(data)

    def add_separator(self, data=None, newseparator=None):
        if data:
            self.rows.append(separator(data))
        elif newseparator:
            self.rows.append(newseparator)

    def get_more_columns(self):
        columns = 0

        for r in self.rows:
            c = len(r.columns)
            if c > columns:
                columns = c

        return columns

    def clean(self):
        self.rows = []

    def width_column(self, num_column):
        width = 0
        
        # See which is the largest 'num_column' column
        for r in self.rows:
            w = r.width_column(num_column)
            if w > width:
                width = w
        
        # Return with a the spaces and left separation
        return width + 1

    def width(self):
        # Start with borders
        width = len(self.chr_vertical)
        
        # See if has head for count columns or take
        # the row with more columns
        head = self.get_head()
        if head:
            columns = len(head.columns)
        else:
            columns = self.get_more_columns()

        # Add left border columns and spaces
        width += (len(self.chr_separator) * columns) + columns

        for x in range(columns):
            width += self.width_column(x)
        
        return width

    def sort(self, column, desc=False):
        if isinstance(column, str):
            column = self.get_index_column(column)
            if column is False:
                return

        try:
            self.rows.sort(
                key = lambda r: int(r.get_clean_column(column)) if not isinstance(r, head) else 0, 
                reverse = desc)
        except Exception:
            self.rows.sort(
                key = lambda r: r.get_clean_column(column), 
                reverse = desc)

    def sort_asc(self, column):
        self.sort(column, False)

    def sort_desc(self, column):
        self.sort(column, True)

    def get_index_column(self, value):
        ret = False
        headc = self.get_head()
        if not headc:
            return
        
        for x in range(len(headc.columns)):
            if headc.get_clean_column(x) == value:
                ret = x
                break
        
        return ret

    def draw(self):
        # Draw head if has
        h = self.get_head()
        if h:
            h.draw(self)
        else:
            self.draw_line()

        # Draw all rows
        for r in self.rows:
            if isinstance(r, head):
                continue
            r.draw(self)
        
        # Draw button line
        self.draw_line()

class row(base_object):
    def __init__(self, data=None):
        super(row, self).__init__()
        self.columns = []
        if data:
            self.set_columns(data)
        self.use = self
        self.was_set_use = False
    
    def use_attr(self, use):
        self.use = use
        self.was_set_use = True

    def useme(self):
        self.use = self
        self.was_set_use = True
    
    def set_columns(self, data):
        for c in data:
            self.columns.append(str(c))

    def add_column(self, column):
        self.columns.append(str(column))

    def get_column(self, column):
        if column >= len(self.columns):
            return ''
        return self.columns[column]
    
    def get_clean_column(self, column):
        return self.get_clean_text(self.get_column(column))

    def str_column(self, column):
        '''
        Return a string with the column
        '''
        text = ''
        # We must add spaces to complete the line
        if not self.table:
            step = ' ' * (self.width_column(column) - len(self.get_clean_column(column)))
        else:
            step = ' ' * (self.table.width_column(column) - len(self.get_clean_column(column)))
        
        # If is the second column or more add a separator character
        if column > 0:
            text = self.use.get_separator()

        return text + ' ' + self.use.get_text(self.get_column(column)) + step

    def draw(self, table=None):
        # Is drawing a table
        if table:
            self.table = table
            # If use was not set, use table
            if not self.was_set_use:
                self.use = table
            head = table.get_head()
            if head:
                stop = len(head.columns)
            else:
                stop = table.get_more_columns()
        # Is drawing only this row
        else:
            self.table = None
            stop = len(self.columns)
        
        draw = ''
        for x in range(stop):
            draw += self.str_column(x)

        print self.use.get_chr_vertical() + draw + self.use.get_chr_vertical()

    def width(self):
        width = 1
        columns = len(self.columns)
        # Add left border columns
        width += (len(self.chr_separator) * columns) + columns

        for x in range(columns):
            width += self.width_column(x)

        return width

    def width_column(self, num_column):
        try:
            return len(self.get_clean_column(num_column)) + 1
        except:
            return 0

class head(row):
    def __init__(self, data=None):
        super(head, self).__init__(data)

    def draw(self, table = None):
        if table:
            if not self.was_set_use:
                line = table.get_chr_horizontal() * table.width()
            else:
                line = self.use.get_chr_horizontal() * table.width()
        # Draw top line
        print line
        # Draw row
        super(head, self).draw(table)
        # Draw button line
        print line

class separator(head):
    def __init__(self, data=None):
        super(head, self).__init__(data)