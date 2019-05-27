import yaml
import io
import sys
import subprocess
import os

# Read YAML file
def main(argv):
    commandName = 'mkisofs';

    
    with open(argv[0]) as stream:
        if not (does_file_exists(argv[0])):
            print('Can not find Yaml File :'+sys.argv[1:])
            return 1
        if not (is_tool(commandName)):
            print( 'Command '+commandName+" Not Found on this system");
            return 1
        try:
            data_loaded = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return 1
    # print the read file
    print(data_loaded)

def does_file_exists(name):
    if os.path.exists(name) and os.path.getsize(name) > 0:
        return True
    else:
        return False
        
def is_tool(name):
    """Check whether 'name' is on PATH."""

    from distutils.spawn import find_executable

    return find_executable(name) is not None

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))