#!/usr/bin/env python
import sys, re, os

#------------------------------------------------------------------------------#
# Global Variables                                                             #
#------------------------------------------------------------------------------#

ARGS = sys.argv[1:]
if not ARGS:
    print 'usage: mountpoint_of_drive'
    sys.exit(1)



#------------------------------------------------------------------------------#
# Functions                                                                    #
#------------------------------------------------------------------------------#

def alpha(file_in):
    file_open = open(file_in, 'rU').read()
    
    # Remove spaces before newlines
    file_open = re.sub(' \n', '\n', file_open)
    
    # Remove excess newlines
    file_open = re.sub('\n{3,}', '\n\n', file_open)
    
    # Set the word used to split the config into its menu blocks
    if file_in.endswith('syslinux.cfg'):
        split_word = 'label'
    else:
        split_word = '#start'
    
    # Split the config into its menu blocks
    file_split = file_open.split('\n' + split_word)
    
    # Divide the config so the first block doesn't get sorted
    final = file_split[0]
    entries_to_sort = file_split[1:]
        
    file_dict = {}    
    for entry in entries_to_sort:
        
        # The split function removes the split_word, so add it back
        entry = split_word + entry
        
        # Find the name of the block and add it the dictionary
        entry_name = re.search(split_word + ' (.*?)\n', entry).group(1)
        file_dict[entry_name] = entry
        
    # All this work just to get ready for these 2 lines...
    for key in sorted(file_dict):
        final += '\n' + file_dict[key]
        
    # Write the sorted config
    file_out = open(file_in, 'w')
    file_out.write(final)
    file_out.close



#------------------------------------------------------------------------------#
# Main                                                                         #
#------------------------------------------------------------------------------#

rootdir = ARGS[0]
sub_dir = os.path.join(rootdir, 'multiboot')
main_dir = os.path.join(sub_dir, 'menu')
local_list = os.listdir(main_dir)
cfg_list = [
    'antivirus.cfg', 'linux.cfg', 'netbook.cfg',
    'other.cfg', 'system.cfg', 'isos.cfg']

for config in cfg_list:
    if config in local_list:
        alpha(os.path.join(main_dir, config))
alpha(os.path.join(sub_dir, 'syslinux.cfg'))
