import struct

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash.SHA import SHA1Hash
from Crypto.Util import Counter
from Crypto import Random

from .zipfile import (
    ZIP_BZIP2, BadZipFile, BaseZipDecrypter, ZipFile, ZipInfo, ZipExtFile,
    crc32,
)

WZ_AES = 'WZ_AES'
WZ_AES_COMPRESS_TYPE = 99
WZ_AES_V1 = 0x0001
WZ_AES_V2 = 0x0002
WZ_AES_VENDOR_ID = b'AE'

EXTRA_WZ_AES = 0x9901


class AESZipDecrypter(BaseZipDecrypter):

    def __init__(self, zef_file, zinfo, pwd):
        super().__init__(zef_file, zinfo, pwd)
        self.zef_file = zef_file
        self.zinfo = zinfo

        salt_lengths = {
            1: 8,   # 128 bit
            2: 12,  # 192 bit
            3: 16,  # 256 bit
        }
        self.salt_length = salt_lengths[self._zinfo.wz_aes_strength]
        key_lengths = {
            1: 16,  # 128 bit
            2: 24,  # 192 bit
            3: 32,  # 256 bit
        }
        self.key_length = key_lengths[self._zinfo.wz_aes_strength]

        self.mac = b''
        self.mac_size = 10
        self.compress_left = zinfo.compress_size - self.offset() - self.mac_size

        salt = struct.unpack(
            "<{}s".format(self.salt_length),
            zef_file.read(self.salt_length)
        )[0]
        pwd_verify_length = 2
        pwd_verify = zef_file.read(pwd_verify_length)
        dkLen = 2*self.key_length + pwd_verify_length
        keymaterial = PBKDF2(self.pwd, salt, count=1000, dkLen=dkLen)

        encpwdverify = keymaterial[2*self.key_length:]
        if encpwdverify != pwd_verify:
            raise RuntimeError("Bad password for file %r" % self._zinfo.filename)

        enckey = keymaterial[:self.key_length]
        self.decypter = AES.new(
            enckey,
            AES.MODE_CTR,
            counter=Counter.new(nbits=128, little_endian=True)
        )
        encmac_key = keymaterial[self.key_length:2*self.key_length]
        self.hmac = HMAC.new(encmac_key, digestmod=SHA1Hash())

    def offset(self):
        # salt_length + pwd_verify_length
        return self.salt_length + 2

    def decrypt(self, data):
        if len(data) > self.compress_left:
            compress_data = data[:self.compress_left]
            self.mac += data[self.compress_left:]
            data = compress_data
            if not data:
                data = b''
        self.hmac.update(data)
        self.compress_left -= len(data)
        return self.decypter.decrypt(data)

    def check_integrity(self):
        if self.hmac.digest()[:10] != self.mac:
            raise BadZipFile("Bad HMAC check for file %r" % self.zinfo.filename)


class BaseZipEncrypter:

    def update_zipinfo(self, zipinfo):
        raise NotImplementedError(
            'BaseZipEncrypter implementations must implement `update_zipinfo`.'
        )

    def encrypt(self, data):
        raise NotImplementedError(
            'BaseZipEncrypter implementations must implement `encrypt`.'
        )

    def flush(self):
        return b''


class AESZipEncrypter(BaseZipEncrypter):

    def __init__(self, pwd, nbits=256, force_wz_aes_version=None):
        if nbits not in (128, 192, 256):
            raise RuntimeError(
                "`nbits` must be one of 128, 192, 256. Got '%s'" % nbits
            )

        self.force_wz_aes_version = force_wz_aes_version
        self.has_written_salt = False
        salt_lengths = {
            128: 8,
            192: 12,
            256: 16,
        }
        self.salt_length = salt_lengths[nbits]
        key_lengths = {
            128: 16,
            192: 24,
            256: 32,
        }
        key_length = key_lengths[nbits]
        aes_strengths = {
            128: 1,
            192: 2,
            256: 3,
        }
        self.aes_strength = aes_strengths[nbits]

        self.salt = Random.new().read(self.salt_length)
        pwd_verify_length = 2
        dkLen = 2 * key_length + pwd_verify_length
        keymaterial = PBKDF2(pwd, self.salt, count=1000, dkLen=dkLen)

        self.encpwdverify = keymaterial[2*key_length:]

        enckey = keymaterial[:key_length]
        self.encrypter = AES.new(
            enckey,
            AES.MODE_CTR,
            counter=Counter.new(nbits=128, little_endian=True)
        )
        encmac_key = keymaterial[key_length:2*key_length]
        self.hmac = HMAC.new(encmac_key, digestmod=SHA1Hash())

    def update_zipinfo(self, zipinfo):
        zipinfo.wz_aes_vendor_id = WZ_AES_VENDOR_ID
        zipinfo.wz_aes_strength = self.aes_strength
        if self.force_wz_aes_version is not None:
            zipinfo.wz_aes_version = self.force_wz_aes_version

    def encrypt(self, data):
        data = self.encrypter.encrypt(data)
        self.hmac.update(data)
        if not self.has_written_salt:
            self.has_written_salt = True
            return self.salt + self.encpwdverify + data
        return data

    def flush(self):
        out = b''
        if not self.has_written_salt:
            out = self.salt + self.encpwdverify
        return out + struct.pack('<10s', self.hmac.digest()[:10])


