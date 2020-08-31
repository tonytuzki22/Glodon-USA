import re

str = '特   征： 1.名称:生活贮热水罐 2.规格:φ×H×L =1800×3560×2085mm，有效容积:8m3 ，设计压力0.25Mpa。'

pata = '(?<==)\d+(?=×)'
patb = '(?<==)(?:\s{0,3})\d+(?=[X, ×])'

str2a = '型号:WDZCN-BYJ-4'
str2b = '型号:BV-2.5'
str2c = '型号:WDZCN-BYJ-4*2.5'
str2d = 'BYJ-1200*20'
str2e = 'BYJ-1200.5*20'
str2f = 'BV-1200.1 * 20'

pat2a = '(?<=BYJ-|BV-)\d+(\.\d+)?(?!\*)'
pat2b = '(?<=BYJ-|BV-)\d+(\.\d+)?(?!\*|x)'
pat2c = '(?<=BYJ-|BV-)\d+(\.\d+)?(?!\*|x|\d)'
pat2d = '(?<=BYJ-|BV-)\d+(\.\d+)?(?!\*|x|\d|\.)'
pat2e = '(?<=BYJ-|BV-)\d+(\.\d+)?(?!\*|x|\d|\.|\s)'

pat3a = '(?<!BYJ-|\*|x|\d|\.)\d+(\.\d+)?(?!\*|x|\d|\.)'
pat3b = '(?<!BYJ-|\*|x|\d|\.|\s)\d+(\.\d+)?(?!\*|x|\d|\.|\s)'

"""
pat = '(=)(\d+)'
match = re.search(pat, str)
if match:
    print(match.group(2))


pat2 = '(\d+)(×)'
match2 = re.search(pat2, str)
if match2:
    print(match2.group(1))
"""