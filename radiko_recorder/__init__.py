import sys

if sys.version_info < (3, 8):
    raise ImportError(
        f'You are using an unsupported version of Python. Only Python versions 3.8 and above are supported by ihc_reporter') # noqa: F541

import argparse
import re
from datetime import datetime
from pathlib import Path

from .recorder import RadikoPlayer
from .config import RADIKO_AREA_ID

def record_radio(area_id: str, station_id: str, start_time: str, duration_minutes: int):
    '''
    ラジオを録音する
    
    Parameters
    ----------
    area_id : str
        エリアID
    station_id : str
        放送局ID
    start_time : str
        録音開始時間
    duration_minutes : int
        録音時間（分）
    '''
    # エリアIDのチェック
    if not _is_valid_area_id(area_id):
        raise ValueError(f"Invalid area ID: {area_id}")
    
    # 出力ファイルのパス
    OUTPUT_DIR = Path("output")
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f'{station_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.aac'
    
    # ラジオを録音
    player = RadikoPlayer(area_id=area_id)
    player.record(
        station_id=station_id,
        start_time=datetime.strptime(start_time, '%Y%m%d%H%M%S'),
        duration_minutes=duration_minutes,
        output_path=output_path
    )

def _show_station_list(area_id: str):
    '''
    放送局リストを表示する
    
    Parameters
    ----------
    area_id : str
        エリアID
    '''
    # エリアIDのチェック
    if not _is_valid_area_id(area_id):
        raise ValueError(f"Invalid area ID: {area_id}")
    
    player = RadikoPlayer(area_id=area_id)
    station_list = player.get_station_list()
    for station in station_list:
        print(f"{station['id']}: {station['name']}")

def _is_valid_area_id(area_id: str) -> bool:
    '''
    エリアIDが有効かどうかを判定する
    
    Parameters
    ----------
    area_id : str
        エリアID
    
    Returns
    -------
    bool
        有効なエリアIDかどうか
    '''
    # エリアIDの正規表現パターン
    pattern = r'^JP([1-9]|[1-3][0-9]|4[0-7])$'
    return re.match(pattern, area_id) is not None

def init_parser() -> argparse.ArgumentParser:
    '''
    コマンドライン引数を解析するためのパーサーを初期化する
    
    Returns
    -------
    parser : argparse.ArgumentParser
        パーサー
    '''
    parser = argparse.ArgumentParser(description='Radiko Recorder')
    parser.add_argument('-a', '--area_id', type=str, help='Area ID (JP13, JP27, etc.)', default=RADIKO_AREA_ID)
    parser.add_argument('-s', '--station_list', action='store_true', help='Show station list')
    parser.add_argument('station_id', type=str, nargs='?', help='Station ID')
    parser.add_argument('start_time', type=str, nargs='?', help='Start time (YYYYMMDDHHMMSS)')
    parser.add_argument('duration_minutes', type=int, nargs='?', help='Duration (minutes)', default=60)
    return parser

def _check_args(args: argparse.Namespace) -> bool:
    '''
    必須引数が提供されているかをチェックする
    
    Parameters
    ----------
    args : argparse.Namespace
        コマンドライン引数
    
    Returns
    -------
    bool
        必須引数が提供されているかどうか
    '''
    return all([args.station_id, args.start_time, args.duration_minutes])

def main(argv=None):
    '''
    メイン関数
    '''
    parser = init_parser()
    args = parser.parse_args(argv)
    
    if args.station_list:
        try:
            # 放送局リストを表示
            _show_station_list(args.area_id)
        except ValueError as e:
            print(e)
        return
    
    # 必須引数のチェック
    if not _check_args(args):
        parser.print_usage()
        print("Station ID, start time, and duration minutes are required unless using the --station-list option.")
        return
    
    # ラジオを録音
    record_radio(
        area_id=args.area_id,
        station_id=args.station_id,
        start_time=args.start_time,
        duration_minutes=args.duration_minutes
    )

__all__ = [
    'main'
]