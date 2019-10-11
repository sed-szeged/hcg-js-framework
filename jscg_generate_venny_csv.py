import copy
import json
import os
import sys
import itertools
from CONFIG import CONF

tools = {
    'acg-demand' : list(),
    'acg-oneshot' : list(),
    'dyn-v8' : list()
}

m_tools = {
    'acg-demand' : list(),
    'acg-oneshot' : list(),
    'dyn-v8' : list()
}

tool_mask = {
    'acg-demand' : True,
    'acg-oneshot' : True,
    'dyn-v8' : True
}
in_dir = os.path.join(CONF['cg-path'], 'x-compared')

def pad(seq, target_length, padding=None):
    length = len(seq)
    seq.extend([padding] * (target_length - length))
    return seq        

def get_greatest_len(dict_with_lists):
    ret = 0
    for key in dict_with_lists.keys():
        if len(dict_with_lists[key]) > ret:
            ret = len(dict_with_lists[key])
    return ret
    
def pad_lists(dict_with_lists):
    greatest_len = get_greatest_len(dict_with_lists)
    for key in dict_with_lists.keys():
        pad(dict_with_lists[key], greatest_len, '')
        
def print_lists(out_file, dict_with_lists):
    llen = len(next(iter(dict_with_lists.values())))
    out_file.write(','.join(dict_with_lists.keys()) + "\n")
    for i in range(llen):
        row = ""
        for key in dict_with_lists.keys():
            row += dict_with_lists[key][i] + ','
        out_file.write(row[:-1] + "\n")

def generate_csv():
    for tool in tool_mask:
        if not tool_mask[tool]:
            tools.pop(tool, None)
            m_tools.pop(tool, None)
            
    for file in os.listdir(in_dir):
        if file.endswith(".json"):
            data = json.load(open(os.path.join(in_dir, file)))
            f_data = data['links']
            if "filter" in sys.argv:
                f_data = filter(lambda x: x['valid'], data['links'])
            for link in f_data:            
                for tool in link['foundBy']:
                    if tool in tools:
                        tools[tool].append(link['label'])
                        m_tools[tool].append(link['label'])
            out_file = open(os.path.join(in_dir, file[:-5]) + ".csv", 'w')
            pad_lists(tools)
            print_lists(out_file, tools)
            for key in tools.keys():
                tools[key] = list()
            out_file.close()
    out_file = open(os.path.join(in_dir, "merged") + ".csv", 'w')
    pad_lists(m_tools)
    print_lists(out_file, m_tools)
    for key in m_tools.keys():
        m_tools[key] = list()
    out_file.close()
    
if __name__ == '__main__':
    generate_csv()