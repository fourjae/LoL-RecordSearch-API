from flask import Flask , request

import os
from multiprocessing import Pool

import requests
import json
from urllib import parse
import time
app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

response = requests.get("http://ddragon.leagueoflegends.com/cdn/11.9.1/data/ko_KR/summoner.json")
#스펠
spellnames = [
    "SummonerSmite", "SummonerHaste", "SummonerHeal", "SummonerTeleport",
    "SummonerBoost", "SummonerBarrier", "SummonerDot", "SummonerExhaust",
    "SummonerFlash", "SummonerMana","SummonerPoroRecall","SummonerPoroThrow",
    "SummonerSnowURFSnowball_Mark","SummonerSnowball"
]

res_spells = json.loads(response.text)
spells = {}

for i in spellnames:
    spells[res_spells["data"][i]["key"]] =  i

################################################################################### 스펠

championinfo = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/11.9.1/data/ko_KR/champion.json").text)

championsinfo = championinfo["data"].keys()

championkeys = {}
championkeyskorean={}
for i in championsinfo:
    championkeys[championinfo["data"][i]["key"]] = i

for j in championsinfo:
    championkeyskorean[championinfo["data"][j]["key"]] = championinfo["data"][j]["name"]
    #print(championinfo["data"][i]["key"], " : ", i)


################################################################################### 챔피언

iteminfo = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/11.9.1/data/ko_KR/item.json").text)

#for i in iteminfo['data'].keys():  # 아이템 키 ['name'](iteminfo['data'][str(i)]['name']) description , plaintext
    #print(i)
#print(iteminfo['data']['1001'])
#################################################################################### 아이템 + 이미지


runeinfo=json.loads(requests.get("https://ddragon.leagueoflegends.com/cdn/11.9.1/data/ko_KR/runesReforged.json").text)
runeinfos={}
for i in range(0,5):
    runeinfos[runeinfo[i]['id']]=runeinfo[i]['name']

##################################################################################### Rune
#for i in range(0,1):
#print(res_spells["data"])
#"{"type":"summoner","version":"11.6.1","data":{"SummonerBarrier":{"id":"SummonerBarrier","name":"Barrier","description":"Shields your champion from 115-455 damage (depending on champion level) for 2 seconds.","tooltip":"Temporarily shields {{ f1 }} damage from your champion for 2 seconds.","maxrank":1,"cooldown":[180],"cooldownBurn":"180","cost":[0],"costBurn":"0","datavalues":{},"effect":[null,[95],[20],[0],[0],[0],[0],[0],[0],[0],[0]],"effectBurn":[null,"95","20","0","0","0","0","0","0","0","0"],"vars":[],"key":"21","summonerLevel":4,"modes":["CLASSIC","ARAM","FIRSTBLOOD","TUTORIAL","STARGUARDIAN","PROJECT","ARSR","ASSASSINATE","DOOMBOTSTEEMO","ONEFORALL","PRACTICETOOL","URF","NEXUSBLITZ"],"costType":"No Cost","maxammo":"-1","range":[1200],"rangeBurn":"1200","image":{"full":"SummonerBarrier.png","sprite":"spell0.png","group":"spell","x":0,"y":0,"w":48,"h":48},"resource":"No Cost"}"
####################################################################################################################################################################################
def status_code(status):
    if (status != 200):
        #존재하지 않는 소환사
        return 1
    else:
        return 0

def match_id(accountid):
    if (accountid == ''):
        return 1
    else:
        return 0

def insertruneinfo(types,runecount,dic):
    tempreturnstats={}
    if runecount==4:
        count=0
        tempreturnstats["mainrune"]=runeinfo[types]["name"]
        tempreturnstats["mainruneing"]='https://ddragon.canisback.com/img/'+runeinfo[types]['icon']
    else:
        count=4
        tempreturnstats["subrune"]=runeinfo[types]["name"]
        tempreturnstats["subnruneing"]='https://ddragon.canisback.com/img/'+runeinfo[types]['icon']
    
    for i in dic.values():
        for j in range(0,runecount):
            for q in range(0,len(runeinfo[types]['slots'][j]['runes'])):
                if i == runeinfo[types]['slots'][j]['runes'][q]['id']:
                    tempreturnstats['perk'+str(count)+'img']='https://ddragon.canisback.com/img/'+runeinfo[types]['slots'][j]['runes'][q]['icon']
                    tempreturnstats['perk'+str(count)+'name']=runeinfo[types]['slots'][j]['runes'][q]['name']
                    #tempreturnstats['perk'+str(count)+'longDesc']=runeinfo[types]['slots'][j]['runes'][q]['longDesc']
                    
                    count+=1
                    break;

    return tempreturnstats;

