import spikeinterface as si
import spiketoolkit as st
import spikewidgets as sw
import json
from PIL import Image
import os
from copy import deepcopy
from kbucket import client as kb
from pairio import client as pa
import mlprocessors as mlpr
from matplotlib import pyplot as plt

def sf_summarize_recording(recording):
  ret=deepcopy(recording)
  ret['computed_info']=compute_recording_info(recording)  
  firings_true_path=recording['directory']+'/firings_true.mda'
  if kb.findFile(firings_true_path):
    ret['ground_truth']=firings_true_path
  ret['plots']=dict(
    timeseries=create_timeseries_plot(recording)
  )
  if ret['ground_truth']:
    ret['plots']['waveforms_true']=create_waveforms_plot(recording,ret['ground_truth'])
  return ret

def read_json_file(fname):
  with open(fname) as f:
    return json.load(f)
  
def write_json_file(fname,obj):
  with open(fname, 'w') as f:
    json.dump(obj, f)
    
def save_plot(fname,quality=40):
    plt.savefig(fname+'.png')
    plt.close()
    im=Image.open(fname+'.png').convert('RGB')
    os.remove(fname+'.png')
    im.save(fname,quality=quality)

# A MountainLab processor for generating the summary info for a recording
class ComputeRecordingInfo(mlpr.Processor):
  NAME='ComputeRecordingInfo'
  VERSION='0.1.0'
  recording_dir=mlpr.Input(directory=True,description='Recording directory')
  json_out=mlpr.Output('Info in .json file')
    
  def run(self):
    ret={}
    recording=si.MdaRecordingExtractor(dataset_directory=self.recording_dir,download=False)
    ret['samplerate']=recording.getSamplingFrequency()
    ret['num_channels']=len(recording.getChannelIds())
    ret['duration_sec']=recording.getNumFrames()/ret['samplerate']
    write_json_file(self.json_out,ret)
  
def compute_recording_info(recording):
  out=ComputeRecordingInfo.execute(recording_dir=recording['directory'],json_out={'ext':'.json'}).outputs['json_out']
  kb.saveFile(out)
  return read_json_file(kb.realizeFile(out))

# A MountainLab processor for generating a plot of a portion of the timeseries
class CreateTimeseriesPlot(mlpr.Processor):
  NAME='CreateTimeseriesPlot'
  VERSION='0.1.6'
  recording_dir=mlpr.Input(directory=True,description='Recording directory')
  jpg_out=mlpr.Output('The plot as a .jpg file')
  
  def run(self):
    R0=si.MdaRecordingExtractor(dataset_directory=self.recording_dir,download=False)
    R=st.filters.bandpass_filter(recording=R0,freq_min=300,freq_max=6000)
    N=R.getNumFrames()
    N2=int(N/2)
    channels=R.getChannelIds()
    if len(channels)>20: channels=channels[0:20]
    sw.TimeseriesWidget(recording=R,trange=[N2-4000,N2+0],channels=channels,width=12,height=5).plot()
    save_plot(self.jpg_out)
    
def create_timeseries_plot(recording):
  out=CreateTimeseriesPlot.execute(recording_dir=recording['directory'],jpg_out={'ext':'.jpg'}).outputs['jpg_out']
  kb.saveFile(out)
  return 'sha1://'+kb.computeFileSha1(out)+'/timeseries.jpg'

# A MountainLab processor for generating a plot of a portion of the timeseries
class CreateWaveformsPlot(mlpr.Processor):
  NAME='CreateWaveformsPlot'
  VERSION='0.1.0'
  recording_dir=mlpr.Input(directory=True,description='Recording directory')
  firings=mlpr.Input(description='Firings file')
  jpg_out=mlpr.Output('The plot as a .jpg file')
  
  def run(self):
    R0=si.MdaRecordingExtractor(dataset_directory=self.recording_dir,download=True)
    R=st.filters.bandpass_filter(recording=R0,freq_min=300,freq_max=6000)
    S=si.MdaSortingExtractor(firings_file=self.firings)
    channels=R.getChannelIds()
    if len(channels)>20:
      channels=channels[0:20]
    units=S.getUnitIds()
    if len(units)>20:
      units=units[::int(len(units)/20)]
    sw.UnitWaveformsWidget(recording=R,sorting=S,channels=channels,unit_ids=units).plot()
    save_plot(self.jpg_out)
    
def create_waveforms_plot(recording,firings):
  out=CreateWaveformsPlot.execute(recording_dir=recording['directory'],firings=firings,jpg_out={'ext':'.jpg'}).outputs['jpg_out']
  kb.saveFile(out)
  return 'sha1://'+kb.computeFileSha1(out)+'/waveforms.jpg'

