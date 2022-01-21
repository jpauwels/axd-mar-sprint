#!/usr/bin/env python
import json

def cleaner(input_path, output_path=None, strip_solutions=False):

    with open(input_path) as f:
        master = json.load(f)

    # remove unnecessary metadata
    master['metadata'].pop('celltoolbar', None)
    master['metadata'].pop('colab', None)
    master['metadata'].pop('nteract', None)
    master['metadata'].pop('toc', None)
    master['metadata'].pop('kernel_info', None)
    master['metadata'].pop('interpreter', None)
    master['metadata']['kernelspec'].pop('display_name', None)
    master['metadata']['kernelspec'].pop('name', None)
    master['metadata']['language_info'].pop('version', None)

    # sort keys in each cell dict
    master['cells'][:] = [dict(sorted(cell.items())) for cell in master['cells']]

    if strip_solutions:
        master['cells'][:] = [cell for cell in master['cells']
                              if 'strip' not in cell['metadata'].get('tags', [])]
    for cell in master['cells']:
        tags = cell['metadata'].get('tags', [])
        if strip_solutions:
            if 'solution' in tags:
                if cell['cell_type'] == 'markdown':
                    cell['source'] = ['_your answer here_']
                else:
                    cell['source'] = ['# your code here']
        #     cell['metadata'] = dict()
        # elif tags:
        #     cell['metadata'] = {'tags': tags}
        # else:
        #     cell['metadata'] = dict()
            cell['metadata'].pop('tags', None)
        for k in set(cell['metadata'].keys()).difference(['collapsed', 'scrolled', 'deletable', 'editable', 'format', 'name', 'tags', 'jupyter', 'execution']):
            cell['metadata'].pop(k, None)
        # clear output and count of code cells
        if cell['cell_type'] == 'code':
            cell['execution_count'] = None
            cell['outputs'] = []

    if output_path is None:
        output_path = input_path

    with open(output_path, 'w') as f:
        json.dump(master, f, indent=1, ensure_ascii=False)
        f.write('\n')

if __name__ == '__main__':
    import sys
    from os.path import basename
    if len(sys.argv) > 1 and len(sys.argv) < 5:
        cleaner(*sys.argv[1:])
    else:
        print('Usage: {} input [output [strip_solutions]]'.format(basename(sys.argv[0])))
