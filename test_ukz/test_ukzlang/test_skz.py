import unittest
from ukz import skz,SkzConfig,ChannelConfig,SongConfig

class TestSkz(unittest.TestCase):

  def chk(self,code,channelConfigs,tempo=SkzConfig.defaultTempo):
    res = skz(code)
    songConfig = SongConfig(tempo,channelConfigs)
    self.assertEqual(res, songConfig)
    

################
# Tests

  def test_config_simple_programnumber(self):
    self.chk("%a i5", [ChannelConfig(programNumber=5,names=["a"])])
  def test_config_simple_word(self):
    self.chk("%a piano", [ChannelConfig(programNumber=0,names=["a"])])
  def test_config_severalwords(self):
    self.chk("%a overdrive guitar", [ChannelConfig(programNumber=29,names=["a"])])
  def test_config_words_and_ints(self):
    self.chk("%a elec piano 1", [ChannelConfig(programNumber=4,names=["a"])])
    self.chk("%a elec piano 2", [ChannelConfig(programNumber=5,names=["a"])])

  def test_config_severalnames(self):
    self.chk("%a %bee overdrive guitar", [ChannelConfig(programNumber=29,names=["a","bee"])])
    
  def test_config_defaultvelocity_nospace(self):
    self.chk("%a i5 v103", [ChannelConfig(programNumber=5,names=["a"],velocities={0:103})])
  def test_config_defaultvelocity_withspace(self):
    self.chk("%a i5 v 103", [ChannelConfig(programNumber=5,names=["a"],velocities={0:103})])
  def test_config_velocities_upward(self):
    self.chk("%a i5 v103 106 108", [ChannelConfig(programNumber=5,names=["a"],velocities={0:103,1:106,2:108})])
  def test_config_velocities_downward(self):
    self.chk("%a i5 v123 106 108", [ChannelConfig(programNumber=5,names=["a"],velocities={0:123,-2:106,-1:108})])
  def test_config_velocities_mixed(self):
    self.chk("%a i5 v103 108 80 106", [ChannelConfig(programNumber=5,names=["a"],velocities={0:103,-1:80,1:106,2:108})])
    
  def test_config_volume(self):
    self.chk("%a i5 V 78", [ChannelConfig(programNumber=5,names=["a"],volume=78)])
  def test_config_velocities_and_volume(self):
    self.chk("%a i5 v123 106 108 V 78", [ChannelConfig(programNumber=5,names=["a"],velocities={0:123,-2:106,-1:108},volume=78)])
  def test_config_volume_and_velocities(self):
    self.chk("%a i5 V78 v123 106 108", [ChannelConfig(programNumber=5,names=["a"],velocities={0:123,-2:106,-1:108},volume=78)])

  def test_config_octave(self):
    self.chk("%a i5 o2", [ChannelConfig(programNumber=5,names=["a"],octave=2)])
  def test_config_octave_and_volume(self):
    self.chk("%a i5 o2 V7", [ChannelConfig(programNumber=5,names=["a"],octave=2,volume=7)])
  def test_config_octave_and_velocities_and_volume(self):
    self.chk("%a i5 o2 v30 40 V7", [ChannelConfig(programNumber=5,names=["a"],octave=2,volume=7,velocities={0:30,1:40})])
  def test_config_velocities_and_volume_and_octave(self):
    self.chk("%a i5 v30 40 V7 o2", [ChannelConfig(programNumber=5,names=["a"],octave=2,volume=7,velocities={0:30,1:40})])


  def test_config_2lines_simples(self):
    self.chk("%a i5 %a i66", [
     ChannelConfig(programNumber=5,names=["a"]), \
     ChannelConfig(programNumber=66,names=["a"]) ])
  def test_config_2lines_severalwords(self):
    self.chk("%a acoustic piano %b %bee overdriven guitar", [
     ChannelConfig(programNumber=0,names=["a"]), \
     ChannelConfig(programNumber=29,names=["b","bee"]) ])
  def test_config_2lines_withvelocities(self):
    self.chk("%a acoustic piano v67 78 %b %bee overdriven guitar v78 89", [
     ChannelConfig(programNumber=0,names=["a"],velocities={0:67,1:78}), \
     ChannelConfig(programNumber=29,names=["b","bee"],velocities={0:78,1:89}) ])
     
  def test_config_with_bpm(self):
    self.chk("bpm 97 %a i5", [ChannelConfig(programNumber=5,names=["a"])],97)
  def test_config_with_bps(self):
    self.chk("bps 3 %a i5", [ChannelConfig(programNumber=5,names=["a"])],180)

################################

if __name__ == '__main__':
    unittest.main()