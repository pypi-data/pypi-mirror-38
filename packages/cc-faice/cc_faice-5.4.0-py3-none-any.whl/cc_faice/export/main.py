from argparse import ArgumentParser

from cc_core.commons.files import load_and_read, dump, file_extension, wrapped_print
from cc_core.commons.red import red_validation
from cc_core.commons.templates import inspect_templates_and_secrets, fill_template, fill_validation
from cc_core.commons.engines import engine_validation

from cc_faice.commons.red import dump_agent_cwl, dump_agent_job, dump_app_cwl
from cc_faice.commons.docker import dump_job


DESCRIPTION = 'Export RED_FILE to standard CWL compatible with cwltool.'


def attach_args(parser):
    parser.add_argument(
        'red_file', action='store', type=str, metavar='RED_FILE',
        help='RED_FILE (json or yaml) containing an experiment description as local path or http url.'
    )
    parser.add_argument(
        '--fill-file', action='store', type=str, metavar='FILL_FILE',
        help='FILL_FILE (json or yaml) containing key-value pairs for template variables in RED_FILE as '
             'local path or http url.'
    )
    parser.add_argument(
        '--outdir', action='store', type=str, metavar='OUTPUT_DIR',
        help='Output directory, default current directory. Will be passed to ccagent in the container.'
    )
    parser.add_argument(
        '--non-interactive', action='store_true',
        help='Do not ask for jinja template values interactively.'
    )
    parser.add_argument(
        '--dump-format', action='store', type=str, metavar='DUMP_FORMAT', choices=['json', 'yaml', 'yml'],
        default='yaml', help='Dump format for data written to files or stdout, choices are "json" or "yaml", default '
                             'is "yaml".'
    )
    parser.add_argument(
        '--dump-prefix', action='store', type=str, metavar='DUMP_PREFIX', default='dumped_',
        help='Name prefix for files dumped to storage, default is "_dumped".'
    )


def main():
    parser = ArgumentParser(description=DESCRIPTION)
    attach_args(parser)
    args = parser.parse_args()
    return run(**args.__dict__)


def run(red_file, fill_file, outdir, non_interactive, dump_format, dump_prefix):
    red_data = load_and_read(red_file, 'RED_FILE')
    red_validation(red_data, False, container_requirement=True)
    engine_validation(red_data, 'container', ['docker'], 'faice export')

    fill_data = None
    if fill_file:
        fill_data = load_and_read(fill_file, 'FILL_FILE')
        fill_validation(fill_data)

    template_keys_and_values, secret_values = inspect_templates_and_secrets(red_data, fill_data, non_interactive)
    red_data = fill_template(red_data, template_keys_and_values, False, True)

    if red_data['container']['settings']['image'].get('auth'):
        wrapped_print([
            'WARNING: cannot export container.settings.image.auth to cwl.',
            ''
        ], error=True)

    if 'batches' in red_data:
        wrapped_print([
            'ERROR: cannot export RED_FILE containing batches.',
            'Use "faice convert batches" to separate batches into individual files, then use "faice export" on the '
            'generated files.',
        ], error=True)
        return 1

    ext = file_extension(dump_format)
    dumped_app_cwl_file = '{}app-cli.cwl'.format(dump_prefix)
    dumped_app_red_file = '{}app-red.{}'.format(dump_prefix, ext)
    dumped_app_job_file = '{}app-job.{}'.format(dump_prefix, ext)
    dumped_agent_cwl_file = '{}agent-cli.cwl'.format(dump_prefix)
    dumped_agent_job_file = '{}agent-job.{}'.format(dump_prefix, ext)
    dumped_agent_job_ignore_output_file = '{}agent-job-ignore-output.{}'.format(dump_prefix, ext)
    agent_stdout_file = 'agent-stdout.{}'.format(ext)

    dumped_app_job_data = dump_job(red_data['inputs'], '.')
    dumped_agent_cwl_data = dump_agent_cwl(red_data, agent_stdout_file)
    dumped_agent_job_data = dump_agent_job(dumped_app_red_file, outdir, dump_format, False)
    dumped_agent_job_ignore_output_data = dump_agent_job(dumped_app_red_file, outdir, dump_format, True)
    dumped_app_cwl_data = dump_app_cwl(red_data)

    dump(dumped_app_cwl_data, dump_format, dumped_app_cwl_file)
    dump(red_data, dump_format, dumped_app_red_file)
    dump(dumped_app_job_data, dump_format, dumped_app_job_file)
    dump(dumped_agent_cwl_data, dump_format, dumped_agent_cwl_file)
    dump(dumped_agent_job_data, dump_format, dumped_agent_job_file)
    dump(dumped_agent_job_ignore_output_data, dump_format, dumped_agent_job_ignore_output_file)

    option3_command = 'cwltool {} {}'.format(dumped_app_cwl_file, dumped_app_job_file)
    if outdir:
        option3_command = '{} --outdir {}'.format(option3_command, outdir)

    wrapped_print([
        'OPTION 1:',
        'Use cwltool to execute app in container via "ccagent red" with support for REMOTE inputs and REMOTE outputs.',
        '$ cwltool {} {}'.format(dumped_agent_cwl_file, dumped_agent_job_file),
        '',
        'OPTION 2:',
        'Use cwltool to execute app in container via "ccagent red" with support for REMOTE inputs and LOCAL outputs.',
        '$ cwltool {} {}'.format(dumped_agent_cwl_file, dumped_agent_job_ignore_output_file),
        '',
        'OPTION 3:',
        'Use cwltool to execute app in container with support for LOCAL inputs and LOCAL outputs.',
        'ATTENTION: adjust input file paths in {}.'.format(dumped_app_job_file),
        '$ {}'.format(option3_command),
        '',
        'OPTION 4:',
        'Customize exported CWL and JOB files.'
    ])

    return 0
