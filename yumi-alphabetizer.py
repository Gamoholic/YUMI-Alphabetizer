#!/usr/bin/env python
import sys, re, os



def alpha(file_in):
    file_open = open(file_in, 'rU').read()
    file_open = re.sub(' \n', '\n', file_open)
    file_open = re.sub('\n{3,}', '\n\n', file_open)
    file_split = file_open.split('\nlabel')
    file_dict = {}
    
    if file_in.endswith('syslinux.cfg'):
        final = file_split[0] + '\n' + 'label' + file_split[1]
        entries_to_sort = file_split[2:]
    else:
        final = file_split[0]
        entries_to_sort = file_split[1:]
        
    for entry in entries_to_sort:
        entry = 'label' + entry
        entry_name = re.search('label (.*?)\n', entry).group(1)
        file_dict[entry_name] = entry
        
    for key in sorted(file_dict):
        final += '\n' + file_dict[key]
        
    file_out = open(file_in, 'w')
    file_out.write(final)
    file_out.close



# Main
rootdir = sys.argv[1]
sub_dir = os.path.join(rootdir, 'multiboot')
main_dir = os.path.join(sub_dir, 'menu')
local_list = os.listdir(main_dir)
cfg_list = [
    'antivirus.cfg',
    'linux.cfg',
    'netbook.cfg',
    'other.cfg',
    'system.cfg',
    'isos.cfg']

for config in cfg_list:
    if config in local_list:
        alpha(os.path.join(main_dir, config))
alpha(os.path.join(sub_dir, 'syslinux.cfg'))
