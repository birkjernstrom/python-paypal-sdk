import sys


def opposite_platform_endian():
	endianness = sys.byteorder
	if endianness == 'little':
		return 'be'
	else: # endianness == 'big'
		return 'le'

paypal_to_python_char_encoding_mapping = {
	'Big5':						'big5',
	'EUC-JP':					'euc_jp',
	'EUC-KR':					'euc_kr',
	'EUC-TW':					'not-supported',
	'gb2312':					'gb2312',
	'gbk':						'gbk',
	'HZ-GB-2312':				'hz',
	'ibm-862':					'cp862',
	'ISO-2022-CN':				'not-supported',
	'ISO-2022-JP':				'iso2022_jp',
	'ISO-2022-KR':				'iso2022_kr',
	'ISO-8859-1':				'latin_1',
	'ISO-8859-2':				'iso8859_2',
	'ISO-8859-3':				'iso8859_3',
	'ISO-8859-4':				'iso8859_4',
	'ISO-8859-5':				'iso8859_5',
	'ISO-8859-6':				'iso8859_6',
	'ISO-8859-7':				'iso8859_7',
	'ISO-8859-8':				'iso8859_8',
	'ISO-8859-9':				'iso8859_9',
	'ISO-8859-13':				'iso8859_13',
	'ISO-8859-15':				'iso8859_15',
	'KOI8-R':					'koi8_r',
	'Shift_JIS':				'shift_jis',
	'UTF-7':					'utf_7',
	'UTF-8':					'utf_8',
	'UTF-16':					'utf_16',
	'UTF-16BE':					'utf_16_be',
	'UTF-16LE':					'utf_16_le',
	'UTF16_PlatformEndian':		'utf_16', # Python default is platform endianness
	'UTF16_OppositeEndian':		'utf_16_'+opposite_platform_endian(),
	'UTF-32':					'utf_32',
	'UTF-32BE':					'utf_32_be',
	'UTF-32LE':					'utf_32_le',
	'UTF32_PlatformEndian':		'utf_32', # Python default is platform endianness
	'UTF32_OppositeEndian':		'utf_32_'+opposite_platform_endian(),
	'US-ASCII':					'ascii',
	'windows-1250':				'cp1250',
	'windows-1251':				'cp1251',
	'windows-1252':				'cp1252',
	'windows-1253':				'cp1253',
	'windows-1254':				'cp1254',
	'windows-1255':				'cp1255',
	'windows-1256':				'cp1256',
	'windows-1257':				'cp1257',
	'windows-1258':				'cp1258',
	'windows-874':				'cp874',
	'windows-949':				'cp949',
	'x-mac-greek':				'mac_greek',
	'x-mac-turkish':			'mac_turkish',
	'x-mac-centraleurroman':	'mac_latin2',
	'x-mac-cyrillic':			'mac_cyrillic',
	'ebcdic-cp-us':				'cp037' # According to http://www.fileformat.info/info/charset/index.htm
	'ibm-1047':					'not-supported'
}
