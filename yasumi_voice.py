#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import re
import time
from multiprocessing import Pool, Manager

# デバッグフラグ
DEBUG = True

# 音声合成の同時処理数
MAX_PROCESS = 3

# open_jtalkコマンドの場所
JTALK = '/usr/local/bin/open_jtalk'

# aplayコマンドの場所
APLAY = '/usr/bin/aplay'

# 辞書ディレクトリ
DICDIR = '/usr/local/dic'

# 音声ファイル

VOICE = '/home/pi/MMDAgent_Example-1.4/Voice/mei/mei_normal.htsvoice'

# 話す速度(標準 1.0。0.0以上の値を指定)
SPEED = 1.0

# additional half-tone
TONE = 2.0

# ボリューム
VOLUME = 10.0

# 作業ディレクトリ
WORKDIR = "/home/pi/"

#
# デバッグメッセージ出力用
#
def _print( message ):
        if DEBUG:
                print message

#
# 音声合成を実行する
#
def create_wav( t ):
        _print( "DEBUG: 音声作成開始[%d:%s]" % ( t[0], t[1] ) )
        # サブプロセス呼び出し
        outfile = WORKDIR + "talk%02d.wav" % t[0]
        c = subprocess.Popen([JTALK, '-x', DICDIR, '-m', VOICE, '-ow', outfile, '-r', str(SPEED), '-fm', str(TONE), '-g', str(VOLUME)], stdin=subprocess.PIPE)
        # 音声合成するテキストを入力
        c.stdin.write(t[1])
        # 終了を待つ
        c.stdin.close()
        c.wait()
        _print( "DEBUG: 音声作成終了[%d:%s]" % ( t[0], t[1] ) )
        t[2].put(t[0])
        return c.returncode

#
# 音声を(複数まとめて)再生する
#
def play_wav( listindex ):
        command = list()
        command.append(APLAY)
        command.append('-q')
        for index in listindex:
                command.append(WORKDIR + "talk%02d.wav" % index)
        return subprocess.Popen(command)

#######################################
# 入力
#######################################
# 引数を取り込み
argvs = sys.argv

# 簡単な引数チェック
if(len(argvs) != 2):
        print 'Usage: # %s textfile' % argvs[0]
        exit(1)

# 指定されたファイルを読み込み
alltext = ""
for line in open( argvs[1] ):
        alltext += line.rstrip()

# 音声合成の進捗を確認するためのキューを作成
queue = Manager().Queue()

# テキストを短文に分割。テキストに連番を振ってリストにしておく。
index = 0
arg = list()
shorttext = re.split(r'、|。', alltext)
for s in shorttext:
        if s != "":
                arg.append((index, s, queue))
                index += 1
_print( "DEBUG: %d個に分割しました。" % len(arg) )

#######################################
# 合成
#######################################
# プロセスプールを作成
p = Pool(MAX_PROCESS)

# 音声合成を開始
r = p.map_async( create_wav, arg )

# 音声合成の進捗リスト。0は未完了、1は音声合成済み。
l = [ 0 for i in range(len(arg))]

# 終端の判断のため-1を付加。
l.append(-1)

#######################################
# 再生
#######################################
# 現在再生中の音声のインデックス
nowplaying = -1

# 現在再生中のaplayコマンドのProcess
playing = None

# 進捗を確認しつつ音声を読み上げる
while ( not r.ready() ) or ( nowplaying != len(arg) ) or ( playing is not None ):
        time.sleep(0.5)
        # 音声合成の終了報告があるかキューを確認する。
        for _ in range(queue.qsize()):
                compiled_index = queue.get()
                l[compiled_index] = 1
        # 再生できるならしてみる？
        if nowplaying < len(arg):
                if playing is None:
                        if l[nowplaying + 1] == 1:
                                # まとめてWAVファイルを指定できるときはする
                                listindex = list()
                                while l[nowplaying + 1] == 1:
                                        nowplaying += 1
                                        listindex.append(nowplaying)
                                _print( "DEBUG: しゃべるよ！[%s]" % str(listindex) )
                                playing = play_wav(listindex)
                        elif l[nowplaying + 1] == 0:
                                _print( "DEBUG: 音声合成の完了待ちです！" )
                        else:
                                exit()
                else:
                        if playing.poll() is not None:
                                playing = None
