"""An Utility to Convert Bijoy ASCII Text to Unicode Bengali"""
import re

__author__ = "Utsob Roy"
__license__ = "MPL2"
__version__ = "1.0.0"
__maintainer__ = "Utsob Roy"
__email__ = "roy@codesign.com.bd"
__status__ = "Beta"

PRE_CONVERSION_MAP = {
    # '্্' : '্'
    ' +': ' ',
    'yy': 'y',
    'vv': 'v',
    '„„': '„',
    '­­': '­',
    'y&': 'y',
    '„&': '„',
    '‡u': 'u‡',
    'wu': 'uw',
    ' ,': ',',
    ' \\|': '\\|',
    '\\\\ ': '',
    ' \\\\': '',
    '\\\\': '',
    '\n +': '\n',
    ' +\n': '\n',
    '\n\n\n\n\n': '\n\n',
    '\n\n\n\n': '\n\n',
    '\n\n\n': '\n\n'
}
CONVERSION_MAP = {
    'Av': 'আ',
    'A': 'অ',
    'B': 'ই',
    'C': 'ঈ',
    'D': 'উ',
    'E': 'ঊ',
    'F': 'ঋ',
    'G': 'এ',
    'H': 'ঐ',
    'I': 'ও',
    'J': 'ঔ',
    'K': 'ক',
    'L': 'খ',
    'M': 'গ',
    'N': 'ঘ',
    'O': 'ঙ',
    'P': 'চ',
    'Q': 'ছ',
    'R': 'জ',
    'S': 'ঝ',
    'T': 'ঞ',
    'U': 'ট',
    'V': 'ঠ',
    'W': 'ড',
    'X': 'ঢ',
    'Y': 'ণ',
    'Z': 'ত',
    '_': 'থ',
    '`': 'দ',
    'a': 'ধ',
    'b': 'ন',
    'c': 'প',
    'd': 'ফ',
    'e': 'ব',
    'f': 'ভ',
    'g': 'ম',
    'h': 'য',
    'i': 'র',
    'j': 'ল',
    'k': 'শ',
    'l': 'ষ',
    'm': 'স',
    'n': 'হ',
    'o': 'ড়',
    'p': 'ঢ়',
    'q': 'য়',
    'r': 'ৎ',
    's': 'ং',
    't': 'ঃ',
    'u': 'ঁ',
    '0': '০',
    '1': '১',
    '2': '২',
    '3': '৩',
    '4': '৪',
    '5': '৫',
    '6': '৬',
    '7': '৭',
    '8': '৮',
    '9': '৯',
    '•': 'ঙ্',
    '|': '।',
    '°': 'ক্ক',
    '±': 'ক্ট',
    '²': 'ক্ষ্ণ',
    '³': 'ক্ত',
    '´': 'ক্ম',
    'µ': 'ক্র',
    '¶': 'ক্ষ',
    '·': 'ক্স',
    '¸': 'গু',
    '¹': 'জ্ঞ',
    'º': 'গ্দ',
    '»': 'গ্ধ',
    '¼': 'ঙ্ক',
    '½': 'ঙ্গ',
    '¾': 'জ্জ',
    '¿': '্ত্র',
    'À': 'জ্ঝ',
    'Á': 'জ্ঞ',
    'Â': 'ঞ্চ',
    'Ã': 'ঞ্ছ',
    'Ä': 'ঞ্জ',
    'Å': 'ঞ্ঝ',
    'Æ': 'ট্ট',
    'Ç': 'ড্ড',
    'È': 'ণ্ট',
    'É': 'ণ্ঠ',
    'Ê': 'ণ্ড',
    'Ë': 'ত্ত',
    'Ì': 'ত্থ',
    'Î': 'ত্র',
    'Ï': 'দ্দ',
    'Ð': 'ণ্ড',
    'Ñ': '-',
    'Ò': '"',
    'Ó': '"',
    'Ô': "'",
    'Õ': "'",
    '×': 'দ্ধ',
    'Ø': 'দ্ব',
    'Ù': 'দ্ম',
    'Ú': 'ন্ঠ',
    'Û': 'ন্ড',
    'Ü': 'ন্ধ',
    'Ý': 'ন্স',
    'Þ': 'প্ট',
    'ß': 'প্ত',
    'à': 'প্প',
    'á': 'প্স',
    'â': 'ব্জ',
    'ã': 'ব্দ',
    'ä': 'ব্ধ',
    'å': 'ভ্র',
    'æ': 'ম্ন',
    'ç': 'ম্ফ',
    'é': 'ল্ক',
    'ê': 'ল্গ',
    'ë': 'ল্ট',
    'ì': 'ল্ড',
    'í': 'ল্প',
    'î': 'ল্ফ',
    'ï': 'শু',
    'ð': 'শ্চ',
    'ñ': 'শ্ছ',
    'ò': 'ষ্ণ',
    'ó': 'ষ্ট',
    'ô': 'ষ্ঠ',
    'õ': 'ষ্ফ',
    'ö': 'স্খ',
    '÷': 'স্ট',
    'ø': 'স্ন',
    'ù': 'স্ফ',
    'û': 'হু',
    'ü': 'হৃ',
    'ý': 'হ্ন',
    'þ': 'হ্ম'
}