def perkruneinfo(key,value,dic):
    if key=="perkPrimaryStyle":
        runecount=4
    else:
        runecount=3
    if value==8000:
        return insertruneinfo(2,runecount,dic) 
    if value==8100:
        return insertruneinfo(0,runecount,dic)
    if value==8200:
        return insertruneinfo(4,runecount,dic)
    if value==8300:
        return insertruneinfo(1,runecount,dic)
    if value==8400:
        return insertruneinfo(3,runecount,dic)
    
def users_info(key,value):
    returnstats={}
    rune={}
    if key=="participantId":
        return str(value)+" pick"

    if key=="teamId":
        if int(value)==100:
            return "Blue Team"
        else:
            return "Purple Team"  

    if key=="championId":     #이미 만들어둔 챔프 목록 함수에서 가져옵니다.
        returnstats['champion']=championkeyskorean[str(value)]
        returnstats['championimg']="https://ddragon.leagueoflegends.com/cdn/11.9.1/img/champion/"+championkeys[str(value)]+".png"
        return returnstats

    if key=="spell1Id" or key=="spell2Id":  #이미 만들어둔 스펠 목록 함수에서 가져옵니다.
        returnstats['spell1Id']=spells[str(value)]
        returnstats['spell1Idimg']="https://ddragon.leagueoflegends.com/cdn/11.9.1/img/spell/"+spells[str(value)]+".png"
        returnstats['spell2Id']=spells[str(value)]
        returnstats['spell2Idimg']="https://ddragon.leagueoflegends.com/cdn/11.9.1/img/spell/"+spells[str(value)]+".png"
        return returnstats   

    if key=="stats":
        stats=dict(value)
        for i in stats:
            #print(i,stats[str(i)])
            if i=="win":
                returnstats['win']=stats[str(i)]
            if "item" in i:
                for _ in range(6):
                    if stats[i]==0:
                        returnstats[str(i)]=''
                        returnstats[str(i)+'img']="#"
                    else:
                        returnstats[str(i)]=iteminfo['data'][str(stats[i])]['name']#+"\n"#+iteminfo['data'][str(stats[i])]['description']
                        #returnstats[str(i)+'gold']=iteminfo['data'][str(stats[i])]['gold']
                        returnstats[str(i)+'img']="https://ddragon.leagueoflegends.com/cdn/11.9.1/img/item/"+str(stats[i])+".png"

            if i=="kills" or i=="deaths" or i=="assists" or i=="largestMultiKill" or i=="doubleKills" or i=="tripleKills" or i=="quadraKills" or i=="pentaKills" or i=="totalDamageDealtToChampions" or i=="visionScore" or i=="goldEarned" or i=="goldSpent" or i=="turretKills" or i=="totalMinionsKilled" or i=="neutralMinionsKilled" or i=="champLevel" or i =="visionWardsBoughtInGame" or i == "sightWardsBoughtInGame" or i == "firstBloodKill":
                returnstats[str(i)]=stats[str(i)]
            if i=="perk0" or i=="perk1" or i=="perk2" or i=="perk3" or i=="perk4" or i=="perk5":
                returnstats[str(i)]=stats[str(i)]
            
                #returnstats[str(i)+'img']="https://ddragon.canisback.com/img/perk-images/Styles"+"_Domination.png"

            if i== "perkPrimaryStyle":
                returnstats[str(i)]=stats[str(i)]
                rune['perk0']=returnstats['perk0']
                rune['perk1']=returnstats['perk1']
                rune['perk2']=returnstats['perk2']
                rune['perk3']=returnstats['perk3']
                returnstats['perkPrimary']=perkruneinfo(i,stats[str(i)],rune)
            
            if i=="perkSubStyle":
                returnstats[str(i)]=stats[str(i)]
                rune['perk4']=returnstats['perk4']
                rune['perk5']=returnstats['perk5']
                returnstats['perkSub']=perkruneinfo(i,stats[str(i)],rune)
        return returnstats;

    if key=="timeline":
        stats=dict(value)
        returnstats['role']=stats['role']
        returnstats['lane']=stats['lane']
        return returnstats

