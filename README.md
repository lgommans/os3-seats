# OS3/SNE seat layout painter

Upstairs lab: `seats.py up [options]`  
Downstairs lab: `seats.py down [options]`  
Who is on a seat: `seats.py seat <number> [options]`  
Find someone: `seats.py find <name> [options]`

This tool requires a csv file on STDIN:  
`cat seats.csv | python3 seats.py down`

Or a little easier:  
`<seats.csv python3 seats.py down`

The csv file is in the format `seat,name\n` (without header), e.g. `1,Jon Doe`

If the output is too wide for your screen, pipe it to `less -S` and use arrow keys to pan.

Options:  
    `-s`  Use first names only when displaying the grid
    
