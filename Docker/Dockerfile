FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-devel

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt --index-url https://mirrors.sustech.edu.cn/pypi/web/simple/
# RUN python3 -m pip install flash-attn --no-build-isolation --index-url https://mirrors.sustech.edu.cn/pypi/web/simple/

WORKDIR /src
