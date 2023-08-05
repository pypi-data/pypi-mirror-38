from __future__ import print_function
from bespin.config import ConfigFile
from bespin.api import BespinApi
from bespin.exceptions import IncompleteJobFileException, WorkflowConfigurationNotFoundException
from bespin.dukeds import DDSFileUtil
from bespin.dukeds import PATH_PREFIX as DUKEDS_PATH_PREFIX
from tabulate import tabulate
import yaml
import sys
from decimal import Decimal, ROUND_HALF_UP

STRING_VALUE_PLACEHOLDER = "<String Value>"
INT_VALUE_PLACEHOLDER = "<Integer Value>"
FILE_PLACEHOLDER = "dds://<Project Name>/<File Path>"
USER_PLACEHOLDER_VALUES = [STRING_VALUE_PLACEHOLDER, INT_VALUE_PLACEHOLDER, FILE_PLACEHOLDER]
USER_PLACEHOLDER_DICT = {
    'File': {
        "class": "File",
        "path": FILE_PLACEHOLDER
    },
    'int': INT_VALUE_PLACEHOLDER,
    'string': STRING_VALUE_PLACEHOLDER,
    'NamedFASTQFilePairType': {
        "name": STRING_VALUE_PLACEHOLDER,
        "file1": {
            "class": "File",
            "path": FILE_PLACEHOLDER
        },
        "file2": {
            "class": "File",
            "path": FILE_PLACEHOLDER
        }
    },
    'FASTQReadPairType': {
        "name": STRING_VALUE_PLACEHOLDER,
        "read1_files": [{
            "class": "File",
            "path": FILE_PLACEHOLDER
        }],
        "read2_files": [{
            "class": "File",
            "path": FILE_PLACEHOLDER
        }]
    }
}


class Commands(object):
    """
    Commands run based on command line input.
    """

    def __init__(self, version_str, user_agent_str):
        """
        :param version_str: str: version of bespin-cli
        :param user_agent_str: str: agent string to use when talking to bespin-api
        """
        self.version_str = version_str
        self.user_agent_str = user_agent_str

    def _create_api(self):
        config = ConfigFile().read_or_create_config()
        return BespinApi(config, user_agent_str=self.user_agent_str)

    def workflows_list(self, all_versions):
        """
        Print out a table of workflows/questionnaires
        :param all_versions: bool: when true show all versions otherwise show most recent
        """
        api = self._create_api()
        workflow_data = WorkflowDetails(api, all_versions)
        print(Table(workflow_data.column_names, workflow_data.get_column_data()))

    def workflow_configuration_show(self, tag, outfile):
        api = self._create_api()
        workflow_configuration = api.workflow_configurations_list(tag=tag)[0]
        outfile.write(yaml.dump(workflow_configuration, default_flow_style=False))

    def jobs_list(self):
        """
        Print out a table of current job statuses
        """
        api = self._create_api()
        jobs_list = JobsList(api)
        print(Table(jobs_list.column_names, jobs_list.get_column_data()))

    def init_job(self, tag, outfile):
        """
        Write a sample job file with placeholder values to outfile
        :param tag: str: tag representing which workflow/questionnaire to use
        :param outfile: file: output file that will have the sample job data written to
        """
        api = self._create_api()
        workflow_configuration = api.workflow_configurations_list(tag=tag)[0]
        job_file = JobConfiguration(workflow_configuration).create_job_file_with_placeholders()
        outfile.write(job_file.yaml_str())
        if outfile != sys.stdout:
            print("Wrote job file {}.".format(outfile.name))
            print("Edit this file filling in TODO fields then run `bespin jobs create {}` .".format(outfile.name))

    def create_job(self, infile, dry_run):
        """
        Create a job based on an input job file (possibly created via init_job)
        Prints out job id.
        :param infile: file: input file to use for creating a job
        :param dry_run: boolean: when True do not actually create a job just validate the input
        """
        api = self._create_api()
        job_file = JobFileLoader(infile).create_job_file()
        if dry_run:
            job_file.verify_job(api)
            print("Job file is valid.")
        else:
            job = job_file.create_job(api)
            job_id = job['id']
            print("Created job {}".format(job_id))
            print("To start this job run `bespin jobs start {}` .".format(job_id))

    def start_job(self, job_id, token=None):
        """
        Start a job with optional authorization token
        :param job_id: int: id of the job to start
        :param token: str: token to use to authorize running the job
        """
        api = self._create_api()
        if token:
            api.authorize_job(job_id, token)
            print("Set run token for job {}".format(job_id))
        api.start_job(job_id)
        print("Started job {}".format(job_id))

    def cancel_job(self, job_id):
        """
        Cancel a running job
        :param job_id: int: id of the job to cancel
        """
        api = self._create_api()
        api.cancel_job(job_id)
        print("Canceled job {}".format(job_id))

    def restart_job(self, job_id):
        """
        Restart a non-running job
        :param job_id: int: id of the job to restart
        """
        api = self._create_api()
        api.restart_job(job_id)
        print("Restarted job {}".format(job_id))

    def delete_job(self, job_id):
        """
        Delete a job
        :param job_id: int: id of the job to delete
        """
        api = self._create_api()
        api.delete_job(job_id)
        print("Deleted job {}".format(job_id))


