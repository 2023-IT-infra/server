# Python 3.11 이미지 사용
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /code

# 필요한 패키지 설치
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


# 애플리케이션 코드 복사
COPY . /code

# 포트 오픈
EXPOSE 8000

# 개발용
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]