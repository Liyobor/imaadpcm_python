from Ray_Python_Tools import SimpleFileExplorer
from pydub import AudioSegment
from adpcm import Adpcm
import scipy.io.wavfile as wavf
import numpy as np
import os 
from tqdm import tqdm
adpcm = Adpcm()
explorer = SimpleFileExplorer()
path = input("輸入路徑\n")

explorer.walk(path)

for file in tqdm(explorer.files):

    sound = AudioSegment.from_wav(file)
    sound = sound.set_channels(1)
    dataArray = sound.get_array_of_samples()
    encodeSample = []
    afterAdpcmData = []
    adpcm.resetState()
    for data in dataArray:
        encodeSample.append(adpcm.encode(data))
    # print('encode sample len = ',len(encodeSample))
    # print('encode sample max = ',max(encodeSample))
    # print('encode sample min = ',min(encodeSample))
    adpcm.resetState()
    for data in encodeSample:
        afterAdpcmData.append(adpcm.decode(data))
    # print('decode sample len = ',len(afterAdpcmData))
    # print('decode sample max = ',max(afterAdpcmData))
    # print('decode sample min = ',min(afterAdpcmData))
    afterAdpcmData = np.array(afterAdpcmData)
    # print('-'*8)
    # print(os.path.split(explorer.files[3])[1])

    wavf.write(f'adpcmed/{os.path.split(file)[1]}', sound.frame_rate, afterAdpcmData.astype(np.int16))