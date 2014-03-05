PyTerminalTable
===============

Class for draw tables in the terminal


Usage
=====
######Simple usage:
```python 
from pyterminaltable import table

t = table.table()

t.add_head(['Name', 'Last Name', 'Email'])
t.add_row(['Lisandro', 'Seijo', 'example@example.com'])
t.add_row(['Leandro', 'Romagnoli', 'example@example.com'])
t.add_row(['Beto', 'Acosta', 'example@example.com'])

t.draw()
```
Print:
```
=================================================
| Name      | Last Name  | Email                |
=================================================
| Lisandro  | Seijo      | example@example.com  |
| Leandro   | Romagnoli  | example@example.com  |
| Beto      | Acosta     | example@example.com  |
=================================================

```
######Drawing a simple row:
```python
from pyterminaltable import table

print 'Simple row:'
r = table.row(['one column', 'two column', 'three column'])
r.draw()

print 'Simple head:'
h = table.head(['one column head', 'two column head', 'three column head'])
h.draw()
```
Output:
```
Simple row:
| one column | two column | three column |

Simple head:
=========================================================
| one column head | two column head | three column head |
=========================================================

```
Style
=====
You can change the table style:
```python
# Change the color
t.set_color('blue')
# Change character of lines
t.chr_horizontal = '*'
t.chr_vertical = '{}'
t.chr_separator = '[]'

t.draw()
```
And we have (in blue):
```
*****************************************************
{} Name      [] Last Name  [] Email                {}
*****************************************************
{} Lisandro  [] Seijo      [] example@example.com  {}
{} Leandro   [] Romagnoli  [] example@example.com  {}
{} Beto      [] Acosta     [] example@example.com  {}
*****************************************************
```
To print with color, is used a function named color(), you can use this in any item of the list to print a unique column with color:
```python
t.add_row(['row 1', 'row 2', table.color('red', 'row 3')])
t.add_row(['row 1', table.color('green', 'row 2'), 'row 3'])
t.add_row([table.color('blue', 'row 1'), 'row 2', 'row 3'])
```

######Style Methods:
* set_colors(color, text, line, vertical, separator):
 	* color: change general color
	* text: change text color
	* line: change horizontal line color
	* vertical: change vertical line color
	* separator: change column's separator color
* set_color(color)
* set_color_text(color)
* set_color_line(color)
* set_color_vertical(color)
* set_color_separator(color)

######Style attributes:
* chr_horizontal
* chr_vertical
* chr_separator

```
Note: this methods and attributes are availables for table, row and head.
```

######Style Functions:
* color(color, text)

######Colors name:
* black
* red
* green
* yellow
* blue
* pink
* skyblue
* white

Advanced usage
==============
You can draw a table and change the style of a specific row calling the method row.useme(). That say what go to use his attributes and no the table attributes.

######Example:
```python
t = table.table()
t.add_head(['Column 1', 'Column 2', 'Column 3'])

# Create a row
r = table.row(['Attr 1', 'Attr 2', 'Attr 3'])
# Change the stye
r.set_colors(color = 'blue', text = 'red')
r.chr_separator = '*'
# Call method useme
r.useme()
# Add row
t.add_row(r)

# Add more rows
t.add_row(['Attr 4', 'Attr 5', 'Attr 6'])
t.add_row(['Attr 7', 'Attr 8', 'Attr 9'])
# Draw table
t.draw()
```
We get:
```
=====================================
| Column 1  | Column 2  | Column 3  |
=====================================
| Attr 1    * Attr 2    * Attr 3    |
| Attr 4    | Attr 5    | Attr 6    |
| Attr 7    | Attr 8    | Attr 9    |
=====================================
```
And same for the head:
```python
t = table.table()

h = table.head(['Column 1', 'Column 2', 'Column 3'])
h.set_colors(color = 'blue', text = 'red')
h.chr_horizontal = '+'
h.useme()
t.add_head(h)

t.add_row(['Attr 1', 'Attr 2', 'Attr 3'])
t.add_row(['Attr 4', 'Attr 5', 'Attr 6'])
t.add_row(['Attr 7', 'Attr 8', 'Attr 9'])

t.draw()
```
```
+++++++++++++++++++++++++++++++++++++
| Column 1  | Column 2  | Column 3  |
+++++++++++++++++++++++++++++++++++++
| Attr 1    | Attr 2    | Attr 3    |
| Attr 4    | Attr 5    | Attr 6    |
| Attr 7    | Attr 8    | Attr 9    |
=====================================
```

