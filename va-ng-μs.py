#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

# project to take the config from
project_path = "https://raw.githubusercontent.com/jmason-va/angular-seed/master"

# paths to generic config files
jenkinsfile = "{}/jenkinsfile".format(project_path)
tasks = "{}/tasks.py".format(project_path)
app_yaml = "{}/app.yaml".format(project_path)
angular_cli_json = "{}/.angular-cli.json".format(project_path)
styles = "{}/src/styles.scss".format(project_path)
karma = "{}/karma.conf.js".format(project_path)
readme = "{}/README.md".format(project_path)
polyfills = "{}/src/polyfills.ts".format(project_path)

# color terminal output
GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'


def get_file(path, filename):
    """takes a path to a github raw page and outputs a file"""
    os.system('curl {} -o "{}"'.format(path, filename))


def jenkins_config(project_name):
    """configuration"""
    print '\n{}configuring jenkinsfile{}'.format(GREEN, END)
    get_file(jenkinsfile, "jenkinsfile")  # generate a generic angular jenkinsfile
    replace_in_file('jenkinsfile', 'angular-seed', project_name)  # update the label to include the project name
    os.system('mv jenkinsfile {}'.format(project_name))  # move the jenkinsfile into the base directory


def tasks_config(project_name, parent_project_name):
    """configuration"""
    print '\n{}configuring tasks.py{}'.format(GREEN, END)
    get_file(tasks, "tasks.py")  # generate a generic angular tasks file
    replace_in_file('tasks.py', '<base-project>',
                    parent_project_name)  # configure which application this service deploys to
    os.system('mv tasks.py {}'.format(project_name))  # move the tasks file into the base directory


def app_yaml_config(project_name):
    """configuration"""
    print '\n{}configuring app.yaml{}'.format(GREEN, END)
    get_file(app_yaml, "app.yaml")  # generate a generic app.yaml file
    replace_in_file('app.yaml', 'angular-seed', project_name)  # configure the service name
    os.system('mv app.yaml {}'.format(project_name))  # move the app.yaml file into the base directory


def karma_config(project_name):
    """configuration"""
    print '\n{}installing and configuring the karma test runner{}'.format(GREEN, END)
    os.system('npm --prefix {} install --save-dev karma-phantomjs-launcher '.format(
        project_name))  # install phantomjs launcher for tests
    os.system('npm --prefix {} install --save intl'.format(project_name))  # install intl as a dep for phantomjs
    os.system('rm {}/karma.conf.js'.format(project_name))  # move the karma.conf.js file into the base directory
    get_file(karma, "karma.conf.js")
    os.system(
        'mv karma.conf.js {}/karma.conf.js'.format(project_name))  # move the karma.conf.js file into the base directory


def polyfill_config(project_name):
    """configuration"""
    print '\n{}configuring polyfills{}'.format(GREEN, END)
    os.system('rm {}/src/polyfills.ts'.format(project_name))  # move the polyfills file into the src directory
    get_file(polyfills, "polyfills.ts")  # generate a generic app.yaml file
    os.system('mv polyfills.ts {}/src'.format(project_name))  # move the app.yaml file into the base directory


def readme_config(project_name):
    """configuration"""
    print '\n{}updating readme{}'.format(GREEN, END)
    os.system('rm {}/README.md'.format(project_name))  # remove cli readme
    get_file(readme, "README.md")  # generate basic readme
    os.system('mv README.md {}'.format(project_name))  # move basic readme into base folder


def styles_config(project_name):
    """configuration"""
    print '\n{}adding basic styles{}'.format(GREEN, END)
    os.system('rm {}/src/styles.css'.format(project_name))  # remove styles.css file
    get_file(styles, "styles.scss")  # get basic styles
    os.system('mv styles.scss {}/src'.format(project_name))  # move styles.scss to the src


def angular_cli_config(project_name):
    """configuration"""
    print '\n{}updating default styling {}'.format(GREEN, END)
    replace_in_file('{}/.angular-cli.json'.format(project_name), 'css',
                    'scss')  # configure project to use scss by default
    replace_in_file('{}/.angular-cli.json'.format(project_name), 'dist',
                    'target')  # output do target folder instead of dist


