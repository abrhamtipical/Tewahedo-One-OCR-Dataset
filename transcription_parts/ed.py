import sys,io
def ed(p,pairs):
    s=open(p,encoding='utf-8').read()
    for a,b in pairs:
        assert s.count(a)==1,(a,s.count(a))
        s=s.replace(a,b)
    open(p,'w',encoding='utf-8').write(s)
