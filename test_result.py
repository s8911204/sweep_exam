import argparse
import json
from pathlib import Path


def get_benchmark_dict(benchmark_file: str) -> dict:
    benchmarks = {}
    for line in Path(benchmark_file).read_text().splitlines():
        d = json.loads(line)
        benchmarks[d['filename']+'_'+str(d['index'])] = {
            'prefix': d['prefix'],
            'suffix': d['suffix'],
            'removed_line': d['removed_line']
        }

    return benchmarks


def parse_results(result_folder: str, benchmarks: dict, extension: str = '.c', result_jsonl_path: str = None) -> dict:
    result_folder = Path(result_folder)
    files = [file for file in result_folder.iterdir() if file.is_file()]
    if not extension.startswith('.'): extension = '.'+extension

    results = {}
    for file in files:
        if str(file).endswith(extension):
            code = Path(file).read_text()
            code = code.replace(benchmarks[str(file.stem)]['prefix'], '')
            code = code.replace(benchmarks[str(file.stem)]['suffix'], '')
            results[str(file.stem)] = code
        else:
            print(f"Skipping file in {str(result_folder.resolve())} -> {file.name}")

    if result_jsonl_path:
        save_path = Path(result_jsonl_path)
        with open(save_path, 'w') as f:
            for k, v in results.items():
                f.write(json.dumps({'task_id': k, 'completion': v, 'removed_line': benchmarks[k]['removed_line']})+ '\n')

    return results


def compare(results: dict, benchmark: dict, mode: str = 'exact_match') -> dict:
    n = len(results)
    count = 0
    if mode == 'exact_match':
        for task_id in results.keys():
            if results[task_id].strip() == benchmark[task_id]['removed_line'].strip():
                count += 1
    else:
        raise NotImplementedError(f"Modes other than {mode} are not available.")
    
    return {'correct': count, 'test_count': n, 'accuracy': count/n}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('result_folder', type=str, help="Result folder.")
    parser.add_argument('benchmark_file', type=str, help="Input benchmark file with `task_id` and `removed_line` keys.")
    parser.add_argument('--extension', type=str, default='.c', help="Extension to search for in result-folder.")
    parser.add_argument('--parsed_result_filename', type=str, help="Indicate the save path for parsed results.  Does not save file if null.")

    args = vars(parser.parse_args())
    benchmarks = get_benchmark_dict(args['benchmark_file'])
    results = parse_results(
        args['result_folder'],
        benchmarks,
        extension=args['extension'],
        result_jsonl_path=args['parsed_result_filename']
    )
    output = compare(results, benchmarks)
    print(f"Out of {output['test_count']} test cases, {output['correct']} are correct.")
    print(f"The accuracy is {output['accuracy']*100:.2f}%.")