def angular_material_config(project_name):
    """configuration"""
    print '\n{}adding material to project{}'.format(GREEN, END)
    app_module_path = '{}/src/app/app.module.ts'.format(project_name)
    replace_in_file(app_module_path, """import { NgModule } from '@angular/core';""",
                    # add material import to app.module
                    "import { NgModule } from '@angular/core';\nimport { MaterialModule } from '@angular/material';")
    replace_in_file(app_module_path, 'imports: [', 'imports: [ MaterialModule,')


def package_json_config(project_name):
    """configuration"""
    print '\n{}updating package.json{}'.format(GREEN, END)
    package_json_path = '{}/package.json'.format(project_name)  # add deps to package json
    replace_in_file(package_json_path, '"dependencies": {',
                    '"dependencies": { \n    "@angular/material": "2.0.0-beta.3",')
    #  having trouble installing this properly
    # os.system('npm --prefix {} install angular-material --save'.format(project_name))


def update_app_component(project_name):
    """configuration"""
    clear_file('{}/src/app/app.component.html'.format(project_name),  # clear app.component
               """
    <md-card style="text-align: center; margin: 30px auto; width: 3000px;">
      <img src="https://vbc-frontend.storage-download.googleapis.com/salesperson-details/vendasta_icon.png"/>
      <div>Welcome to your new angular microservice</div>
      <div style="font-size:10px;padding-top:20px;">va-ng-μs</div>
    </md-card>
    <router-outlet></router-outlet>
               """)


def update_default_specs(project_name):
    """configuration"""
    clear_file('{}/src/app/app.component.spec.ts'.format(project_name),
               """
    import { TestBed, async } from '@angular/core/testing';
    import { RouterTestingModule } from '@angular/router/testing';
    
    import { AppComponent } from './app.component';
    
    describe('sanity', () => {
      it('succeeds properly', () => {
          expect(true).toBe(true);
      });
    });
               """)


def generate_config_files(project_name, parent_project_name):
    """generate vendasta config"""
    jenkins_config(project_name)
    tasks_config(project_name, parent_project_name)
    app_yaml_config(project_name)
    polyfill_config(project_name)
    readme_config(project_name)
    styles_config(project_name)
    angular_cli_config(project_name)
    angular_material_config(project_name)
    package_json_config(project_name)
    update_app_component(project_name)
    update_default_specs(project_name)
    karma_config(project_name)


def generate_angular_cli_project(project_name, parent_project_name):
    """generate angular project using the cli"""
    print '\n{}generating new angular project {}{}'.format(GREEN, project_name, END)
    print '{}add routing in {} to your new microservice at https://github.com/vendasta/{}/blob/master/src/dispatch.yaml{}\n\n'.format(
        GREEN, parent_project_name, parent_project_name, END)
    os.system('ng new {} --routing'.format(project_name))


def replace_in_file(file_name, to_replace, replacement):
    # Read in the file
    with open(file_name, 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(to_replace, replacement)
    # Write the file out again
    with open(file_name, 'w') as file:
        file.write(filedata)


def clear_file(file_name, text=''):
    # Read in the file
    with open(file_name, 'r') as file:
        filedata = file.read()
    # Write the file out again with the text
    with open(file_name, 'w') as file:
        file.write(text)


def main():
    """main"""
    print "\nthis will generate a angular project from the standard-cli."
    print "it will also generate the Vendasta config needed for a frontend microservice."
    print "{}warning: angular-cli is required to run this script.{}".format(RED, END)
    print "{}see https://github.com/angular/angular-cli for more details.\n{}".format(RED, END)

    project_name = raw_input("enter a project name: ").strip()
    parent_project_name = raw_input("enter the project that will serve this module: ").strip()

    generate_angular_cli_project(project_name, parent_project_name)

    print '\n\n\n{}generating vendasta config for {}{}'.format(GREEN, project_name, END)
    generate_config_files(project_name, parent_project_name)

    print '\n\n\n{}installing node modules{}'.format(GREEN, END)
    os.system('npm --prefix {} install'.format(project_name))

    print '\n\n\n{}starting project{}'.format(GREEN, END)
    os.system('npm --prefix {} start'.format(project_name))


main()
