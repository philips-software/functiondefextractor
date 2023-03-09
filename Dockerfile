FROM amancevice/pandas:1.0.5-alpine

RUN apk add --update --no-cache grep ctags libstdc++

RUN pip3 install functiondefextractor

ENTRYPOINT [ "python", "-m", "functiondefextractor", "--p", "/usr/bin/code"]