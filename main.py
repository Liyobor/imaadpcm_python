from Adpcm3 import Adpcm3
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
    sound = sound.set_sample_width(2)
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


def adpcm3Process(file):
    if(os.path.exists(f'D:/adpcmed/{os.path.split(file)[1]}')):
        return
    adpcm3 = Adpcm3()
    sound = AudioSegment.from_wav(file)
    sound = sound.set_channels(1)
    sound = sound.set_sample_width(2)
    dataArray = sound.get_array_of_samples()
    encodeSample = []
    afterAdpcmData = []

    adpcm3.resetState()

    

    for data in dataArray:
        '''
        IMA-ADPCM encode
        '''
        encodeSample.append(adpcm3.encode(data))

    for data in encodeSample:
        '''
        IMA-ADPCM decode
        '''
        afterAdpcmData.append(adpcm3.decode(data))
    afterAdpcmData = np.array(afterAdpcmData)
    # print(afterAdpcmData)
    
    if not os.path.exists('D:/adpcmed'):
        os.makedirs('D:/adpcmed')
    wavf.write(f'D:/adpcmed/{os.path.split(file)[1]}', sound.frame_rate, afterAdpcmData.astype(np.float32))



if __name__ == '__main__':
    

    path = input("輸入音檔資料夾路徑\n")
    
    fileListTemp = os.listdir(path)
    fileList = []
    for index in range(len(fileListTemp)):
        if fileListTemp[index][-3:]=="wav":
            fileList.append(os.path.join(path,fileListTemp[index]))

    with Pool(os.cpu_count()) as pool:
        list(tqdm(pool.imap(adpcm3Process,fileList),total=len(fileList)))