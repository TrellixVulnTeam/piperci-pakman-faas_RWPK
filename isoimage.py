import yaml
import sys
import os
import pathlib
import zipfile
import shutil
import tarfile
import errno


# Read YAML file
def main(argv):
    command_name = 'mkisofs'
    target_directory = 'target'

    if sys.version_info[0] != 3 or sys.version_info[1] < 6:
        print("This script requires Python version 3.6+")
        sys.exit(1)

    with open(argv[0]) as stream:
        if not (does_file_exists(argv[0])):
            print('Can not find Yaml File :'+sys.argv[1:])
            return 1
        if not is_tool(command_name):
            print('Command '+command_name+" Not Found on this system")
            return 1
        try:
            data_loaded = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return 1
        # print the read file
        print(" Statred Processing :"+sys.argv[1])
        # validate yaml file before processing
        validate_yaml_file(data_loaded)
        # print(data_loaded)
        mkdir_p(target_directory)

        # get_iso_package_name(data_loaded,packages);
        image_name = 'default.iso'
        # image_type = 'iso'
        structure = {}
        for row in data_loaded.get('packages'):
            if 'structure' in row:
                # image_name = row.get('name')
                # image_type = row.get('type')
                # print('Image name:', image_name)
                # print('Image type:', image_type)
                structure = row.get('structure')
                for files_row in structure.get('files'):
                    if 'file' in files_row:
                        file_name = files_row.get('file')
                        # unarhive = files_row.get('unarchive')
                        py = pathlib.Path().glob(file_name)
                        for file in py:
                            shutil.copy2(file, target_directory)
                for subdirs_row in structure.get('subdirs'):
                    process_subdir(subdirs_row, None)
        command_name += '  -V CDNAME -J -r -o '+image_name+' '
        command_name += target_directory
        print(" Generating Iso image", command_name)
        os.system(command_name)


def isNotValid(file_name):
    print("ERROR: File:"+file_name+'is not Valid')


def create_destination_directory(parent_dir, subdir):
    target_directory = 'target'
    # print('Subdirectory:',subdir)
    # print('Parent:',parent_dir)
    if(parent_dir is not None):
        destination = get_dest_dir_name(target_directory, parent_dir)
        destination = get_dest_dir_name(destination, subdir)
    else:
        destination = get_dest_dir_name(target_directory, subdir)
    mkdir_p(destination)
    return destination


def process_subdir(subdirs_row, parent_dir):
    subdir = subdirs_row.get('subdir')
    # print('Subdirectory1:',subdir)
    # print('Parent1:',parent_dir)
    destination = create_destination_directory(parent_dir, subdir)
    # print('destination1:',destination)
    if "subdirs" in subdirs_row:
        if(subdirs_row.get('subdirs') is not None):
            for sub_subdirs_row in subdirs_row.get('subdirs'):
                # print("Processing subdirs:"+sub_subdirs_row.get('subdir'))
                process_subdir(sub_subdirs_row, subdir)

    if 'files' in subdirs_row:
        for files_row in subdirs_row.get('files'):
            file_name = files_row.get('file')
            unarhive = files_row.get('unarchive')
            # print('Processsing file_name:',file_name)
            # print('should Unarchive:',unarhive)
            if unarhive:
                unarchive_file_to_destination(destination, file_name)
            else:
                # print('Copy file to destination')
                py = pathlib.Path().glob(file_name)
                for file in py:
                    shutil.copy2(file, destination)


def validate_subdir(subdirs_row):
    # print('Validating',subdirs_row)
    if "subdirs" in subdirs_row:
        if(subdirs_row.get('subdirs') is not None):
            for sub_subdirs_row in subdirs_row.get('subdirs'):
                # print('Validating',subdirs_row.get('subdirs'))
                validate_subdir(sub_subdirs_row)

    if 'files' in subdirs_row:
        for files_row in subdirs_row.get('files'):
            file_name = files_row.get('file')
            # print('Validating',file_name)
            if not does_file_exists(file_name):
                print("Does not found file:", file_name)
                sys.exit(1)


def validate_yaml_file(data_loaded):
    for row in data_loaded.get('packages'):
        if 'structure' in row:
            structure = row.get('structure')
            for files_row in structure.get('files'):
                if 'file' in files_row:
                    py = pathlib.Path().glob(files_row.get('file'))
                    for file in py:
                        # print('Checking file:',file)
                        if not does_file_exists(str(file)):
                            print("Does not found file:", (str(file)))
                            sys.exit(1)
                for subdirs_row in structure.get('subdirs'):
                    validate_subdir(subdirs_row)
        else:
            print(' The file should have structure element')
            sys.exit(1)


def unarchive_file_to_destination(destination, file_name):
    print('unarchive the files to destination:', destination)
    if (does_file_exists(file_name) and zipfile.is_zipfile(file_name)):
        extract_zip_file(file_name, destination)
    elif(does_file_exists(file_name) and tarfile.is_tarfile(file_name)):
        extract_tar_file(file_name, destination)
    else:
        isNotValid(file_name)


def does_file_exists(name):
    if os.path.exists(name):
        return True
    else:
        return False


def get_dest_dir_name(destination, subdir):
    return destination+str(os.sep)+subdir


def extract_zip_file(file_name, destination):
    zip_ref = zipfile.ZipFile(file_name, 'r')
    zip_ref.extractall(destination)
    zip_ref.close()


def extract_tar_file(file_name, destination):
    with tarfile.open(file_name) as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, path=destination)


def is_tool(name):
    """Check whether 'name' is on PATH."""
    from distutils.spawn import find_executable
    return find_executable(name) is not None


def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
