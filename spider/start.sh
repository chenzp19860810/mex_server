#!/usr/bin/env bash

cd /www/web/api.geekjb.cn/venv/webblog && source bin/activate && cd /www/web/api.geekjb.cn/webblog/spider && scrapy crawl japonx && deactivate