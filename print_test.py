import json
import os


output_content = {}

def read_jsonl_and_write(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            json_dict = json.loads(line)
            print(f"debug json_dict={json_dict}")
            combined_str = json_dict['prompt'] + '[jackie]\n' + json_dict['suffix']
            print(f"debug prompt={json_dict['prompt']}")
            print(f"debug suffix={json_dict['suffix']}")
            output_file_name = json_dict['task_id'] + '.cpp'
            output_file_name = output_file_name.replace('/', '_')

            result = '{"task_id": "' + json_dict['task_id'] + '", "completion": "jackie"}\n'
            
            with open(f"{output_file_name}", 'w') as wf:
                wf.write(combined_str)
            
            task_id = json_dict['task_id'] #HumanEval_0_has_close_elements
            id = task_id.split('_')[1]
            output_content[int(id)] = result

    #with open(f"output/result_cpp.jsonl", 'a') as af:
    #    for key in sorted(output_content.keys()):
    #        result = output_content[key]
    #        af.write(result)

read_jsonl_and_write('benchmark_single_line_cpp_test.jsonl')