import os
import sys
import click
import yaml

#sys.path.append("..")

from pyfiglet import Figlet 
try:
    from jxcore import pyjenkins
    from ctlcore import ctlCore
except ImportError:
    from .jxcore import pyjenkins
    from .ctlcore import ctlCore

__author__="Deepan"

@click.group()
def main():
    """
    Jenkins Control Command to interact with your Jenkins Instance    
    """
    pass

@main.command()
def info():
    """
    Show the infomation about your Jenkins Context
    """
    f = Figlet(font='smslant')    
    click.echo(f.renderText('jxctl'))
    pyjenkins().info()

@main.group()
def context():
    pass

@main.group()
def get():
    pass

#pujxctl - context group
@context.command()
@click.option('--url', type=str)
@click.option('--user', type=str)
@click.option('--token', type=str, nargs=1)
@click.option('--name', type=str)
def set(url, user, token, name):
    """
    Set Jenkins Context
    """   
    ctlCore().set_context(url, user, token, name)
    

@context.command()
def show():
    ctlCore().show_current_context()

#pujxctl - get group

@get.command()
@click.option('--count', is_flag=True)
@click.option('--all', is_flag=True)
@click.option('--maven', is_flag=True)
@click.option('--freestyle', is_flag=True)
@click.option('--pipeline', is_flag=True)
@click.option('--matrix', is_flag=True)
@click.option('--folders', is_flag=True)
@click.option('--org', is_flag=True)
def jobs(count, all, maven, freestyle, pipeline, matrix, folders, org):
    """
    List Jobs of your Jenkins Context
    """
    if(count):
        if(not all):
            option_dist = { "maven" : maven, "freestyle" : freestyle, "pipeline" : pipeline, "matrix" : matrix, "folders" : folders, "org" : org}        
            option_list = []
            for item in option_dist:
                if(option_dist[item]):
                    option_list.append(item)
            pyjenkins().jobs_count(option_list)
        else:
            pyjenkins().jobs_count_all()
    elif(all):
        pyjenkins().list_all_jobs()    
    elif(freestyle):
        pyjenkins().list_jobs("freestlye")
    elif(maven):
        pyjenkins().list_jobs("maven")
    elif(pipeline):
        pyjenkins().list_jobs("pipeline")
    elif(matrix):
        pyjenkins().list_jobs("matrix")
    elif(folders):
        pyjenkins().list_jobs("folders")
    elif(org):
        pyjenkins().list_jobs("org")
    else: 
        pass

@get.command()
@click.option('--count', is_flag=True)
def plugins(count):
    """
    List all installed plugins of your Jenkins Context
    """
    if(count):
        pyjenkins().plugins_count()
    else:
        pyjenkins().list_all_plugins()

def init():
    default_config_file = """
    current-context: 
    context: 
        url: 
        user: 
        token: 
        name: 
    """
    user_home = os.path.expanduser('~')
    if not os.path.isdir(user_home+"/.jxctl"):
        os.mkdir(user_home+"/.jxctl")
    config_file = user_home+"/.jxctl/config"
    if not os.path.isfile(config_file):
        with open(config_file, 'w') as yaml_file:
            yaml.dump(yaml.load(default_config_file), yaml_file, default_flow_style=False)

if __name__ == '__main__':
    init()
    main()

def start():
    init()
    main()