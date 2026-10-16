import re,collections
per=collections.defaultdict(collections.Counter)
for l in open('/home/user/PreMerge/docs/review3/logs/mutmut_results.txt'):
    m=re.match(r'\s*premerge\.(\w+)\.\S+:\s*(\w+)',l)
    if m: per[m.group(1)][m.group(2)]+=1
print(f'{"module":12}{"killed":>8}{"survived":>10}{"no tests":>10}{"score":>8}')
tk=ts=tn=0
for k,v in sorted(per.items()):
    kk,s,n=v['killed'],v['survived'],v['no']; tk+=kk;ts+=s;tn+=n
    print(f'{k:12}{kk:8}{s:10}{n:10}{kk/(kk+s+n):8.0%}')
print(f'{"TOTAL":12}{tk:8}{ts:10}{tn:10}{tk/(tk+ts+tn):8.0%}')
