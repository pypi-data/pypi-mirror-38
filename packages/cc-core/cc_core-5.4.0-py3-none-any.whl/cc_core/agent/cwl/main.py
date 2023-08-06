import os
from argparse import ArgumentParser

from cc_core.commons.files import load_and_read, dump_print
from cc_core.commons.cwl import cwl_to_command, cwl_validation
from cc_core.commons.cwl import cwl_input_files, cwl_output_files, cwl_input_file_check, cwl_output_file_check
from cc_core.commons.shell import execute, shell_result_check
from cc_core.commons.exceptions import exception_format


DESCRIPTION = 'Run a CommandLineTool as described in a CWL_FILE and its corresponding JOB_FILE.'


def attach_args(parser):
    parser.add_argument(
        'cwl_file', action='store', type=str, metavar='CWL_FILE',
        help='CWL_FILE containing a CLI description (json/yaml) as local path or http url.'
    )
    parser.add_argument(
        'job_file', action='store', type=str, metavar='JOB_FILE',
        help='JOB_FILE in the CWL job format (json/yaml) as local path or http url.'
    )
    parser.add_argument(
        '--outdir', action='store', type=str, metavar='OUTPUT_DIR',
        help='Output directory, default current directory.'
    )
    parser.add_argument(
        '--dump-format', action='store', type=str, metavar='DUMP_FORMAT', choices=['json', 'yaml', 'yml'],
        default='yaml', help='Dump format for data written to files or stdout, default is "yaml".'
    )


def main():
    parser = ArgumentParser(description=DESCRIPTION)
    attach_args(parser)
    args = parser.parse_args()

    result = run(**args.__dict__)
    dump_print(result, args.dump_format)

    if result['state'] == 'succeeded':
        return 0

    return 1


def run(cwl_file, job_file, outdir, **_):
    result = {
        'command': None,
        'inputFiles': None,
        'process': None,
        'outputFiles': None,
        'debugInfo': None,
        'state': 'succeeded'
    }

    try:
        cwl_data = load_and_read(cwl_file, 'CWL_FILE')
        job_data = load_and_read(job_file, 'JOB_FILE')

        cwl_validation(cwl_data, job_data)

        input_dir = os.path.split(os.path.expanduser(job_file))[0]

        command = cwl_to_command(cwl_data, job_data, input_dir=input_dir)
        result['command'] = command

        input_files = cwl_input_files(cwl_data, job_data, input_dir=input_dir)
        result['inputFiles'] = input_files
        cwl_input_file_check(input_files)

        process_data = execute(command)
        result['process'] = process_data
        shell_result_check(process_data)

        output_files = cwl_output_files(cwl_data, output_dir=outdir)
        result['outputFiles'] = output_files
        cwl_output_file_check(output_files)
    except:
        result['debugInfo'] = exception_format()
        result['state'] = 'failed'

    return result
