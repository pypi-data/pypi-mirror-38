paspas [![Build Status](https://travis-ci.org/hirokikana/paspas.svg?branch=master)](https://travis-ci.org/hirokikana/paspas)
====

## Description
paspas is simple password generator for CLI.

## Install

```
pip install paspas
```

## Usage
```
$ paspas --help
```

```
$ paspas --site=google --user=bob --master=secret
```

site settings and master password is yaml format. setting save to `~/.paspas` .
```
master_password: secret
google:
 max_length: 30
 unavailable_char: !@#
```

optional argument
```
  -s SITE, --site SITE        site name
  -u USER, --user USER        user name
  -m MASTER, --master MASTER  master password
```
