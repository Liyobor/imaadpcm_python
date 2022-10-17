class Adpcm:

    def __init__(self) -> None:
        self._ps = 0
        self._i = 0
        self._ss = 7

        self._i_table = [-1, -1, -1, -1, 2, 4, 6, 8,
        -1, -1, -1, -1, 2, 4, 6, 8]

        self._ss_table = [7, 8, 9, 10, 11, 12, 13, 14,
        16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45, 50, 55, 60,
        66, 73, 80, 88, 97, 107, 118, 130, 143, 157, 173, 190, 209,
        230, 253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658,
        724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878,
        2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871,
        5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635,
        13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794,
        32767]

    def encode(self,input):
        sample:int = 0
        diff:int = input - self._ps
        if diff<0:
            sample = 1 << 3
        diff = abs(diff)
    
        sample = sample | int((diff <<2) / self._ss) & 0x7
        self._ps += self._diffcalc(sample,self._ss)

        pcm = self._ps
        pcm = self._clamp(pcm,-32768,32767)
        self._i += self._i_table[sample]
        self._i = self._clamp(self._i,0,88)
        self._ss = self._ss_table[self._i]
        return sample

    def decode(self,sample):
        self._ps += self._diffcalc(sample,self._ss)
        pcm = self._ps
        pcm = self._clamp(pcm,-32768,32767)
        self._i += self._i_table[sample]
        self._i = self._clamp(self._i,0,88)
        self._ss = self._ss_table[self._i]
        return pcm

    def _diffcalc(self,sample,ss):
        diff = 0
        smp = sample & 0x7
        diff = smp * ss >>2
        return -diff if (sample & 0x8) == 8 else diff

    def _clamp(self,value,min,max):
        return min if value<min else max if value>max else value
        
    def resetState(self):
        self._ps = 0
        self._i = 0
        self._ss = 7
