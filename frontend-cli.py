import os
import subprocess

# paths to generic config files
jenkinsfile_path = "https://raw.githubusercontent.com/jmason-va/angular-seed/master/jenkinsfile"
tasks_path = "https://raw.githubusercontent.com/jmason-va/angular-seed/master/tasks.py"
app_yaml = "https://raw.githubusercontent.com/jmason-va/angular-seed/master/app.yaml"
angular_cli_json = "https://raw.githubusercontent.com/vendasta/marketplace-public-store/master/.angular-cli.json?token=AQecjDCTZC1Jou_uR_m6lImwgRT-0yv4ks5ZqcF_wA%3D%3D"
styles = "https://raw.githubusercontent.com/jmason-va/angular-seed/master/src/styles.scss"
readme = "https://raw.githubusercontent.com/jmason-va/angular-seed/master/README.md"

# color terminal output
GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'


def get_file(path, filename):
  """takes a path to a github raw page and outputs a file"""
  os.system('curl {} -o "{}"'.format(path, filename))


def generate_config_files(project_name, parent_project_name):
  """generates vendasta config needed for a frontend microservice"""
  ls_output = subprocess.check_output('ls')

  get_file(jenkinsfile_path, "jenkinsfile")                             # generate a generic angular jenkinsfile
  replace_in_file('jenkinsfile', 'angular-seed', project_name)          # update the label to include the project name
  os.system('mv jenkinsfile {}'.format(project_name))                   # move the jenkinsfile into the base directory

  get_file(tasks_path, "tasks.py")                                      # generate a generic angular tasks file
  replace_in_file('tasks.py', '<base-project>', parent_project_name)    # configure which application this service deploys to
  os.system('mv tasks.py {}'.format(project_name))                      # move the tasks file into the base directory

  get_file(app_yaml, "app.yaml")                                        # generate a generic app.yaml file
  replace_in_file('app.yaml', 'angular-seed', project_name)             # configure the service name
  os.system('mv app.yaml {}'.format(project_name))                      # move the app.yaml file into the base directory
  
  replace_in_file('{}/.angular-cli.json'.format(project_name), 'css', 'scss')              # configure project to use scss by default
  replace_in_file('{}/.angular-cli.json'.format(project_name), 'dist', 'target')           # output do target folder instead of dist

  os.system('rm {}/README.md'.format(project_name))                     # remove cli readme
  get_file(readme, "README.md")                                         # generate basic readme
  os.system('mv README.md {}'.format(project_name))                     # move basic readme into base folder

  get_file(styles, "styles.scss")                                       # get basic styles
  os.system('mv styles.scss {}/src'.format(project_name))               # move styles.scss to the src
  os.system('rm {}/src/styles.css'.format(project_name))                # remove the auto generated styles.css file

  app_module_path = '{}/src/app/app.module.ts'.format(project_name)
  replace_in_file(app_module_path, """import { NgModule } from '@angular/core';""",         # add material import to app.module
"""import { NgModule } from '@angular/core';
import { MaterialModule } from '@angular/material';
""")  
  replace_in_file(app_module_path, 'imports: [', 'imports: [ MaterialModule,')              

  package_json_path = '{}/package.json'.format(project_name)                                # add deps to package json
  replace_in_file(package_json_path, '"dependencies": {', '"dependencies": { \n    "@angular/material": "2.0.0-beta.3",')
  
  clear_file('{}/src/app/app.component.html'.format(project_name),                          # clear app.component
  '<div style="text-align: center; padding: 20px;">add components and routes</div>\n<router-outlet></router-outlet>')
  

def generate_full_project(project_name, parent_project_name):
  """generate a project from scratch"""
  print '\n{}generating new angular project {}{}\n'.format(GREEN, project_name, END)
  os.system('ng new {} --routing'.format(project_name))

  print '\n{}generating vendasta config for {}{}\n'.format(GREEN, project_name, END)
  generate_config_files(project_name, parent_project_name)

  print '\n{}Add routing in {} to your new microservice at https://github.com/vendasta/{}/blob/master/src/dispatch.yaml {}\n'.format(GREEN, parent_project_name, parent_project_name, END)

def replace_in_file(file_name, to_replace, replacement):
  # Read in the file
  with open(file_name, 'r') as file :
    filedata = file.read()
  # Replace the target string
  filedata = filedata.replace(to_replace, replacement)
  # Write the file out again
  with open(file_name, 'w') as file:
    file.write(filedata)

def clear_file(file_name, text=''):
  # Read in the file
  with open(file_name, 'r') as file :
    filedata = file.read()
  # Write the file out again with the text
  with open(file_name, 'w') as file:
    file.write(text)

def main():
  print "\nThis will generate a angular project from the standard-cli."
  print "It will also generate the Vendasta config needed for a frontend microservice."
  print "{}warning: this will fail if you do not have the angular-cli installed on your machine.\n{}".format(RED, END)

  project_name = raw_input("enter a project name: ")
  parent_project_name = raw_input("enter the project that will serve this module: ")
  generate_full_project(project_name, parent_project_name)

main()