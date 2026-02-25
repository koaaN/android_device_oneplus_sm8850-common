#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'vendor/oneplus/infiniti', #"FIXME: libqti-perfd" depends on undefined module "libdisplayconfig.qti".
    'device/oneplus/sm8850-common',
    'hardware/qcom-caf/sm8850',
    'hardware/qcom-caf/wlan',
    'hardware/oplus',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]

def lib_fixup_odm_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'odm' else None

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libosensenativeproxy_client',
        'vendor.oplus.hardware.subsys-V5-ndk',
        'vendor.qti.ImsRtpService-V2-ndk',
        'vendor.qti.diaghal-V1-ndk',
        'vendor.qti.hardware.dpmaidlservice-V1-ndk',
        'vendor.qti.hardware.wifidisplaysession_aidl-V1-ndk',
        'vendor.qti.qccsyshal_aidl-V1-ndk',
        'vendor.qti.qccvndhal_aidl-V1-ndk',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so' : blob_fixup()
        .replace_needed('libprotobuf-cpp-full.so', 'libprotobuf-cpp-full-21.12.so'),
    'odm/bin/hw/vendor.oplus.hardware.biometrics.fingerprint@2.1-service_uff': blob_fixup()
        .add_needed('libshims_aidl_fingerprint_v3.oplus.so'),
    'odm/etc/init/init.network.rc': blob_fixup()
        .regex_replace(r'/\* (Huo\.Chen@SYSTEM\.RF, 2024/09/06, Add for ICC) \*/', r'# \1'),
    'product/etc/sysconfig/com.android.hotwordenrollment.common.util.xml': blob_fixup()
        .regex_replace('/my_product', '/product'),
    'system_ext/bin/horae': blob_fixup()
        .replace_needed('libprotobuf-cpp-lite.so', 'libprotobuf-cpp-lite-21.12.so'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .add_needed('libinput_shim.so'),
    (
        'vendor/etc/media_codecs_canoe_sku3.xml',
        'vendor/etc/media_codecs_canoe_v2.xml',
    ): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n', ''),
    (
        'vendor/lib64/hw/android.hardware.bluetooth.audio_sw.so',
        'vendor/lib64/hw/libaudiocorehal.default.so',
        'vendor/lib64/hw/libaudiocorehal.qti.so',
        'vendor/lib64/libaudioplatformconverter.qti.so',
        'vendor/lib64/libaudioserviceexampleimpl.so',
        'vendor/lib64/libqtigefar.so',
        'vendor/lib64/libwfdmmsrc_proprietary.so',
    ): blob_fixup()
        .replace_needed('android.hardware.audio.core-V3-ndk.so', 'android.hardware.audio.core-V4-ndk.so'),
    (
        'vendor/lib64/hw/android.hardware.bluetooth.audio_sw.so',
        'vendor/lib64/hw/libaudiocorehal.qti.so',
        'vendor/lib64/hw/libaudioeffecthal.qti.so',
        'vendor/lib64/libaudioserviceexampleimpl.so',
        'vendor/lib64/libqtigefar.so',
        'vendor/lib64/soundfx/libqcompostprocbundle.so',
        'vendor/lib64/soundfx/libqcomvisualizer.so',
        'vendor/lib64/soundfx/libqcomvoiceprocessing.so',
        'vendor/lib64/soundfx/libvolumelistener.so',
    ): blob_fixup()
        .replace_needed('android.media.audio.common.types-V5-ndk.so', 'android.media.audio.common.types-V4-ndk.so'),
    'vendor/lib64/libaudioserviceexampleimpl.so': blob_fixup()
        .add_needed('libbluetooth_audio_session_aidl_shim.so')
        .add_needed('libaudioutils_shim.so'),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/lib64/libVoiceSdk.so': blob_fixup()
        .replace_needed('libtensorflowlite_c.so', 'libtensorflowlite_c_vendor.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8850-common',
    'oneplus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)
module.add_proprietary_file('proprietary-files-phone.txt').add_copy_files_guard(
    'TARGET_IS_TABLET', 'true', invert=True
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
