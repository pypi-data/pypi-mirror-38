from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from pybis import Openbis
import numpy as np

import json
import os
import urllib
from urllib.parse import unquote, unquote_plus
from subprocess import check_output
from urllib.parse import urlsplit, urlunsplit
import yaml

openbis_connections = {}


def _jupyter_server_extension_paths():
    return [{'module': 'jupyter-openbis-extension.server'}]

def _load_configuration(filename='openbis-connections.yaml'):
    
    home = os.path.expanduser("~")
    abs_filename = os.path.join(home, '.jupyter', filename)

    with open(abs_filename, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLexception as exc:
            print(exc)
            return None
        

def load_jupyter_server_extension(nb_server_app):
    """Call when the extension is loaded.
    :param nb_server_app: Handle to the Notebook webserver instance.
    """

    # load the configuration file
    config = _load_configuration()
    if config is not None:
        for conn in config['connections']:
            try:
                register_connection(conn)
            except Exception as exc:
                print(exc)
            

    web_app = nb_server_app.web_app
    host_pattern = '.*$'

    base_url = web_app.settings['base_url']

    web_app.add_handlers(
        host_pattern, 
        [(url_path_join(
            base_url,
            '/openbis/dataset/(?P<connection_name>.*)?/(?P<permId>.*)?/(?P<downloadPath>.*)'), 
            DataSetDownloadHandler
        )]
    ) 
    web_app.add_handlers( host_pattern, [(
            url_path_join(
                base_url,
                '/openbis/dataset/(?P<connection_name>.*)'
            ),
            DataSetUploadHandler
        )]
    ) 
    web_app.add_handlers(
        host_pattern, 
        [(  
            url_path_join(
                base_url,
                '/openbis/sample/(?P<connection_name>.*)?/(?P<permId>.*)'
            ), 
            SampleHandler
        )]
    ) 
    web_app.add_handlers(
        host_pattern, 
        [(
            url_path_join(base_url, '/openbis/conn'), 
            OpenBISHandler
        )]
    )

    print("pybis loaded: {}".format(Openbis))


def register_connection(connection_info):
    
    conn = OpenBISConnection(
        name           = connection_info['name'],
        url            = connection_info['url'],
        verify_certificates = connection_info['verify_certificates'],
        username       = connection_info['username'],
        password       = connection_info['password'],
        status         = 'not connected',
    )
    openbis_connections[conn.name] = conn

    try:
        openbis = Openbis(
            url = conn.url,
            verify_certificates = conn.verify_certificates
        )
        conn.openbis = openbis

        openbis.login(
            username = conn.username,
            password = conn.password
        )
        conn.status  = 'connected'
        print('connected to {}'.format(conn.name))
    except Exception as exc:
        conn.status  = 'FAILED: {}'.format(exc)
        print('ERROR: could not connected to {}. Reason: {}'.format(conn.name, exc))

        raise exc


def check_connection(connection_name):
    """Checks whether connection is valid and session is still active
    and tries to reconnect, if possible. Returns the active session
    """
    
    if connection_name not in openbis_connections:
        return None
        
    conn = openbis_connections[connection_name]
    if not conn.openbis.isSessionActive():
        conn.openbis.login(conn.username, conn.password)
         

class OpenBISConnection:
    """register an openBIS connection
    """

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def is_session_active(self):
        return self.openbis.is_session_active()

    def reconnect(self):
        self.openbis.login(self.username, self.password)


class OpenBISHandler(IPythonHandler):
    """Handle the requests to /openbis/conn
    """

    def get(self):
        """returns all available openBIS connections
        """
        connections= []
        for conn in openbis_connections.values():
            connections.append({
                'name'   : conn.name,
                'url'    : conn.url,
                'status' : conn.status,
            })

        self.write({
            'status'     : 200,
            'connections': connections,
            'cwd'        : os.getcwd()
        })
        return

class SampleHandler(IPythonHandler):
    """Handle the requests for /openbis/sample/connection/permId"""

    def get_datasets(self, conn, permId):
        if not conn.is_session_active():
            try:
                conn.reconnect()
            except Exception as exc:
                print(exc)
                self.send_error(
                    reason = 'connection to {} could not be established: {}'.format(conn.name, exc)
                )

        sample = None
        try:
            sample = conn.openbis.get_sample(permId)
        except Exception as exc:
            print(exc) 
            self.send_error( reason = 'No such sample found: {}'.format(permId) )

        datasets = sample.get_datasets().df
        datasets.replace({np.nan:None}, inplace=True)  # replace NaN with None, otherwise we cannot convert it correctly
        return datasets.to_dict(orient='records')   # is too stupid to handle NaN


    def get(self, **params):
        """Handle a request to /openbis/sample/connection_name/permId
        download the data and return a message
        """
        try:
            conn = openbis_connections[params['connection_name']]
        except KeyError:
            self.send_error(
                reason = 'connection {} was not found'.format(params['connection_name'])
            )
        
        datasets = self.get_datasets(conn, params['permId'])
        if datasets is not None:
            self.set_status(200)
            self.write({
                "dataSets": datasets
            })



class DataSetDownloadHandler(IPythonHandler):
    """Handle the requests for /openbis/dataset/connection/permId"""


    def download_data(self, conn, permId, downloadPath=None):
        if not conn.is_session_active():
            try:
                conn.reconnect()
            except Exception as exc:
                self.send_error(
                    reason = 'connection to {} could not be established: {}'.format(conn.name, exc)
                )
                return

        try:
            dataset = conn.openbis.get_dataset(permId)
        except Exception as exc:
            self.send_error(
                reason = 'No such dataSet found: {}'.format(permId)
            )
            return

        # dataset was found, download the data to the disk
        try: 
            destination = dataset.download(destination=downloadPath)
        except Exception as exc:
            self.send_error(
                reason = 'Data for DataSet {} could not be downloaded: {}'.format(permId, exc)
            )
            return
            
        # return success message
        path = os.path.join(downloadPath, dataset.permId)
        self.write({
            'permId'    : dataset.permId,
            'path'      : path,
            'dataStore' : dataset.dataStore,
            'location'  : dataset.physicalData.location,
            'size'      : dataset.physicalData.size,
            'statusText': 'Data for DataSet {} was successfully downloaded to: {}.'.format(dataset.permId, path)
        })

    def get(self, **params):
        """Handle a request to /openbis/dataset/connection_name/permId
        download the data and return a message
        """

        try:
            conn = openbis_connections[params['connection_name']]
        except KeyError:
            self.send_error(
                reason = 'connection {} was not found'.format(params['connection_name'])
            )
            return
        
        results = self.download_data(conn=conn, permId=params['permId'], downloadPath=params['downloadPath'])


class DataSetUploadHandler(IPythonHandler):
    """Handle the requests for /openbis/dataset/connection"""


    def upload_data(self, conn, data):
        if not conn.is_session_active():
            try:
                conn.reconnect()
            except Exception as exc:
                self.send_error(
                    reason = 'connection to {} could not be established: {}'.format(conn.name, exc)
                )
                return

        try:
            sample = conn.openbis.get_sample(data.get('sampleIdentifier'))
        except Exception as exc:
            self.send_error(
                reason = 'No such sample found: {}'.format(data.get('sampleIdentifier'))
            )
            return

        filenames = []
        for filename in data.get('files'):
            filename = unquote(filename)
            filenames.append(filename)

        try: 
            ds = conn.openbis.new_dataset(
                name        = data.get('name'),
                description = data.get('description'),
                type        = data.get('type'),
                sample      = sample,
                files       = filenames
            ) 
        except Exception as exc:
            self.send_error(
                reason = 'Error while creating the dataset: {}'.format(exc)
            )
            return

        try:
            ds.save()
        except Exception as exc:
            self.send_error(
                reason = 'Error while saving the dataset: {}'.format(exc)
            )
            return
        
            
        # return success message
        self.write({
            'status': 200,
            'statusText': 'Jupyter Notebook was successfully uploaded to: {} with permId: {}'.format(conn.name, ds.permId)
        })

    def post(self, **params):
        """Handle a request to /openbis/dataset/connection_name/permId
        download the data and return a message
        """

        try:
            conn = openbis_connections[params['connection_name']]
        except KeyError:
            self.send_error(
                reason = 'connection {} was not found'.format(params['connection_name'])
            )
            return

        data = self.get_json_body()
        results = self.upload_data(conn=conn,data=data)
