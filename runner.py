import json
import pathlib
import shutil
import sys
from warnings import warn

script = sys.argv[1]
SOL_DIR = 'solutions'
NB_DIR = 'notebooks'


def backup_nb(path):
    new_path = path.absolute().parent.parent / 'tmp_backup' / path.name
    shutil.copy(path, new_path)


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
            ret.append(line[:line.find('#')] + 'pass # Your Code Here\n')
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
            new_cell['outputs'] = []
            new_cell['execution_count'] = None
            new_cell['metadata'] = {}
        ret.append(new_cell)
    nb['cells'] = ret
    return nb


def exercise_notebook(path, backup=False):
    path = pathlib.Path(path)
    if backup:
        backup_nb(path)
    new_path = path.parent.with_name('notebooks') / path.name
    nb = load_nb(path)
    new_nb = change_notebook(nb)
    return save_nb(new_nb, new_path)


switch = {
    'strip': exercise_notebook,
    'backup': backup_nb,
}


###
class Run:
    @staticmethod
    def strip():
        path = pathlib.Path(SOL_DIR)
        for p in path.glob('Part*.ipynb'):
            print(p)
            exercise_notebook(p)

    @staticmethod
    def backup():
        path = pathlib.Path(SOL_DIR)
        for p in path.glob('Part*.ipynb'):
            print(p)
            backup_nb(p)

    @staticmethod
    def rmnb():
        path = pathlib.Path(NB_DIR)
        shutil.rmtree(path)
        path.mkdir()


if __name__ == '__main__':
    print(script)
    # p = pathlib.Path('solutions/Part 6 - Behind the Scenes.ipynb')
    # exercise_notebook(p)
    getattr(Run, script)()
