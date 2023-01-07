from State import State


class Adpcm3:
    def __init__(self) -> None:
        self.encodeState = State()
        self.decodeState = State()
        self.isEnable = True

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

    def encode(self,inData):
        valpred = self.encodeState.valprev
        index = self.encodeState.index
        step = self._ss_table[index]
        diff = inData - valpred
        if(diff<0):
            delta = 8
            diff = -diff
        else:
            delta = 0
        vpdiff = step >> 3
        if(diff>=step):
            delta = delta | 4
            diff -= step
            vpdiff += step
        step = step >> 1
        if(diff>=step):
            delta = delta | 1
            vpdiff += step
        if (delta &8):
            valpred -= vpdiff
            if (valpred<-32768):
                valpred -= 32768
        else:
            valpred+=vpdiff
            if(valpred>32767):
                valpred=32767
        index += self._i_table[delta]
        if(index<0):
            index = 0
        elif(index>88):
            index = 88
        step = self._ss_table[index]
        self.encodeState.valprev = valpred
        self.encodeState.index = index
        return delta

    def decode(self,delta):
        valpred = self.decodeState.valprev
        index = self.decodeState.index
        step = self._ss_table[index]
        vpdiff = step >> 3
        index += self._i_table[delta]
        if(index<0):
            index = 0
        elif(index>88):
            index = 88
        if(delta&4):
            vpdiff += step
        if(delta&2):
            vpdiff += step >> 1
        if(delta&1):
            vpdiff += step >> 2
        if(delta &8):
            valpred-=vpdiff
            if(valpred<-32768):
                valpred = -32768
        else:
            valpred+=vpdiff
            if(valpred>32767):
                valpred = 32767
        step = self._ss_table[index]
        self.decodeState.valprev = valpred
        self.decodeState.index = index
        

        # return valpred
        if(valpred<0):
            return valpred/32768
        elif(valpred>0):
            return valpred/32767
        else:
            return valpred

    def resetState(self):
        self.encodeState.reset()
        self.decodeState.reset()