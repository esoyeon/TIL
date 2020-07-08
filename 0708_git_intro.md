# git intro

## local git

1. 초기화 `$ git init`

   1. 실제로는 '.git' 폴더가 생성됨

   2. 버전관리가 시작됨

   3. repo(리포: repository)라고 부름 

      

2. 서명 설정 

   1. `$git config --global user.name "name"`

   2. `$git config --global user.email "any email"`

      

3. 리포의 상태보기`$ git status`

   빨간 색: 바뀌었지만 스테이지에 안 올라왔다. 

4. stage에 올리기 `$git add`

   1. 특정 파일만 올리기 `$git add <file name>`
   2. 내 위치 폴더 다 올리기 `$ git add .

5. snapshot 찍기 `$git commit`

   ​	`commit -m`: -m은 message라는 뜻

6. 로그(git의 사진첩)보기 `$git log`

## github

1. 원격저장소(remote repository) 생성

2. 로컬 리포 ==> 리모트 리포 

   `$ git remote add origin <url>`

3. 로컬 커밋들을 remote로 보내기

   `$git push origin master`

4. `$git push` ==> `$git push origin master`로 단축명령하기

   `$git push -u origin master`

5. 다른 컴퓨터에서 remote repo **최초**로 받아오기

   `$ git clone <url>`

6. 이후 remote repo 변경사항을 local repo에서 반영하기 

   `$git pull`

## TIL 관리 시나리오

1. 멀캠
2. `$git pull`
3. 중간중간`$git add .` & `$git commit`

4. 집 가기 전에 `$git push`

5. 집 도착 `$git pull`
6. 복습 및 자습
7. 마지막으로 `$git push`