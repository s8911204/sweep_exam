import json
import os


output_content = {}

def read_jsonl_and_write(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            json_dict = json.loads(line)
            combined_str = json_dict['prefix'] + '[jackie]\n' + json_dict['suffix']
            output_file_name = f"{json_dict['filename']}_{json_dict['index']}" + '.c'
            #output_file_name = output_file_name.replace('/', '_')

            result = '{"task_id": "' + f"{json_dict['filename']}_{json_dict['index']}" + '", "completion": "jackie"}\n'
            
            with open(f"output/{output_file_name}", 'w') as wf:
                wf.write(combined_str)
            
            output_content[f"{json_dict['filename']}_{json_dict['index']}"] = result

    #with open(f"output/result_c.jsonl", 'a') as af:
    #    for key in sorted(output_content.keys()):
    #        result = output_content[key]
    #        af.write(result)

read_jsonl_and_write('fim-oneline-300-kernel510.jsonl')