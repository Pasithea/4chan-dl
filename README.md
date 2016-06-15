# 4chan-dl
A 4chan images downloader with CLI.
Multi-threading supported.

## Install
    python setup.py install

## Sample usage
    $ 4chan-dl -b w -t 1565459 --download
    $ 4chan-dl -b w -t 1565459 --download --threads 10 --path ./4chan

## Use proxy
* `--http-proxy https://127.0.0.1:9000`
* `--socks5-proxy 127.0.0.1 1080`

## Utils
    See `--help`

## License
    MIT