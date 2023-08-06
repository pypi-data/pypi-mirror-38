import os
import sys
import yaml
import jenkins
import json
from tabulate import tabulate

#sys.path.append("..")

try:
    from ctlcore import ctlCore
except ImportError:
    from .ctlcore import ctlCore

class pyjenkins:
   
    server = ''
    URL = ''
    username = ''    
    version = ''

    option_dist = {
        "freestyle" : ["hudson.model.FreeStyleProject"], 
        "maven" : ["hudson.maven.MavenModuleSet"], 
        "pipeline" : ["org.jenkinsci.plugins.workflow.job.WorkflowJob", "org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject"],
        "folders" : ["com.cloudbees.hudson.plugins.folder.Folder"],
        "matrix" : ["hudson.matrix.MatrixProject"],
        "org" : ["jenkins.branch.OrganizationFolder"]
    }
    non_jobs_list = [ 
	"com.cloudbees.hudson.plugins.folder.Folder",
	"com.cloudbees.hudson.plugins.modeling.impl.builder.BuilderTemplate",
	"com.cloudbees.hudson.plugins.modeling.impl.jobTemplate.JobTemplate"
	]

    def __init__(self):
        ctl = ctlCore()
        if ctl.validate_context():
            try:
                self.server = jenkins.Jenkins(ctl.cURL, username=ctl.cUser, password=ctl.cToken)
                self.username = self.server.get_whoami()["fullName"]
                self.version = self.server.get_version()
                self.URL = ctl.cURL                
            except Exception as e:
                print(e)
                exit()
        else:
            print("Please validate the Jenkins Context before proceeding...")
            exit()
    
    def info(self):                
        info_list = [["URL", self.URL], ["Version", self.version], ["User", self.username]]
        print(tabulate(info_list, headers=['Jenkins', 'Description'], tablefmt='orgtbl'))       

    # jxcore - Job functions
    def list_all_jobs(self):
        jobs_list = []
        jobs = self.server.get_all_jobs(folder_depth=None, folder_depth_per_request=50)
        for job_item in jobs:                        
            if( job_item["_class"] not in self.non_jobs_list ):
                jobs_list.append([job_item["name"], job_item["url"]])
        print(tabulate(jobs_list, headers=['Name', 'URL'], tablefmt='orgtbl'))     
    
    def jobs_count_all(self):
        jobs_list = []
        jobs = self.server.get_all_jobs(folder_depth=None, folder_depth_per_request=50)
        for job_item in jobs:                        
            if( job_item["_class"] not in self.non_jobs_list ):
                jobs_list.append([job_item["_class"], job_item["url"]])
        print(len(jobs_list))

    def list_jobs(self, option):
        jobs = self.server.get_all_jobs(folder_depth=None, folder_depth_per_request=50)
        jobs_list = []
        if option == "freestlye":
            for item in jobs:
                if(item["_class"] == "hudson.model.FreeStyleProject"):
                    jobs_list.append([item["_class"], item["url"]])        
        elif option == "maven":
            for item in jobs:
                if(item["_class"] == "hudson.maven.MavenModuleSet"):
                    jobs_list.append([item["_class"], item["url"]])
        elif option == "pipeline":
            for item in jobs:
                if(item["_class"] == "org.jenkinsci.plugins.workflow.job.WorkflowJob" or item["_class"] == "org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject"):
                    jobs_list.append([item["_class"], item["url"]])
        elif option == "matrix":
            for item in jobs:
                if(item["_class"] == "hudson.matrix.MatrixProject"):
                    jobs_list.append([item["_class"], item["url"]])
        elif option == "matrix":
            for item in jobs:
                if(item["_class"] == "hudson.matrix.MatrixProject"):
                    jobs_list.append([item["_class"], item["url"]])
        elif option == "org":
            for item in jobs:
                if(item["_class"] == "jenkins.branch.OrganizationFolder"):
                    jobs_list.append([item["_class"], item["url"]])
        elif option == "folders":
            for item in jobs:
                if(item["_class"] == "com.cloudbees.hudson.plugins.folder.Folder"):
                    jobs_list.append([item["_class"], item["url"]])
        print(tabulate(jobs_list, headers=['Name', 'URL'], tablefmt='orgtbl')) 
    
    def jobs_count(self, option_list):
        jobs_list = []
        jobs = self.server.get_all_jobs(folder_depth=None, folder_depth_per_request=50)
        for item in option_list:
            for job_item in jobs:                        
                if(job_item["_class"] in self.option_dist[item]):
                    jobs_list.append([job_item["_class"], job_item["url"]])
        print(tabulate([[len(jobs_list)]], headers=['No. of Jobs'], tablefmt='orgtbl'))

    # jxcore - Plugin functions
    def list_all_plugins(self):
        plugins = self.server.get_plugins_info()
        plugins_list = []
        for item in plugins:
            plugins_list.append([item["longName"], item["version"]])
        print(tabulate(plugins_list, headers=['Plugin Name', 'Version'], tablefmt='orgtbl'))          

    def plugins_count(self):
        plugins = self.server.get_plugins_info()
        print(tabulate([[len(plugins)]], headers=['No. of Plugins'], tablefmt='orgtbl'))