def timestamp(gametime):
    if gametime<60:
    	return {"timedate":str(int(gametime))+"초 전"};
    elif gametime>60 and gametime<3600:
        return {"timedate":str(int(gametime//60))+"분 전"};
    elif gametime>3600 and gametime<86400:
        return {"timedate":str(int(gametime//3600))+"시간 전"};
    else:
    	return {"timedate":str(int(gametime//86400))+"일 전"};
    
def multi_run_wrapper(args):
    return API(*args)

def summoner_info_rank(num,searchsummoner):
    summonerinforank=[]
    if num==0 or num==1:
        summonerinforank.append(searchsummoner[num]['queueType'])
        summonerinforank.append(searchsummoner[num]['tier'])
        summonerinforank.append(searchsummoner[num]['leaguePoints'])
        summonerinforank.append(searchsummoner[num]['wins'])
        summonerinforank.append(searchsummoner[num]['losses'])
        return summonerinforank
    elif num==2:
        summonerinforank.append(searchsummoner['name'])
        summonerinforank.append(searchsummoner['profileIconId'])
        summonerinforank.append(searchsummoner['summonerLevel'])
        return summonerinforank

def API(gameId,SummonerName,api_key,gamecount,accountId):
    time.sleep(0.5)
    start = time.time()
    returndata=[]         # 전적 리턴용
    returntemp={}
    if (match_id(gameId)):
        pass
    else:
        response2 = requests.get("https://kr.api.riotgames.com/lol/match/v4/matches/" + str(gameId) + "?api_key=" + api_key)
        print(response2.status_code)
        res2 = json.loads(response2.text)
        ############################################## 정리 ###################################################
        returndata.append(timestamp(start-res2["gameCreation"]/1000))
        minute = 0
        seconds = 0
        minute = res2["gameDuration"] // 60 
        seconds = res2["gameDuration"] % 60
        returndata.append({"Gameinfo":gamecount+1})
        #print("=============================게임 정보=============================")
        returndata.append({"GameTime":(minute,seconds)})
        #print("게임 시간 : ", minute, "분", seconds, "초")

        if (res2["queueId"] == 420):  # http://static.developer.riotgames.com/docs/lol/queues.json 큐 종류
            returndata.append({"queueid":"5v5 Ranked Solo games"})

        if (res2["queueId"] == 450): 
            returndata.append({"queueid":"5v5 ARAM games"})

        if (res2["queueId"] == 440):
            returndata.append({"queueid":"5v5 Ranked Flex games"})

        for i in range(10):  # 어차피 롤은 10명이 최대니까 10번만 돌림SummonerName=SummonerName.replace(" ","")
            if ((res2["participantIdentities"][i]["player"]["accountId"] == accountId) and (res2["participantIdentities"][i]["player"]["summonerName"].replace(" ","") == SummonerName)):
                denId = (res2["participantIdentities"][i]["participantId"])

                #print("게임 픽순 : ",      denId)
                returndata.append({"reqsummonername":res2["participantIdentities"][i]['player']['summonerName']})
                returndata.append({"searchuserpick":str(denId)+" pick"})
                break
        Summonerinfo = res2["participants"][denId-1]

        if (Summonerinfo["teamId"] == 100):
            #print("게임 팀 : ", "blue")
            returndata.append({"searchuserpickteam":"blue"})
        elif (Summonerinfo["teamId"] == 200):
            #print("게임 팀 : ", "purple")   
            returndata.append({"searchuserpickteam":"purple"})
        teams_info=res2["teams"]
        #del teams_info['teams'][0]['bans']
        #####팀 별 나눠 구분
        for i in range(2):  ##### 두 팀 밖에 없으니 두 번
            for j in teams_info[i]: #####배열 형식의 길이는 객체 하나이므로 객체 자체만 받아와 그 len을 반복
                    #print(j,":",teams_info[i][j])
                returntemp[j]=teams_info[i][j]
                #print("\n\n")
            returndata.append(returntemp)
            returntemp={}
        
        returnarray=[]      # 다음 10명 정보 담을 때만 사용합니다.
        timelinesort=[]
        returnarraysort=[]
        returnarraycollection=[]
        timelineres=requests.get("https://kr.api.riotgames.com/lol/match/v4/timelines/by-match/"+ str(gameId) +"?api_key="+api_key)
        print(timelineres.status_code,gamecount)
        timelineress=json.loads(timelineres.text)
        for i in range(10): ## 10명임
            participants_info=res2["participants"][i]
            returnarray.append({"summonercdname":res2["participantIdentities"][i]['player']['summonerName']})
            for j in participants_info:
                # 유저 정보는 다음 함수에서 실행합니다.
                returnarray.append(users_info(j, participants_info[j]))
            returnarraycollection.append(returnarray)
            returnarray=[]
        
        for i in range(1,11):
            timelinesort.append(timelineress['frames'][0]['participantFrames'][str(i)]['participantId'])
            

        #for i in range(10):
    	#    timelinesort.append(timelineres["participants"][i]["timeline"]['role'],timelineres["participants"][i]["timeline"]['lane'])
        #[2, 3, 4, 1, 5, 9, 7, 6, 8, 10]
        for j in timelinesort:
            returnarraysort.append(returnarraycollection[j-1])
        returndata.append(returnarraysort)
        time.sleep(0.1)
        return returndata
        returndata=[]
        
#####################################################################################################################################################################################
@app.route('/')
def main():
    mainReturn=[]
    pool = Pool(os.cpu_count())          # 돌릴 process 준비  # 현재 서버의 CPU 수
    start = time.time()
    TrollScore = [0] * 30
    api_key = "" #라이엇 API 발급 키 (RGAPI)
    #SummonerName = "예시 이름"
    SummonerName = request.args.get('summonername',)
    SummonerName=SummonerName.replace(" ","")
    
    if SummonerName =='':
        return {"400":"not user"}
    
    response0 = requests.get("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + parse.quote(SummonerName) + "?api_key=" + api_key)
    status = response0.status_code

    if status==404:
        return {"404":"Data not found - summoner not found"}   
    ################################################################################### 전적 검색할 소환사 명 api 요청
    else:
        res0 = json.loads(response0.text)  #ID 가져오기
        accountId = res0["accountId"]
        encid=res0["id"]
        
        ################################################################################### match ID 가져오기
        response1 = requests.get("https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountId + "?api_key=" + api_key)  # 최근 100게임 가져오기
        resgame1 = json.loads(response1.text)
        #for문 30회 돌려야함. 30 게임만 가져오기
        if len(resgame1["matches"])>=30:
            allgamecount=30
        else:
            allgamecount=len(resgame1["matches"])
      
    ################################################################################### match ID 가져왔음 가장 최근 위에거 가져옴 match 안의 0번째 gamdId
    allGameReturn=[]
    renewal=[]
    for q in range(allgamecount):
        renewal.append((resgame1["matches"][q]["gameId"],SummonerName,api_key,q,accountId))
    results = pool.map(multi_run_wrapper,(renewal))
    
    pool.close()
    end = time.time()
    print(end-start)
    
    ##################################### 전적 갱신자 티어 갱신 ##################################################
    summonerinfoetc=[]
    response = requests.get("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-account/" + accountId + "?api_key=" + api_key)
    searchsummoner=json.loads(response.text)
    summonerinfoetc.append(summoner_info_rank(2,searchsummoner))

    response = requests.get("https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+encid+"?api_key="+api_key)
    searchsummoner=json.loads(response.text)
    summonerinfoetc.append(summoner_info_rank(0,searchsummoner))
    summonerinfoetc.append(summoner_info_rank(1,searchsummoner))
    results.append(summonerinfoetc)

    return {"200":results};

    
if __name__ == '__main__':
	app.run()