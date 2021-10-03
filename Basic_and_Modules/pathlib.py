# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:27:26 2020

@author: rmileng
"""
import pathlib

pathlib.Path.cwd()
p = pathlib.Path('.') # the path of current folder
[x for x in p.iterdir() if x.is_dir()]
list(p.glob('**/*.py'))

p = pathlib.Path('D:\LYS\python_learning')
q = p / 'learn'
print(q)

pathlib.PurePath('setup.py')
pathlib.PurePath('sf','sdf/asdf')
pathlib.PurePath(Path('sf'),Path('sdf/asdf'))
pathlib.PureWindowsPath('F:\cookies\python\learnPython','\game')

p = pathlib.Path('.')
p
str(p)
p.name
p.with_suffix('.txt')
p.with_name('set_up.py')
p.owner()
p = Path('foo')

p.open('w').write('some text')
with p.open('w') as f: 
    f.write('sometex')
