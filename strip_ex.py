import json
import pathlib


def load_nb(path: str or pathlib.Path):
    path = pathlib.Path(path)
    with path.open() as f:
        nb = json.load(f)
    return nb

def save_nb(path: str or pathlib.Path):
    pass

def get_code_cells(nb: dict):
    cells = nb['cells']
    code = [cell['source'] for cell in cells if cell['cell_type'] == 'code']
    return code


def comment(line, s: str):
    line = line.lower().replace(' ', '').replace('#', '')
    return line.startswith(s.lower())


def replace_ex(cell):
    if not comment(cell[0], 'ex'):
        return cell
    ignore = False
    ret = []
    for line in cell:
        if comment(line, 'boe'):
            ignore = True
            line = line[:line.find('#')] + 'pass\n'
            ret.append(line)
        if comment(line, 'eoe'):
            ignore = False
            continue
        if ignore:
            continue
        ret.append(line)
    return ret

def change_notebook(nb):
    cells = nb['cells']
    ret = []
    for cell in cells:
        new_cell = cell
        if cell['cell_type'] == 'code':
            new_code = replace_ex(cell['source'])
            new_cell['source'] = new_code
        ret.append(new_cell)
    nb['cells'] = ret
    return nb



if __name__ == '__main__':
    nb = load_nb('Part 2 - Array Shape.ipynb')
    code = get_code_cells(nb)
    new_nb = change_notebook(nb)
    x = replace_ex(code[-7])
    y = replace_ex(code[-8])
    print()