class Table(object):
    """
    Used to display column headers and associated data as rows
    """
    def __init__(self, column_names, items):
        self.column_names = column_names
        self.items = items

    @staticmethod
    def _format_column_name(column_name):
        return column_name.replace("_", " ").title()

    def __str__(self):
        column_data = [[item[name] for name in self.column_names] for item in self.items]
        formatted_column_names = [self._format_column_name(name) for name in self.column_names]
        return tabulate(column_data, headers=formatted_column_names)


class WorkflowDetails(object):
    """
    Creates column data based on workflows/questionnaires
    """
    TAG_COLUMN_NAME = "version tag"

    def __init__(self, api, all_versions):
        self.api = api
        self.all_versions = all_versions
        self.column_names = ["id", "name", self.TAG_COLUMN_NAME]

    def get_column_data(self):
        """
        Return list of dictionaries of workflow data.
        :return: [dict]: one record for each questionnaire
        """
        data = []
        for workflow in self.api.workflows_list():
            if len(workflow['versions']):
                versions = workflow['versions']
                if not self.all_versions:
                    versions = versions[-1:]
                for version in versions:
                    for workflow_configuration in self.api.workflow_configurations_list(workflow_version=version):
                        workflow[self.TAG_COLUMN_NAME] = workflow_configuration['tag']
                        data.append(dict(workflow))
        return data


