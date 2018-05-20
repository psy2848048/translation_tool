# MyCAT Tool 코드를 설명해보겠습니다.

```shell
mycattool
├─ app
│	└─ modules
├─ configs
├─ requirements.txt
└─ run.py
```



## Configuration

```shell
configs
├── __init__.py
├── cert_key
│   ├── pfx.mycattool_com.crt
│   └── pfx.mycattool_com.key
└── google_client_secret.json
```



#### Configuration 설정하기

1. configs/\__init__.py로 이동
2. Config 클래스에 필요한 값들 설정한다.
3. Config 클래스를 ProdConfig, DevConfig, TestConfig에 상속시킨다.
4. 각 환경에 따라 필요한 값으로 설정해준다.



#### Configuration 적용하기

1. 환경변수 `PURPOSE`를 PROD 또는 DEV로 설정한다.
2. app/\__init__.py 에서 `PURPOSE`에 따라 어떤 Config 클래스를 상속받을지 설정한다.

```python
#: Configurations
import configs
# from configs import ProdConfig, DevConfig, Config

if os.environ.get('PURPOSE') == 'PROD':
    app.config.from_object(configs.ProdConfig)
elif os.environ.get('PURPOSE') == 'DEV':
    app.config.from_object(configs.DevConfig)
else:
    app.config.from_object(configs.Config)
```





## Modules

```shell
module
├─ __init__.py	# 폴더를 모듈로써 인식시키려면 반드시 필요
├─ urls.py
├─ controllers.py
	# 입력과 응답 값들만 오가도록, 최대한 간단하게
	# 요청 데이터, 사용자 권한 등 입력된 데이터 검사하는 작업만
└─ models.py
	# 데이터베이스 작업
	# 복잡한 작업은 다 여기서
```



### About Modules

```shell
app
├─ auth
	# 로컬, 페이스북, 구글 로그인 가능
	# 어떤 OAuth를 붙여도 social_callback()을 통하여 일괄 처리하도록 만듦
	# flask_login으로 사용자 세션 관리
├─ users
├─ mail
│   ├── __init__.py
│   └── templates
	# ciceron_server/simpleRequest 가져와서 리팩토링함
	# import app.mail as mail 또는 from app import mail 으로 호출하기
	# __init__.py, example.py 보면 도움이 될까요?.. 허허
├─ projects
├─ docs
├─ search
	# 검색하는 API는 하나로 처리하려고 따로 모듈로 만들었는데 아직 많이 허접합니다.
├─ static
├─ termbase
├─ trans_memory
├─ workbench
├─ __init__.py
└─ common.py
	# 여러 모듈에서 쓰이는, 추후에 다른 프로젝트에서도 잘 쓰일 함수를 모아놨습니다.
```

[마이캣툴 API](https://docs.google.com/document/d/1TsqcnW4W-_cK1vxvjQGAw5ib5F0qjAyrwJ4HTAYb_JI/edit?usp=sharing) 문서에 각 모듈별로 할 수 있는 기능들을 모아서 작성했습니다. `-`로 구분해둠!

