import numpy as np

class STM:
    def __init__(self, LockinRC_factor = 7960., DAC_Voltage_Range = 20000.0):
        self.LockinRC_factor = LockinRC_factor #mutliplicative factor to get LockinRC param in Hz
        self.DAC_Voltage_Range = DAC_Voltage_Range #in mV
    def __str__(self):
        ret = 'LockinRC_factor: %f\n' %self.LockinRC_factor
        ret += 'DAC_Voltage_Range: %.1f mV' %self.DAC_Voltage_Range
        return ret

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
def load_VERT_file(filename, stm = STM()):
     #find all the relevant parameters
    f = open(filename, 'r')
    for line in f:
        if "ZPiezoconst" in line:
            ZPiezoconst = float(line[line.find('=')+1:-1])
        if "LockinRC" in line:
            LockinRC = float(line[line.find('=')+1:-1])*stm.LockinRC_factor #Hz
        if "Vertmandelay" in line:
            Vertmandelay = float(line[line.find('=')+1:-1])
        if "VertSpecBack" in line:
            VertSpecBack = int(line[line.find('=')+1:-1])
        if "LockinAmpl" in line:
            LockinAmpl = float(line[line.find('=')+1:-1]) #mV
        if "Current[A]" in line:
            Current = float(line[line.find('=')+1:-1]) #Amps
        if "DSP_Clock" in line:
            DSP_Clock = float(line[line.find('=')+1:-1]) #DSP Units to determine Speclength
        if "DAC-Type" in line:
            DAC_Type = float(line[line.find('=')+1:-4])
        if "Gainpreamp" in line:
            Gainpreamp = float(line[line.find('=')+1:-1])


    #data = np.loadtxt(filename, skiprows = stm.skiprows)
    EOF = file_len(filename)

    N = int(np.loadtxt(filename, skiprows = EOF - 1)[0]) + 1

    Speclength = Vertmandelay * N / DSP_Clock
    
    data = np.loadtxt(filename, skiprows = EOF-N)
                   
    z = data[:, 2] * ZPiezoconst/1000.0 # Angstroms
    V = data[:, 1] / 1000.0 #Volts
    I = data[:, 3] / 2**DAC_Type * stm.DAC_Voltage_Range / 10**Gainpreamp / 1e6#current in amps 
    dIdV = data[:, 4] / 2**DAC_Type * stm.DAC_Voltage_Range #conductance in meV

    ret = spectra(V, I, dIdV)
    
    label = filename[-19:-5]
    if 'L' in label or 'R' in label:
        label = filename[-25:-5]
    ret.label = label
    ret.z = z
    ret.ZPiezoconst = ZPiezoconst
    ret.LockinRC = LockinRC
    ret.Speclength = Speclength
    ret.VertSpecBack = VertSpecBack
    ret.LockinAmpl = LockinAmpl
    ret.Current = Current
    ret.N = N
    #hysteresis correction factor
    hyst = int(N/Speclength/LockinRC/np.pi)
    ret.hyst = hyst
    f.close()

    return ret
        
class spectra:
    def __init__(self, V, I, dIdV):
        self.label = None

        #data should include V, z, I, and dIdV in that order
        
        #Assign values to spectra object
        self.ZPiezoconst = 1.0
        self.LockinRC = 0.0
        self.Speclength = None
        self.VertSpecBack = 0
        self.LockinAmpl = None
        self.Current = 1

        self.hyst = 0

        self.z = np.ones(len(V))
        self.V = V
        self.I = I
        self.dIdV = dIdV
        
        #Number of data points, needed for averaging and hysteresis correction
        N = len(V)
        self.N = N

    #use command print(spectra_object) to print out a few relevant parameters
    def __str__(self):
        ret = 'label: ' + self.label +'\n'
        ret += 'data points: %d\n' %self.N
        ret += 'VertSpecBack: %d\n' %self.VertSpecBack
        ret += 'LockinAmpl: %.1f mV\n' %self.LockinAmpl
        ret += 'Setpoint: %.1e A\n' %self.Current
        ret += 'Hystersis Correction: %d' %self.hyst
        return ret

    def average(self, hyst_cor = True):
    # this function averages the spectra together, and edits the values of sepctra_object.V, .z, .I, and .dIdV
    #not if you want to get the original values after this, just call e.g. epctra_object.I0
        
        N = self.N 
        if self.VertSpecBack + 1 <= 1:
            raise Exception('VertSpecBack is %d, which means no averaging or hystersis correction is possible.' %n)
        else:
            while N % (self.VertSpecBack + 1) != 0:
                self.V = delete(self.V, len(self.V))
                self.I = delete(self.I, len(self.I))
                self.dIdV = delete(self.dIdV, len(self.dIdV))
                self.z = delete(self.z, len(self.z))
        self.N = len(self.V)

        n = N/(self.VertSpecBack+1)
        V = self.V[0:n]

        dIdV = np.zeros(n)
        I = np.zeros(n)
        z = np.zeros(n)

        if hyst_correction == True:
            hyst = self.hyst
        else:
            hyst = 0

        foo = np.empty(n)
        for i in range(self.VertSpecBack+1):
            if i%2 == 0:
                j, k = hyst/2 + i*n, n * (i+1)

                foo[0:-hyst/2] = self.I[j:k]
                foo[-hyst/2:] = self.I[k-1]
                I += foo

                foo[0:-hyst/2] = self.dIdV[j:k]
                foo[-hyst/2:] = self.dIdV[k-1]
                dIdV += foo

                foo[0:-hyst/2] = self.z[j:k]
                foo[-hyst/2:] = self.z[k-1]
                z += foo
            else:
                j, k = i*n + hyst/2, (i + 1)*n
                
                foo[0:-hyst/2] = self.I[j:k]
                foo[-hyst/2:] = self.I[k-1]
                foo = foo[::-1]
                I += foo

                foo[0:-hyst/2] = self.dIdV[j:k]
                foo[-hyst/2:] = self.dIdV[k-1]
                foo = foo[::-1]
                dIdV += foo

                foo[0:-hyst/2] = self.z[j:k]
                foo[-hyst/2:] = self.z[k-1]
                foo = foo[::-1]
                z += foo

        self.V = V
        self.I = I/(self.VertSpecBack + 1)
        self.dIdV = dIdV/(self.VertSpecBack + 1)
        self.z = z/(self.VertSpecBack + 1)

            
        
    #normalize the spectra using an input value of kappa in Ang^-1
    def normalize(self, kappa):
        self.I = self.I * np.exp(-2 * kappa * self.z)
        self.dIdV = self.dIdV * np.exp(-2* kappa * self.z)
