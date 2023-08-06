# -*- coding: utf-8 -*-
# This file is part of fintie.

# Copyright (C) 2018-present qytz <hhhhhf@foxmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""提供分红送配股信息查询

信息获取通道包括：

    * https://xueqiu.com/S/SZ002353/GBJG

加载已保存的数据::

    import pandas as pd
    from pathlib import Path

    df = pd.read_json(Path('xxx.json')
"""
import os
import time
import json
import asyncio
import logging
from pathlib import Path
from datetime import date

import click
import pandas as pd

from .cli import stock_cli_group, MODULE_DATA_DIR
from ..env import _init_in_session
from ..utils import fetch_http_data, add_doc


logger = logging.getLogger(__file__)
__all__ = ["async_get_guben", "get_guben"]


async def _init(session, force=False):
    if force or not _init_in_session.get("xueqiu"):
        _init_in_session["xueqiu"] = True
        await session.get("https://xueqiu.com")
    return True


async def async_get_guben(session, symbol, data_path=None, return_df=True):
    """
    从雪球获取分红送配股数据

    :param session: `aiohttp.ClientSession` 对象，同步接口不需要传
    :param symbol: 股票代码
    :param data_path: 数据保存路径
    :param return_df: 是否返回 `pandas.DataFrame` 对象，False 返回原始数据

    :returns: 原始数据或 `pandas.DataFrame` 对象，见 return_df 参数，
              失败则返回 `None`
    """
    await _init(session)

    page_size = 10000
    curr_page = 1
    params = {"_": 0, "symbol": symbol, "page": curr_page, "size": page_size}

    logger.info("start download guben from xueqiu for %s...", symbol)
    url = "https://xueqiu.com/stock/f10/shareschg.json"
    params["_"] = int(time.time() * 1000)

    date_str = str(date.today())
    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            logger.warning("get guben from %s failed: %s", url, resp.status)
            return None
        data = await resp.json()
        if "list" not in data:
            logger.warn("no guben data downloaded for %s from %s: % ", symbol, url, data)
        guben_data = data["list"]

    if not guben_data:
        logger.warn("no guben data downloaded for %s from %s, return None", symbol, url)
        return None

    logger.info("download guben for %s from %s finish", symbol, url)
    if data_path:
        data_path = Path(data_path) / MODULE_DATA_DIR / "guben"
        os.makedirs(data_path, exist_ok=True)
        data_fname = "-".join((symbol, date_str)) + ".json"
        data_file = data_path / data_fname
        with data_file.open("w", encoding="utf-8") as dataf:
            json.dump(guben_data, dataf, indent=4, ensure_ascii=False)

    if not return_df:
        return guben_data

    df = pd.DataFrame(guben_data)
    # set index
    # df.set_index("bonusimpdate", inplace=True)
    return df


@add_doc(async_get_guben.__doc__)
def get_guben(*args, **kwargs):
    ret = fetch_http_data(async_get_guben, *args, **kwargs)
    if isinstance(ret, Exception):
        raise ret
    return ret


@click.option("-s", "--symbol", required=True)
@click.option(
    "-f",
    "--save-path",
    type=click.Path(exists=False)
)
@click.option("-p/-np", "--print/--no-print", "show", default=True)
@stock_cli_group.command("guben")
@click.pass_context
def guben_cli(ctx, symbol, save_path, show):
    """从雪球获取股本数据"""
    if not save_path:
        save_path = ctx.obj["data_path"]
    data = get_guben(symbol, save_path)
    if show:
        click.echo(data)


if __name__ == "__main__":
    guben_cli()
