import argparse
from Adpcm3 import Adpcm3
from pydub import AudioSegment
from adpcm import Adpcm
import scipy.io.wavfile as wavf
import numpy as np
import os 
from tqdm import tqdm
from multiprocessing import Pool


def adpcmProcess(info):
    file_path,output_dir = info
    if(os.path.exists(os.path.join(output_dir,file_path)[1])):
        return
    adpcm = Adpcm()
    sound = AudioSegment.from_wav(file_path)
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

    if not os.path.exists(output_dir):
        os.makedirs(output_dir,exist_ok=True)
    wavf.write(os.path.join(output_dir,file_path)[1], sound.frame_rate, afterAdpcmData.astype(np.int16))


def adpcm3Process(info):
    file_path,output_dir = info
    if(os.path.exists(os.path.join(output_dir,file_path)[1])):
        return
    adpcm3 = Adpcm3()
    sound = AudioSegment.from_wav(file_path)
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

    if not os.path.exists(output_dir):
        os.makedirs(output_dir,exist_ok=True)
    wavf.write(os.path.join(output_dir,file_path)[1], sound.frame_rate, afterAdpcmData.astype(np.float32))



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--files_path",
        type=str,
        default=None,
        help="The path of the wav file.",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        default='D:/adpcmed/',
        help="The path of the wav file.",
    )


    args = parser.parse_args()


    if args.output_dir is not None:
        os.makedirs(args.output_dir, exist_ok=True)

    return args


if __name__ == '__main__':
    
    args = parse_args()

    fileListTemp = os.listdir(args.files_path)
    infoList = []
    for index in range(len(fileListTemp)):
        if fileListTemp[index].endswith("wav"):
            infoList.append((os.path.join(args.files_path,fileListTemp[index]),args.output_dir))

    with Pool(os.cpu_count()) as pool:
        list(tqdm(pool.imap(adpcm3Process,infoList),total=len(infoList)))