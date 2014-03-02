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
    return color + text + '\x1b[0m'

class base_object(object):
    def __init__(self):
        # Horizonal line character
        self.chr_horizontal = '*'
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

    def set_color(self, color):
        self.color = color

    def set_color_text(self, color):
        self.color_text = color

    def set_color_line(self, color):
        self.color_line = color

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

class table(base_object):
    def __init__(self):
        super(table, self).__init__()
        self.rows = []

    def add_head(self, data = None, newhead = None):
        if data:
            self.rows.append(head(data))
        elif newhead:
            self.rows.append(newhead)

    def get_head(self):
        ret = None

        for r in self.rows:
            if type(r) is head:
                ret = r
                break

        return ret

    def add_row(self, data = None, newrow = None):
        if data:
            self.rows.append(row(data))
        elif newrow:
            self.rows.append(newrow)

    def add_separator(self, data = None, newseparator = None):
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
        width = 2
        
        # See if has head for count columns or take
        # the row with more columns
        head = self.get_head()
        if head:
            columns = len(head.columns)
        else:
            columns = self.get_more_columns()

        # Add left border columns and spaces
        width += columns * 2

        for x in range(columns):
            width += self.width_column(x)
        
        return width

    def draw(self):
        # Draw head if has
        head = self.get_head()
        if head:
            head.draw(self)
        else:
            self.draw_line()

        # Draw all rows
        for r in self.rows:
            if type(r) is row or type(r) is separator:
                r.draw(self)
        
        # Draw button line
        self.draw_line()

class row(base_object):
    def __init__(self, data):
        super(row, self).__init__()
        self.columns = data
    
    def get_column(self, column):
        if column >= len(self.columns):
            return ''
        return self.columns[column]

    def str_column(self, column, use):
        '''
        Return a string with the column
        '''
        text = ''
        # We must add spaces to complete the line
        step = ' ' * (use.width_column(column) - len(self.get_column(column)))
        
        # If is the second column or more add a separator character
        if column > 0:
            text = use.chr_separator
        else:
            step += ' '

        return text + ' ' + use.get_text(self.get_column(column)) + step

    def draw(self, table = None):
        # Use table attributes
        if table:
            use = table
            head = table.get_head()
            if head:
                stop = len(head.columns)
            else:
                stop = table.get_more_columns()
        # Use row attributes
        else:
            use = self
            stop = len(self.columns)
        
        draw = ''
        for x in range(stop):
            draw += self.str_column(x, use)

        print use.chr_vertical + draw + use.chr_vertical

    def width(self):
        width = 0
        columns = len(self.columns)
        # Add left border columns
        width += columns

        for x in range(columns):
            width += self.width_column(x)

        return width

    def width_column(self, num_column):
        try:
            return len(self.columns[num_column]) + 1
        except:
            return 0

class head(row):
    def __init__(self, data):
        super(head, self).__init__(data)

    def draw(self, table):
        # Draw top line
        table.draw_line()
        # Draw row
        super(head, self).draw(table)
        # Draw button line
        table.draw_line()

class separator(head):
    def __init__(self, data):
        super(head, self).__init__(data)