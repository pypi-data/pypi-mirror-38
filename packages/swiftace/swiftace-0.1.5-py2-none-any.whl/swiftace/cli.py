import argparse
from swiftace.utils.anaconda import save_conda_env, load_conda_env
from swiftace.utils.data import get_dir_hash


def exec_save_env():
    print('Capturing & saving anaconda environment..')
    hash = save_conda_env()
    print(f'Environment saved! ID: {hash}')
    print('Load using the command:')
    print(f'  $ swiftace load-env {hash}\n')


def exec_load_env(env_id, name):
    if not env_id:
        print('Environment ID is required!')
        return
    if not name:
        print('Please provide a name for the target environment using --name')
        return
    print(f'Loading environment "{env_id}"')
    load_conda_env(env_id, name)


def exec_dir_hash(directory):
    if not directory:
        print('Directory is required!')
        return
    print(f'Calculating hash of directory "{directory}"')
    get_dir_hash(directory)

    
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('env_id', nargs='?')
    parser.add_argument('-n', '--name')
    parser.add_argument('-d', '--dir')
    return parser.parse_args()


def main():
    args = get_args()
    command = args.command
    if command == 'save-env':
        exec_save_env()
    elif command == 'load-env':
        exec_load_env(args.env_id, args.name)
    elif command == 'hash':
        exec_dir_hash(args.dir)
    else:
        print('Unknown command')


if __name__ == '__main__':
    main()