######Using prototypes:
Sometimes for any reason we must use the same style depending of an attribute or any condition. For that its easier to create first prototype rows with the style and then assign calling the method use_attr().
```python
data = [
   ['Dog', 'Droopy', 10],
   ['Cat', 'Felix', 5],
   ['Bird', 'Tweety', 10],
   ['Dog', 'Muttley', 5],
   ['Cat', 'Top Cat', 10],
   ['Bird', 'Woody', 5]
]
# Table
t = table.table()
t.add_head(['Specie', 'Name', 'Years'])

# Creating prototypes
dog_row = table.row()
dog_row.set_colors(color = 'red')
dog_row.chr_separator = '*'

bird_row = table.row()
bird_row.set_colors(color = 'green')
bird_row.chr_separator = '/'

cat_row = table.row()
cat_row.set_colors(color = 'blue')
cat_row.chr_separator = '\\'

# Fill table
for animal in data:
	# Create the row
	r = table.row(animal)

	# See wich specie and add the row with style using use_attr
	if animal[0] == 'Dog':
		r.use_attr(dog_row)
	elif animal[0] == 'Cat':
		r.use_attr(cat_row)
	elif animal[0] == 'Bird':
		r.use_attr(bird_row)

	# Add row in table
	t.add_row(r)

# Draw
t.draw()
```
Output:
```
===============================
| Specie  | Name     | Years  |
===============================
| Dog     * Droopy   * 10     |
| Cat     \ Felix    \ 5      |
| Bird    / Tweety   / 10     |
| Dog     * Muttley  * 5      |
| Cat     \ Top Cat  \ 10     |
| Bird    / Woody    / 5      |
===============================
```
######Use methods:
* useme()
* use_attr(use)

######Sort:
You can sort rows by a column using the methods table.sort() table.sort_asc() and table.sort.desc() and sending the name of column or index
```python
t = table.table()
t.add_head(['Serie', 'Seasons'])

t.add_row(['The Simpsons', 25])
t.add_row(['Family Guy', 12])
t.add_row(['The Big Bang Theory', 7])
t.add_row(['South Park', 17])

# Sort by Seasons asc
print 'Order by N° of seasons desc'
t.sort_desc('Seasons') # or t.sort_desc(1), or t.sort(1, true)
t.draw()

# Sort by serie's name desc
print 'Order by serie\'s name asc'
t.sort_asc('Serie') # or t.sort_asc(0), or t.sort(0)
t.draw()
```
```
Order by N of seasons desc
===================================
| Serie                | Seasons  |
===================================
| The Simpsons         | 25       |
| South Park           | 17       |
| Family Guy           | 12       |
| The Big Bang Theory  | 7        |
===================================

Order by serie's name asc
===================================
| Serie                | Seasons  |
===================================
| Family Guy           | 12       |
| South Park           | 17       |
| The Big Bang Theory  | 7        |
| The Simpsons         | 25       |
===================================
```
######Sort methods:
* sort(column, desc = False)
* sort_desc(column)
* sort_asc(column)

Others
======
Table, row and head methods:
* draw(): print the table or row
* draw_line(): draw a line
* width(): return the width
* width_column(num_column): return the width of a specific column by index

[See complete list of class, methods and attributes](https://github.com/LisandroSeijo/PyTerminalTable/wiki)

Licence
=======
```
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2014 Lisandro Seijo <lisandroseijo@gmail.com>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```

Author
=======
Lisandro Seijo, [@LisandroSeijo](https://twitter.com/LisandroSeijo)