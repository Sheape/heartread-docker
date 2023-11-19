from keras.models import load_model
from scipy.io import loadmat
from scipy.signal import filtfilt, butter
from app.cloudflare_r2 import deleteFile, uploadFile, downloadFile
import numpy as np
import os
import ecg_plot
from pathlib import Path

__version__ = '0.1.0'
BASE_DIR = Path(__file__).resolve(strict=True).parent

model = load_model(f"{BASE_DIR}/ecg_model_sigmoid-{__version__}.h5")
labels = [
    'Pacing Rhythm',
    'Axis left shift',
    'Axis right shift',
    'Left ventricular hypertrophy',
    'S-T changes',
    'Right bundle branch block',
    'T wave opposite',
    'Counterclockwise vectorcardiographic loop',
    'Left ventricle hypertrophy',
    'Atrial Fibrillation',
    'Atrial Flutter',
    'Abnormal Q wave',
    'ST extension',
    'T wave Change',
    'Lower voltage QRS in all lead',
    '1 Degree atrioventricular block',
    'Atrial premature beats',
    'Poor R wave progression',
    'Sinus Bradycardia',
    'Supraventricular Tachycardia',
    'Sinus Rhythm',
    'Sinus Tachycardia',
    'Premature ventricular contractions',
    'Sinus Irregularity',
    'ST-T Change',
    'ST drop down',
    'Intraventricular block',
    'Complete right bundle branch block'
]


def load_mat(filename):
    x = loadmat(filename)
    data = np.asarray(x['val'], dtype=np.float64)
    Wn = 0.1
    b, a = butter(4, Wn, 'low', analog=False)
    smooth_ecg = filtfilt(b, a, data)

    return smooth_ecg


def plot_ecg(filename):
    ecg_data = load_mat(filename)
    filename_only, _ = os.path.splitext(filename)
    ecg_plot.plot_12(ecg_data/1000, sample_rate=500, title="12-Lead ECG Graph")
    ecg_plot.save_as_svg(filename_only)


def createPlot(filename):
    downloadFile(filename)
    raw_filename, _ = os.path.splitext(filename)
    svgFile = f"{raw_filename}.svg"
    plot_ecg(filename)
    deleteFile(filename)
    uploadFile(svgFile)


def ecg_predict(filename):
    ecg = load_mat(filename)
    reshaped_ecg = ecg.reshape(1, 5000, 12)
    prediction = model.predict(x=reshaped_ecg)
    top_5 = sorted(prediction[0].tolist(), reverse=True)[:5]
    top_5_dict = {prediction[0].tolist().index(value): value for value in top_5}
    result_dict = {labels[k]: v for k, v in top_5_dict.items()}
    return result_dict
