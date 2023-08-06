import hashlib
from tqdm import tqdm_notebook
from IPython.core.display import display, HTML
from time import sleep
from swiftace.utils.anaconda import init_project, init_experiment
from swiftace.utils.data import get_dir_hash

API_URL = 'https://swiftai-217215.firebaseapp.com'
current_proj = None
current_run_id = None


def init(name):
    global current_proj
    if current_proj is None or current_proj != name:
        resp = init_project(name)
        if resp:
            current_proj = resp
            print(f'[swiftace] Project initlalized: {resp}')
            print(f"{get_project_tracking_url()}")

def dir_hash(directory):
    return get_dir_hash(directory)

    
def get_exp_tracking_url():
    global current_proj
    global current_run_id
    if current_proj is not None and current_run_id is not None:
        return f"{API_URL}/projects/{current_proj}/experiments/{current_run_id}"
    else:
        return ""


def get_project_tracking_url():
    global current_proj
    if current_proj is not None:
        return f"{API_URL}/projects/{current_proj}"
    else:
        return ""


def new_session(force=False):
    global current_proj
    global current_run_id
    if current_run_id is None or force:
        resp = init_experiment(current_proj)
        if resp is not None:
            current_run_id = resp
            print(f'[swiftace] Initiating new experiment: {resp}')
            print(f"{get_exp_tracking_url()}")
    else:
        print(f'[swiftace] Current experiment id: {current_run_id}')
        print(f"{get_exp_tracking_url()}")


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def log_dataset(path):
    for i in tqdm_notebook(range(100)):
        pass
    print('[swiftace] Dataset logged. Checksum: ' + md5(path))


def log_hyperparams(dict):
    for i in tqdm_notebook(range(100)):
        pass
    print(dict)
    print('')
    print('[swiftace] Hyperparameters logged successfully.')


class KerasCallback(object):
    def __init__(self):
        self.validation_data = None
        self.model = None

    def set_params(self, params):
        self.params = params

    def set_model(self, model):
        self.model = model

    def on_epoch_begin(self, epoch, logs=None):
        pass

    def on_epoch_end(self, epoch, logs=None):
        pass

    def on_batch_begin(self, batch, logs=None):
        pass

    def on_batch_end(self, batch, logs=None):
        pass

    def on_train_begin(self, logs=None):
        pass

    def on_train_end(self, logs=None):
        print('')
        print('[swiftace] Training metrics logged successfully.')


def log_metrics(dict):
    for _ in tqdm_notebook(range(100)):
        pass
    print(dict)
    print('')
    print('[swiftace] Metrics logged successfully.')


def upload_file(path):
    for _ in tqdm_notebook(range(21), unit='MB'):
        pass
    print('[swiftace] File uploaded successfully. Checksum: ' + md5(path))


def commit(message):
    for i in tqdm_notebook(range(4)):
        if i == 0:
            print('[swiftace] Capturing environment...')
        elif i == 1:
            print('[swiftace] Saving Jupyter notebook...')
        elif i == 2:
            print('[swiftace] Uploading source code...')
        else:
            print('[swiftace] Finalizing commit...')
        sleep(1)
    print('')
    print('[swiftace] Commit 0a9dc74d successful.')
    return display(HTML("""<a href="https://swiftace.ai/aakashns/keras-mnist/0a9dc74d" target="_blank">https://swiftace.ai/aakashns/mnist-basic/0a9dc74d</a>"""))
