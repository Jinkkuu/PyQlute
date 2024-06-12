import requests
def submit_score(perf,combo,beatmapid,beatmapsetid,max,great,meh,bad,difficulty,mods,maxperf,taken):
    global oldstats,issubmiting
    oldstats=[totperf,totscore,totacc,level] # type: ignore
    print('Submitting Score...')
    template=str(p2[beatsel].replace('\n','-'))+';'+str(perf)+';'+str(combo)+';'+str(beatmapid)+';'+str(beatmapsetid)+';'+str(max)+';'+str(great)+';'+str(meh)+';'+str(bad)+';'+str(difficulty)+';'+str(mods)+';'+str(maxperf)+';'+str(taken) # type: ignore
    f=requests.get(settingskeystore['apiurl']+'api/submitscore?'+str(settingskeystore['username'])+';'+str(settingskeystore['password'])+';'+str(template),headers={'User-Agent': 'QluteClient-'+str(gamever)},timeout=10) # type: ignore
    f=f.text
    reloadprofile() # type: ignore
    issubmiting=0
    if f!='':
        print(f.rstrip('\n'))
        notification('QlutaBot',desc=f.rstrip('\n')) # type: ignore