PRE_SYMBOLS_MAP = {
    '®': 'ষ্',
    '¯': 'স্',
    '”': 'চ্',
    '˜': 'দ্',
    '™': 'দ্',
    'š': 'ন্',
    '›': 'ন্',
    '¤': 'ম্',

}

REFF = {
    '©': 'র্',
}

POST_SYMBOLS_MAP = {
    '&': '্‌',
    'ú': '্প',
    'è': '্ন',
    '^': '্ব',
    '‘': '্তু',
    '’': '্থ',
    '‹': '্ক',
    'Œ': '্ক্র',
    '—': '্ত',
    'Í': '্ত',
    'œ': '্ন',
    'Ÿ': '্ব',
    '¡': '্ব',
    '¢': '্ভ',
    '£': '্ভ্র',
    '¥': '্ম',
    '¦': '্ব',
    '§': '্ম',
    '¨': '্য',
    'ª': '্র',
    '«': '্র',
    '¬': '্ল',
    '­': '্ল',
    'Ö': '্র',

}

KAARS = {
    'v': 'া',
    'w': 'ি',
    'x': 'ী',
    'y': 'ু',
    'z': 'ু',
    '“': 'ু',
    '–': 'ু',
    '~': 'ূ',
    'ƒ': 'ূ',
    '‚': 'ূ',
    '„': 'ৃ',
    '…': 'ৃ',
    '†': 'ে',
    '‡': 'ে',
    'ˆ': 'ৈ',
    '‰': 'ৈ',
    'Š': 'ৗ'
}

KAAR_POST_CONVERSION = {
    "ো": "ো",
    "ৌ": "ৌ",

}

POST_CONVERSION_MAP = {
    # '০ঃ': '০:',
    # '১ঃ': '১:',
    # '২ঃ': '২:',
    # '৩ঃ': '৩:',
    # '৪ঃ': '৪:',
    # '৫ঃ': '৫:',
    # '৬ঃ': '৬:',
    # '৭ঃ': '৭:',
    # '৮ঃ': '৮:',
    # '৯ঃ': '৯:',
    # ' ঃ': ' :',
    # '\nঃ': '\n:',
    # ']ঃ': ']:',
    # '\\[ঃ': '\\[:',
    # '  ': ' ',
    'অা': 'আ',
    '্‌্‌': '্‌'
}

ALL_SYMBOLS = {**CONVERSION_MAP, **PRE_SYMBOLS_MAP, **POST_SYMBOLS_MAP}


def create_conversion_pattern(symbols):
    return '|'.join(sorted(re.escape(k)
                           for k in symbols))


SYMBOLS_CONVERSION_PATTERN = re.compile(r'({})'.format(
    create_conversion_pattern(ALL_SYMBOLS)),
    re.MULTILINE)

MAIN_CONVERSION_PATTERN = re.compile(r'([wx†‡ˆ‰Š]?)(({})*({})?({})*)({})?([vyz“–~ƒ‚„…]?)'.format(
    create_conversion_pattern(PRE_SYMBOLS_MAP),
    create_conversion_pattern(CONVERSION_MAP),
    create_conversion_pattern(POST_SYMBOLS_MAP),
    create_conversion_pattern(REFF)),
    re.MULTILINE)

HASAANT_PATTERN = re.compile(r'({})+'.format(re.escape('্')), re.MULTILINE)

PRE_CONVERSION_PATTERN = re.compile(r'({})'.format(
    create_conversion_pattern(PRE_CONVERSION_MAP)), re.MULTILINE)

POST_CONVERSION_PATTERN = re.compile(r'({})'.format(
    create_conversion_pattern(POST_CONVERSION_MAP)), re.MULTILINE)


def replace_symbol(m):
    return ALL_SYMBOLS.get(m.group(0), "")


def main_converter(match):
    """Main Conversion Function"""
    core = SYMBOLS_CONVERSION_PATTERN.sub(replace_symbol, match.group(2))
    core = HASAANT_PATTERN.sub(lambda m: "্", core)
    pre_kaar = post_kaar = None
    if match.group(1):
        pre_kaar = KAARS.get(match.group(1))
    if match.group(6):
        core = "র্" + core
    if match.group(7):
        post_kaar = KAARS.get(match.group(7))
    kaar_string = f'{pre_kaar if pre_kaar else ""}{post_kaar if post_kaar else ""}'
    core = core + KAAR_POST_CONVERSION.get(kaar_string, kaar_string)
    return core


def bijoy2unicode(string):
    converted_text = PRE_CONVERSION_PATTERN.sub(
        lambda m: PRE_CONVERSION_MAP.get(m.group(0)), string)
    converted_text = MAIN_CONVERSION_PATTERN.sub(
        main_converter, converted_text)
    converted_text = POST_CONVERSION_PATTERN.sub(
        lambda m: POST_CONVERSION_MAP.get(m.group(0)), converted_text)
    return converted_text
