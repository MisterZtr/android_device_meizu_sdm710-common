# Copyright (C) 2009 The Android Open Source Project
# Copyright (C) 2019 The MoKee Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import common
import re

def FullOTA_InstallBegin(info):
  OTA_InstallFirmware(info)
  return

def IncrementalOTA_InstallBegin(info):
  OTA_InstallFirmware(info)
  return

def AddImage(info, basename, dest):
  name = basename
  data = info.input_zip.read("RADIO/" + basename)
  common.ZipWriteStr(info.output_zip, name, data)
  info.script.Print("Flashing " + basename + "...")
  info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))

def AddImageWithBak(info, basename, dest):
  name = basename
  data = info.input_zip.read("RADIO/" + basename)
  common.ZipWriteStr(info.output_zip, name, data)
  info.script.Print("Flashing " + basename + "...")
  info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))
  info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest + "bak"))

def OTA_InstallFirmware(info):
  info.script.Print("Patching firmware images...")
  info.script.Print("Flashing...")
  AddImageWithBak(info, "cmnlib64.mbn", "/dev/block/bootdevice/by-name/cmnlib64")
  AddImageWithBak(info, "cmnlib.mbn", "/dev/block/bootdevice/by-name/cmnlib")
  AddImageWithBak(info, "hyp.mbn", "/dev/block/bootdevice/by-name/hyp")
  AddImageWithBak(info, "tz.mbn", "/dev/block/bootdevice/by-name/tz")
  AddImageWithBak(info, "aop.mbn", "/dev/block/bootdevice/by-name/aop")
  AddImageWithBak(info, "xbl_config.elf", "/dev/block/bootdevice/by-name/xbl_config")
  AddImageWithBak(info, "keymaster64.mbn", "/dev/block/bootdevice/by-name/keymaster")
  AddImageWithBak(info, "qupv3fw.elf", "/dev/block/bootdevice/by-name/qupfw")
  AddImageWithBak(info, "abl.elf", "/dev/block/bootdevice/by-name/abl")
  AddImageWithBak(info, "dtbo.img", "/dev/block/bootdevice/by-name/dtbo")
  AddImageWithBak(info, "devcfg.mbn", "/dev/block/bootdevice/by-name/devcfg")
  AddImageWithBak(info, "storsec.mbn", "/dev/block/bootdevice/by-name/storsec")
  AddImageWithBak(info, "xbl.elf", "/dev/block/bootdevice/by-name/xbl")
  info.script.Print("Finalizing...")
  AddImage(info, "dspso.bin", "/dev/block/bootdevice/by-name/dsp")
  AddImage(info, "NON-HLOS.bin", "/dev/block/bootdevice/by-name/modem")
  AddImage(info, "BTFM.bin", "/dev/block/bootdevice/by-name/bluetooth")
  AddImage(info, "vbmeta.img", "/dev/block/bootdevice/by-name/vbmeta")
  info.script.Print("Firmware images patched successfully!")
  return