class AESZipInfo(ZipInfo):
    """Class with attributes describing each file in the ZIP archive."""

    # __slots__ on subclasses only need to contain the additional slots.
    __slots__ = (
        'wz_aes_version',
        'wz_aes_vendor_id',
        'wz_aes_strength',
        # 'wz_aes_actual_compression_type',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wz_aes_version = None
        self.wz_aes_vendor_id = None
        self.wz_aes_strength = None

    def decode_extra_wz_aes(self, ln, extra):
        if ln == 7:
            counts = struct.unpack("<H2sBH", extra[4: ln+4])
        else:
            raise BadZipFile(
                "Corrupt extra field %04x (size=%d)" % (EXTRA_WZ_AES, ln))

        self.wz_aes_version = counts[0]
        self.wz_aes_vendor_id = counts[1]
        # 0x01  128-bit encryption key
        # 0x02  192-bit encryption key
        # 0x03  256-bit encryption key
        self.wz_aes_strength = counts[2]

        # the compression method is the one that would otherwise have been
        # stored in the local and central headers for the file. For example, if
        # the file is imploded, this field will contain the compression code 6.
        # This is needed because a compression method of 99 is used to indicate
        # the presence of an AES-encrypted file
        self.compress_type = counts[3]
        # self.wz_aes_actual_compression_type = counts[3]

    def get_extra_decoders(self):
        extra_decoders = super().get_extra_decoders()
        extra_decoders[EXTRA_WZ_AES] = self.decode_extra_wz_aes
        return extra_decoders

    def encode_extra(self, crc, compress_type):
        wz_aes_extra = b''
        if self.wz_aes_vendor_id is not None:
            compress_type = WZ_AES_COMPRESS_TYPE
            aes_version = self.wz_aes_version
            if aes_version is None:
                if self.file_size < 20 | self.compress_type == ZIP_BZIP2:
                    # The only difference between version 1 and 2 is the
                    # handling of the CRC values. For version 2 the CRC value
                    # is not used and must be set to 0.
                    # For small files, the CRC files can leak the contents of
                    # the encrypted data.
                    # For bzip2, the compression already has integrity checks
                    # so CRC is not required.
                    aes_version = WZ_AES_V2
                else:
                    aes_version = WZ_AES_V1

            if aes_version == WZ_AES_V2:
                crc = 0

            wz_aes_extra = struct.pack(
                "<3H2sBH",
                EXTRA_WZ_AES,
                7,  # extra block body length: H2sBH
                aes_version,
                self.wz_aes_vendor_id,
                self.wz_aes_strength,
                self.compress_type,
            )
        return wz_aes_extra, crc, compress_type

    def encode_local_directory(self, *, crc, compress_type, extra, **kwargs):
        wz_aes_extra, crc, compress_type = self.encode_extra(crc, compress_type)
        return super().encode_local_directory(
            crc=crc,
            compress_type=compress_type,
            extra=extra+wz_aes_extra,
            **kwargs
        )

    def encode_central_directory(self, *, crc, compress_type, extra_data, **kwargs):
        wz_aes_extra, crc, compress_type = self.encode_extra(crc, compress_type)
        return super().encode_central_directory(
            crc=crc,
            compress_type=compress_type,
            extra_data=extra_data+wz_aes_extra,
            **kwargs)


class AESZipExtFile(ZipExtFile):

    def get_decrypter_cls(self):
        if self._zinfo.wz_aes_version is not None:
            return AESZipDecrypter
        return super().get_decrypter_cls()

    def _update_crc(self, newdata):
        if self._eof and self._decrypter:
            self._decrypter.check_integrity()
            if self._zinfo.wz_aes_version == WZ_AES_V2 and self._expected_crc == 0:
                # CRC value should be 0 for AES vendor version 2.
                return

        # Update the CRC using the given data.
        if self._expected_crc is None:
            # No need to compute the CRC if we don't have a reference value
            return
        self._running_crc = crc32(newdata, self._running_crc)
        # Check the CRC if we're at the end of the file

        if self._eof and self._running_crc != self._expected_crc:
            raise BadZipFile("Bad CRC-32 for file %r" % self.name)


class AESZipFile(ZipFile):
    zipinfo_cls = AESZipInfo
    zipextfile_cls = AESZipExtFile

    def __init__(self, *args, **kwargs):
        encryption = kwargs.pop('encryption', None)
        encryption_kwargs = kwargs.pop('encryption_kwargs', None)
        super().__init__(*args, **kwargs)
        self.encryption = encryption
        self.encryption_kwargs = encryption_kwargs

    def get_encrypter(self):
        if self.encryption == WZ_AES:
            if not self.pwd:
                raise RuntimeError(
                    '%s encryption requires a password.' % WZ_AES
                )
            if self.encryption_kwargs is None:
                encryption_kwargs = {}
            else:
                encryption_kwargs = self.encryption_kwargs

            return AESZipEncrypter(pwd=self.pwd, **encryption_kwargs)