class JobsList(object):
    """
    Creates column data based on current users's jobs
    """
    def __init__(self, api):
        self.api = api
        self.column_names = ["id", "name", "state", "step", "last_updated", "elapsed_hours", "workflow_tag"]

    def get_column_data(self):
        """
        Return list of dictionaries of workflow data.
        :return: [dict]: one record for each questionnaire
        """
        data = []
        for job in self.api.jobs_list():
            job['elapsed_hours'] = self.get_elapsed_hours(job.get('usage'))
            job['workflow_tag'] = self.get_workflow_tag(job['workflow_version'])
            data.append(job)
        return data

    def get_workflow_tag(self, workflow_version):
        """
        Lookup the workflow tag for the specified workflow version
        :param workflow_version: int: workflow version id to lookup tag for
        :return: str: tag associated with workflow_version
        """
        configurations = self.api.workflow_configurations_list(workflow_version=workflow_version)
        return configurations[0]['tag']

    def get_elapsed_hours(self, usage):
        if usage:
            elapsed_hours = Decimal(usage.get('vm_hours'))
            # round to 1 decimal placec
            rounded_elapsed_hours = Decimal(elapsed_hours.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
            return float(rounded_elapsed_hours)
        return None


class JobFile(object):
    """
    Contains data for creating a job.
    """
    def __init__(self, workflow_tag, name, fund_code, job_order):
        """
        :param workflow_tag: str: questionnaire tag from bespin-api
        :param name: str: user name for the job
        :param fund_code: str: fund code to
        :param job_order: dict: job order details used with CWL workflow
        """
        self.workflow_tag = workflow_tag
        self.name = name
        self.fund_code = fund_code
        self.job_order = job_order

    def yaml_str(self):
        data = {
            'name': self.name,
            'fund_code': self.fund_code,
            'job_order': self.job_order,
            'workflow_tag': self.workflow_tag,
        }
        return yaml.dump(data, default_flow_style=False)

    def create_user_job_order(self):
        """
        Format job order replacing dds remote file paths with filenames that will be staged
        :return: dict: job order for running CWL
        """
        user_job_order = self.job_order.copy()
        formatter = JobOrderFormatFiles()
        formatter.walk(user_job_order)
        return user_job_order

    def get_dds_files_details(self):
        """
        Get dds files info based on job_order
        :return: [(dds_file, staging_filename)]
        """
        job_order_details = JobOrderFileDetails()
        job_order_details.walk(self.job_order)
        return job_order_details.dds_files

    def read_workflow_configuration(self, api):
        workflow_configurations = api.workflow_configurations_list(tag=self.workflow_tag)
        if workflow_configurations:
            return workflow_configurations[0]
        raise WorkflowConfigurationNotFoundException(
            "Unable to find workflow configuration for tag {}".format(self.workflow_tag)
        )

    def create_job(self, api):
        """
        Create a job using the passed on api
        :param api: BespinApi
        :return: dict: job dictionary returned from bespin api
        """
        dds_user_credential = api.dds_user_credentials_list()[0]
        workflow_configuration = self.read_workflow_configuration(api)
        stage_group = api.stage_group_post()
        dds_project_ids = set()
        sequence = 0
        for dds_file, path in self.get_dds_files_details():
            file_size = dds_file.current_version['upload']['size']
            api.dds_job_input_files_post(dds_file.project_id, dds_file.id, path, 0, sequence,
                                         dds_user_credential['id'], stage_group_id=stage_group['id'],
                                         size=file_size)
            sequence += 1
            dds_project_ids.add(dds_file.project_id)
        user_job_order = self.create_user_job_order()
        job = api.workflow_configurations_create_job(workflow_configuration['id'], self.name, self.fund_code,
                                                     stage_group['id'], user_job_order, None)
        dds_file_util = DDSFileUtil()
        for project_id in dds_project_ids:
            dds_file_util.give_download_permissions(project_id, dds_user_credential['dds_id'])
        return job

    def verify_job(self, api):
        self.read_workflow_configuration(api)  # workflow configuration must exist
        self.get_dds_files_details()  # DukeDS input files must exist
        self.create_user_job_order()  # verify that we can generate a job order


class JobFileLoader(object):
    """
    Creates JobFile based on an input file
    """
    def __init__(self, infile):
        self.data = yaml.load(infile)

    def create_job_file(self):
        self.validate_job_file_data()
        job_file = JobFile(workflow_tag=self.data['workflow_tag'],
                           name=self.data['name'],
                           fund_code=self.data['fund_code'],
                           job_order=self.data['job_order'])
        return job_file

    def validate_job_file_data(self):
        bad_fields = []
        for field_name in ['name', 'fund_code']:
            if self.data[field_name] in USER_PLACEHOLDER_VALUES:
                bad_fields.append(field_name)
        checker = JobOrderPlaceholderCheck()
        checker.walk(self.data['job_order'])
        bad_fields.extend(['job_order.{}'.format(key) for key in checker.keys_with_placeholders])
        if bad_fields:
            bad_fields.sort()
            bad_fields_str = ', '.join(bad_fields)
            error_msg = "Please fill in placeholder values for field(s): {}".format(bad_fields_str)
            raise IncompleteJobFileException(error_msg)


class JobConfiguration(object):
    """
    Creates a placeholder job file based on workflow_configuration
    """
    def __init__(self, workflow_configuration):
        self.workflow_configuration = workflow_configuration

    def create_job_file_with_placeholders(self):
        return JobFile(workflow_tag=self.workflow_configuration['tag'],
                       name=STRING_VALUE_PLACEHOLDER, fund_code=STRING_VALUE_PLACEHOLDER,
                       job_order=self.format_user_fields())

    def format_user_fields(self):
        user_fields = self.workflow_configuration['user_fields']
        formatted_user_fields = {}
        for user_field in user_fields:
            field_type = user_field.get('type')
            field_name = user_field.get('name')
            if isinstance(field_type, dict):
                if field_type['type'] == 'array':
                    value = self.create_placeholder_value(field_type['items'], is_array=True)
                else:
                    value = self.create_placeholder_value(field_type['type'], is_array=False)
            else:
                value = self.create_placeholder_value(field_type, is_array=False)
            formatted_user_fields[field_name] = value
        return formatted_user_fields

    def create_placeholder_value(self, type_name, is_array):
        if is_array:
            return [self.create_placeholder_value(type_name, is_array=False)]
        else:  # single item type
            placeholder = USER_PLACEHOLDER_DICT.get(type_name)
            if not placeholder:
                return STRING_VALUE_PLACEHOLDER
            return placeholder


class JobOrderWalker(object):
    def walk(self, obj):
        for key in obj.keys():
            self._walk_job_order(key, obj[key])

    def _walk_job_order(self, top_level_key, obj):
        if self._is_list_but_not_string(obj):
            return [self._walk_job_order(top_level_key, item) for item in obj]
        elif isinstance(obj, dict):
            if 'class' in obj.keys():
                self.on_class_value(top_level_key, obj)
            else:
                for key in obj:
                    self._walk_job_order(top_level_key, obj[key])
        else:
            # base object string or int or something
            self.on_simple_value(top_level_key, obj)

    @staticmethod
    def _is_list_but_not_string(obj):
        return isinstance(obj, list) and not isinstance(obj, str)

    def on_class_value(self, top_level_key, value):
        pass

    def on_simple_value(self, top_level_key, value):
        pass

    @staticmethod
    def format_file_path(path):
        """
        Create a valid file path based on a dds placeholder url
        :param path: str: format dds://<projectname>/<filepath>
        :return: str: file path to be used for staging data when running the workflow
        """
        if path.startswith(DUKEDS_PATH_PREFIX):
            return path.replace(DUKEDS_PATH_PREFIX, "dds_").replace("/", "_").replace(":", "_")
        return path


class JobOrderPlaceholderCheck(JobOrderWalker):
    def __init__(self):
        self.keys_with_placeholders = set()

    def on_class_value(self, top_level_key, value):
        if value['class'] == 'File':
            path = value.get('path')
            if path and path in USER_PLACEHOLDER_VALUES:
                self.keys_with_placeholders.add(top_level_key)

    def on_simple_value(self, top_level_key, value):
        if value in USER_PLACEHOLDER_VALUES:
            self.keys_with_placeholders.add(top_level_key)


class JobOrderFormatFiles(JobOrderWalker):
    def on_class_value(self, top_level_key, value):
        if value['class'] == 'File':
            path = value.get('path')
            if path:
                value['path'] = self.format_file_path(path)


class JobOrderFileDetails(JobOrderWalker):
    def __init__(self):
        self.dds_file_util = DDSFileUtil()
        self.dds_files = []

    def on_class_value(self, top_level_key, value):
        if value['class'] == 'File':
            path = value.get('path')
            if path and path.startswith(DUKEDS_PATH_PREFIX):
                dds_file = self.dds_file_util.find_file_for_path(path)
                self.dds_files.append((dds_file, self.format_file_path(path)))
