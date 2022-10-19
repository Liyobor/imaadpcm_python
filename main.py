from Ray_Python_Tools import SimpleFileExplorer
from pydub import AudioSegment
from adpcm import Adpcm
import scipy.io.wavfile as wavf
import numpy as np
import os 
from tqdm import tqdm
from multiprocessing import Pool


def adpcmProcess(file):
    # for file in tqdm(explorer.files):
    if(os.path.exists(f'D:/adpcmed/{os.path.split(file)[1]}')):
        return
    adpcm = Adpcm()
    sound = AudioSegment.from_wav(file)
    sound = sound.set_channels(1)
    dataArray = sound.get_array_of_samples()
    encodeSample = []
    afterAdpcmData = []

    adpcm.resetState()

    

    for data in dataArray:
        '''
        IMA-ADPCM encode
        '''
        encodeSample.append(adpcm.encode(data))
    adpcm.resetState()

    for data in encodeSample:
        '''
        IMA-ADPCM decode
        '''
        afterAdpcmData.append(adpcm.decode(data))
    afterAdpcmData = np.array(afterAdpcmData)
    
    if not os.path.exists('D:/adpcmed'):
        os.makedirs('D:/adpcmed')
    wavf.write(f'D:/adpcmed/{os.path.split(file)[1]}', sound.frame_rate, afterAdpcmData.astype(np.int16))


if __name__ == '__main__':
    
    explorer = SimpleFileExplorer()
    path = input("輸入路徑\n")
    explorer.walk(path)
    fileList = explorer.files
    with Pool(os.cpu_count()) as pool:
        list(tqdm(pool.imap(adpcmProcess,fileList),total=len(fileList)))