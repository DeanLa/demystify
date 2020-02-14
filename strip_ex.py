import json
import pathlib
from warnings import warn
import shutil

SUFFIX = 'class'
if not SUFFIX:
    exit(-1)

def load_nb(path: str or pathlib.Path):
    path = pathlib.Path(path)
    with path.open() as f:
        nb = json.load(f)
    return nb


def save_nb(nb, path: str or pathlib.Path):
    path = pathlib.Path(path)
    with path.open(mode='w') as f:
        json.dump(nb, f)
    return path.absolute()


def get_code_cells(nb: dict):
    cells = nb['cells']
    code = [cell['source'] for cell in cells if cell['cell_type'] == 'code']
    return code


def comment(line, s: str):
    line = line.lower().replace(' ', '').replace('#', '')
    return line.startswith(s.lower())


def replace_exercise(cell):
    if len(cell) == 0:
        return cell
    if not comment(cell[0], 'ex'):
        return cell
    ignore = False
    ret = []
    for line in cell:
        if comment(line, 'boe'):
            ignore = True
            ret.append( line[:line.find('#')] + 'pass # Your Code Here\n')
        if comment(line, 'eoe'):
            ignore = False
            continue
        if ignore:
            continue
        ret.append(line)
    if ignore:
        warn('Cell not closed')
        ret = ['# Exercise not closed\n'] + ret
    return ret


def change_notebook(nb):
    cells = nb['cells']
    ret = []
    for cell in cells:
        new_cell = cell
        if cell['cell_type'] == 'code':
            new_code = replace_exercise(cell['source'])
            new_cell['source'] = new_code
        ret.append(new_cell)
    nb['cells'] = ret
    return nb


def exercise_notebook(path, backup=False):
    path = pathlib.Path(path)
    if backup:
        backup_nb(path)
    new_path = path.with_name(f'{path.stem}_{SUFFIX}.ipynb')
    nb = load_nb(path)
    new_nb = change_notebook(nb)
    return save_nb(new_nb, new_path)


def backup_nb(path):
    new_path = path.absolute().parent / 'tmp_backup' / p.name
    shutil.copy(path, new_path)

if __name__ == '__main__':
    path = pathlib.Path()
    for p in path.glob('Part*.ipynb'):
        if p.stem.endswith(SUFFIX):
            continue
        print(p)
        exercise_notebook(p)
    print()
