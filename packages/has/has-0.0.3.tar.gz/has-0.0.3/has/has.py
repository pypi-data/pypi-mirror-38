#!/usr/bin/python3
import argparse
import sys
import hashlib
import os
from shutil import copyfile

__version__ = '0.0.3' # Release version

# Print to the terminal with different colors
green_color = '\033[92m'
red_color = '\033[91m'
end_color = '\033[0m'
def print_green(x): print(green_color + x + end_color)
def print_red(x): print(red_color + x + end_color)


def read_file_records(filename):
    ''' Read saved records from a snapshot file '''
    with open(filename, 'r') as f:
        file_records = f.readlines()
    return dict(file_record.strip('\n').split(':') for file_record in file_records)


def gen_file_records(path):
    ''' Get all of the file hashes under *path* '''
    def hash_file(filename):
        ''' Return a hash of the file contents '''
        with open(filename, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    for root, _, files in os.walk(path):
        for f in files: # Create a hash for all of the files under the path
            filename = root + '/' + f
            yield hash_file(filename), filename.replace(path + '/', '')


def create_snapshot_file(path, snapshot_filename):
    ''' Create a snapshot file named *filename* from the dataset at *path* '''
    with open(snapshot_filename, 'w') as f:
        for file_hash, filename in sorted(gen_file_records(path)):
            line = '%s:%s' % (file_hash, filename)
            print(line)
            f.write('%s\n' % line)
    

def recover_dataset(source_path, destination_path, snapshot_filename):
    ''' Copy files from source_path to destination_path according to the snapshot file '''
    source_file_records = {k:v for k,v in gen_file_records(source_path)}
    snapshot_file_records = read_file_records(snapshot_filename)
    for file_hash in set(source_file_records).intersection(snapshot_file_records):
        # Get filenames without full path
        source_filename = source_file_records[file_hash]
        snapshot_filename = snapshot_file_records[file_hash]

        # Add full paths to filenames
        src = './' + source_path + '/' + source_filename
        dst = './' + destination_path + '/' + snapshot_filename

        # Make sure file directory exists before copying the file
        if not os.path.exists(os.path.dirname(dst)):
            try:
                os.makedirs(os.path.dirname(dst))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        copyfile(src, dst)

    # Print files not found in backup directory
    print('Files not found in backup directory: ')
    for file_hash in (set(snapshot_file_records) - set(source_file_records)):
        print_red('%s:%s' % (file_hash, snapshot_file_records[file_hash])) 


def check_files(path, snapshot_filename):
    ''' Make sure all of the files under *path* are consistent with the snapshot '''
    existing_file_records = {k:v for k,v in gen_file_records(path)}
    snapshot_file_records = read_file_records(snapshot_filename)

    # Print files/hashes that have been added since the snapshot was created
    print('Files added/modified: ')
    for file_hash in (set(existing_file_records) - set(snapshot_file_records)):
        print_green('%s:%s' % (file_hash, existing_file_records[file_hash]))

    # Print files/hashes that have been removed since the snapshot was created
    print('Files removed/modified: ')
    for file_hash in (set(snapshot_file_records) - set(existing_file_records)):
        print_red('%s:%s' % (file_hash, snapshot_file_records[file_hash]))


def main():
    ''' Executed with *python has.py ...* '''
    # Input arguments to program
    parser = argparse.ArgumentParser(description='Create a hash array snapshot for recording your dataset state.')
    parser.add_argument('action', nargs='?', help='snap, recover, or check (e.g. \'has snap\')', default=None)
    parser.add_argument('-v', '--version', help='check version', action='store_true')
    parser.add_argument('-f', '--filename', help='name for the snapshot file (e.g. \'../snapshot.has\')')
    parser.add_argument('-d', '--directory', help='working directory')
    parser.add_argument('-b', '--backup', help='directory containing backup files')

    # Parse arguments received
    args = parser.parse_args()
    if True == args.version: print('has version %s' % __version__)
    if None == args.filename: args.filename = 'snapshot.has'
    if None == args.directory: args.directory = '.'
    if None == args.backup: args.backup = '.'

    if 'snap' == args.action: # Create snapshot file of current dataset
        create_snapshot_file(args.directory, args.filename)
    elif 'recover' == args.action: # Recover a dataset by using a snapshot
        if [] == os.listdir(args.directory):
            recover_dataset(args.backup, args.directory, args.filename)
        else: # User cannot recover to a directory that already has files
            print('Error. Recovery directory must be empty.')
    elif 'check' == args.action:
        check_files(args.directory, args.filename)
    else: parser.print_help()


if __name__=='__main__':
    main()
