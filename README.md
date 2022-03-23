# lolsearch RestAPI(서비스 X)

### 1. 프로젝트 요약

프론트 개발자 1명과 함께 flask 서버를 이용해 만든 롤 최근 30 게임을 불러오는 전적검색 RestAPI

서버로 구축된 것은 아니며 구축 후 RestAPI로 사용할 수 있음.

### 2. 사용한 언어 및 라이브러리

Python(Flask,  request, multiprocessing)

### 3. 주요 기능

![image](https://user-images.githubusercontent.com/47708717/134893442-36522b7f-93b8-43c5-ac8a-46074e25b807.png)

![image](https://user-images.githubusercontent.com/47708717/134893680-3796ab94-6ceb-4d35-bcd7-7d913ba0a2a3.png)

![image](https://user-images.githubusercontent.com/47708717/134893714-ce62b3c2-01ac-4d7e-98ee-576421cf44e7.png)

### 4. 담당역할 및 성과



### 5. 레퍼런스
사용방법은 다음과 같습니다. 그 외 개조가능

309번째 줄의 api_key = "" 라이엇 API 발급 키 (RGAPI)를 받아 사용합니다.

311번째 줄의 SummonerName 변수에 검색할 아이디 값을 보내주면 끝!


## 발생 문제 및 해결방법

윈도우 서버(포트포워딩)에서 최근 30게임을 완전탐색으로 필요한 내용만 가져와도 30초가 걸렸습니다.

- **속도 개선**

  멀티프로세싱 모듈을 이용하여 노트북 코어의 수(4개) 만큼 병렬처리 한 결과 약 15초 까지 줄었습니다.

  파이썬 버전을 3.7.1 -> 3.9.5 업데이트 후 전적검색시 11초 까지 줄었습니다.



## **그 외 생각하는 문제점 및 느낀점**

데이터 가공 후 넘겨주는 JSON값을 프론트와 의논을 해야 합니다. (커뮤니케이션의 중요성)

데이터 가공상태가 최적화 되지 않아 DB 연동 후 데이터를 넣을 때 어려움이 있을 것이라 생각합니다. (최적화의 중요성)
