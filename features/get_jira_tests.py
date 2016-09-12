import optparse
import os

BEHAVE_SERVER = "https://behave.pro"
USER = "amlyYTphNzNkNDNjNC01OTM2LTQzYTItYTUxZS02MTY0OGY5OTcxZTk="
PASSWORD = "6ce0f5fd7b3c8b9ac277f68a7b058c0c143bc7af"

parser = optparse.OptionParser()
parser.add_option('-p', '--project',
                  dest="project",
                  help="Project ID in JIRA from the scenarios will be extracted",
                  )
parser.add_option('-a', '--only_automated',
                  dest="only_automated",
                  default=False,
                  action="store_true",
                  help="Only retrieve automated testcases",
                  )
parser.add_option('-d', '--directory',
                  dest="directory",
                  default="behave_pro_jira",
                  help="Output directory to place the features files containing the scenarios",
                  )
options, remainder = parser.parse_args()

if options.project == None or options.directory == None:
    parser.error("Error: project and directory params are mandatory")
    parser.print_help()

command = "behave-cli {behave_server} {project} -u {user} -p {password} -d {directory} --verify".format(behave_server=BEHAVE_SERVER, project=options.project, user=USER, password=PASSWORD, directory=options.directory)
if options.only_automated == False:
    command = command + " -m"

os.system(command)