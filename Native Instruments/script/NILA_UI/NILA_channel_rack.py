import nihia
from nihia import *

from script.device_setup import NILA_core as core

from script.device_setup import config 
from script.device_setup import constants
from script.device_setup import transform 
from script.screen_writer import NILA_OLED as oled

import channels
import device 
import ui 

def OnMidiMsg(self, event): 

    if ui.getFocused(constants.winName["Channel Rack"]) == True:

        # VOLUME CONTROL
        s_series = False

        for z in range(8):
            if channels.channelCount() > z and channels.selectedChannel() < (channels.channelCount() - z) :
                if (event.data1 == nihia.mixer.knobs[0][z]):
                    event.handled = True 
                    
                    if core.seriesCheck(s_series) == True: 
                        
                        print(event.data2)
                         
                        if event.data2 in range(65, 95):
                            if channels.getChannelVolume(channels.selectedChannel() + z) != 0 :
                                channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) - config.increment * 2.5)) 
                                
                        elif event.data2 in range(96, 128):
                            if channels.getChannelVolume(channels.selectedChannel() + z) != 0 :
                                channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) - config.increment))
                                
                        elif event.data2 in range (0, 31):
                            channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) + config.increment))
                       
                        elif event.data2 in range (32, 64):
                            channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) + config.increment * 2.5))
                    else:
                        if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                            if channels.getChannelVolume(channels.selectedChannel() + z) != 0 :
                                channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) - config.increment)) 

                        elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                            channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) + config.increment))
                            
                oled.OnRefresh(self, event)

            else:
                event.handled = True 

        # PAN CONTROL

        for z in range(8):
            if channels.channelCount() > z and channels.selectedChannel() < (channels.channelCount()-z) :
                if (event.data1 == nihia.mixer.knobs[1][z]):
                    event.handled = True  
                    if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (channels.getChannelPan(channels.selectedChannel() + z))
                        channels.setChannelPan((channels.selectedChannel() + z), (x - config.increment) )

                    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:  
                        x = (channels.getChannelPan(channels.selectedChannel() + z))
                        channels.setChannelPan((channels.selectedChannel() + z), (x + config.increment) ) 
            else:
                event.handled = True 

