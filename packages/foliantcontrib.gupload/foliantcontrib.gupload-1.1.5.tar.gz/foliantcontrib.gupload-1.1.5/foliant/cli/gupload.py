'''CLI extension for the ``gupload`` command.'''

import os
from cliar import set_arg_map, set_metavars, set_help, ignore
from pathlib import Path
import webbrowser

from foliant.cli import make
from foliant.cli.base import BaseCli
from foliant.config import Parser
from foliant.utils import spinner

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Cli(BaseCli):
    def _gdrive_auth(self):
        if not self._gdoc_config['com_line_auth']:
            self._gdoc_config['com_line_auth'] = False

        gauth = GoogleAuth()

        if self._gdoc_config['com_line_auth']:
            gauth.CommandLineAuth()
            self._gdrive = GoogleDrive(gauth)
        else:
            if True:  # 'False' while debugging to reduce amount of new tabs
                gauth.LocalWebserverAuth()
                self._gdrive = GoogleDrive(gauth)
            else:
                gauth.LoadCredentialsFile('client_creds.txt')

                if gauth.credentials is None:
                    gauth.LocalWebserverAuth()
                elif gauth.access_token_expired:
                    gauth.Refresh()
                else:
                    gauth.Authorize()

                gauth.SaveCredentialsFile('client_creds.txt')
                self._gdrive = GoogleDrive(gauth)

    def _create_gdrive_folder(self):

        if not self._gdoc_config['gdrive_folder_name']:
            self._gdoc_config['gdrive_folder_name'] = 'Foliant upload'

        if not self._gdoc_config['gdrive_folder_id']:
            folder = self._gdrive.CreateFile({'title': self._gdoc_config['gdrive_folder_name'], 'mimeType': 'application/vnd.google-apps.folder'})
            folder.Upload()
            self._gdoc_config['gdrive_folder_id'] = folder['id']

    def _upload_file(self, target):
        if self._gdoc_config['gdoc_title']:
            title = self._gdoc_config['gdoc_title']
        else:
            title = self._filename

        if target == 'docx':
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif target == 'pdf':
            mimetype = 'application/pdf'
        elif target == 'tex':
            mimetype = 'application/x-latex'
        else:
            mimetype = 'application/vnd.google-apps.document'

        if self._gdoc_config['gdoc_id']:
            upload_file = self._gdrive.CreateFile({'title': title, 'id': self._gdoc_config['gdoc_id'], 'parents': [{'id': self._gdoc_config['gdrive_folder_id']}], 'mimeType': mimetype})
        else:
            upload_file = self._gdrive.CreateFile({'title': title, 'parents': [{'id': self._gdoc_config['gdrive_folder_id']}], 'mimeType': mimetype})

        if self._gdoc_config['convert_file']:
            convert = self._gdoc_config['convert_file']
        else:
            convert = False

        upload_file.SetContentFile('/'.join((os.getcwd(), f'{self._filename}')))
        upload_file.Upload(param={'convert': convert})

        self._gdoc_config['gdoc_id'] = upload_file['id']
        self._gdoc_link = upload_file['alternateLink']

        webbrowser.open(self._gdoc_link)

    @set_arg_map({'backend': 'with', 'project_path': 'path', 'config_file_name': 'config'})
    @set_metavars({'target': 'TARGET', 'backend': 'BACKEND'})
    @set_help(
        {
            'target': 'Target format: pdf, docx, html, etc.',
            'backend': 'Backend to make the target with: Pandoc, MkDocs, etc.',
            'project_path': 'Path to the Foliant project',
            'config_file_name': 'Name of config file of the Foliant project',
            'quiet': 'Hide all output accept for the result. Useful for piping.',
            'keep_tmp': 'Keep the tmp directory after the build.',
            'debug': 'Log all events during build. If not set, only warnings and errors are logged.'
        }
    )
    def gupload(
            self,
            target,
            backend='',
            project_path=Path('.'),
            config_file_name='foliant.yml',
            quiet=False,
            keep_tmp=False,
            debug=False
        ):

        file_to_upload = make.Cli()
        self._filename = file_to_upload.make(target, backend, project_path, config_file_name, quiet, keep_tmp, debug)

        print('─────────────────────')

        self._gdoc_config = file_to_upload.get_config(project_path, config_file_name, quiet=True)['gupload']

        self._gdrive_auth()

        with spinner(f"Uploading '{self._filename}' to Google Drive", self.logger, quiet=False, debug=False):
            try:
                self._create_gdrive_folder()
                self._upload_file(target)

            except Exception as exception:
                raise type(exception)(f'The error occurs: {exception}')

        if self._gdoc_link:
            self.logger.info(f'File {self._filename} uploaded to Google Drive: {self._gdoc_link}')

            if not quiet:
                print('─────────────────────')
                print(f"Result:\n\
Doc link: {self._gdoc_link}\n\
Google drive folder ID: {self._gdoc_config['gdrive_folder_id']}\n\
Google document ID: {self._gdoc_config['gdoc_id']}")

            return self._gdoc_link

        else:
            self.logger.critical('Upload failed')
            exit('Upload failed')
            return None
