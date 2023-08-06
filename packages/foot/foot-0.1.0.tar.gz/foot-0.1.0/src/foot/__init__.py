#!/usr/bin/env python3

import argparse
import asyncio
from datetime import datetime

import aiohttp

from . import sillywalks


def get_args():
    parser = argparse.ArgumentParser(description="foot")
    parser.add_argument(
        "-u", "--urls", type=str, help="Url", required=False, default=False
    )
    parser.add_argument(
        "-f", "--file", type=str, help="Filename", required=False, default=False
    )
    parser.add_argument(
        "-c", "--chunk", type=int, help="Chunk Size", required=False, default=False
    )
    parser.add_argument(
        "--recursive", help="Recursive", action="store_true", default=False
    )

    return parser.parse_args()


async def fetcher(session, url, recursive):
    print(f"Fetching: {url}")
    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                result = f"{url} : {resp.status}"
                print(result)
                return None
            else:
                data = await http_data(url=url, resp=resp, recursive=recursive)
                return data
    except aiohttp.client_exceptions.ClientConnectionError:
        print(f"Not found: {url}")


def multidict_convert(multidict):
    dict = {}
    for key in multidict:
        dict[key] = multidict[key]
    return dict


async def http_data(url, resp, recursive):
    status = resp.status
    headers = multidict_convert(resp.headers)
    cookies = multidict_convert(resp.cookies)
    html = await resp.read()

    aiohttp_data = {
        "status": status,
        "headers": headers,
        "cookies": cookies,
        "html": html,
    }

    walk_data = sillywalks.walk(url=url, data=aiohttp_data, recursive=recursive)
    return walk_data


async def fetching(session, urls, recursive):
    results = await asyncio.gather(
        *[
            asyncio.create_task(fetcher(session=session, url=url, recursive=recursive))
            for url in urls
        ]
    )
    return results


async def crawl(urls, chunk=10, recursive=False):
    refs = []
    async with aiohttp.ClientSession() as session:
        url_chunk = [urls[i : i + chunk] for i in range(0, len(urls), chunk)]
        for group in url_chunk:
            data = await fetching(session=session, urls=group, recursive=recursive)
            if data:
                for items in data:
                    if type(items) is list:
                        for item in items:
                            refs.append(item)
                    elif type(items) is str:
                        refs.append(items)
    if refs:
        refs = list(set(refs))
        await crawl(urls=refs, recursive=False)

        date_string = datetime.now().strftime("%Y%m%d-%H%M")
        with open(f"./foot/foot-{date_string}.txt", "w") as file:
            for url in refs:
                file.write(f"{url}\n")


def file(filename, chunk=10, recursive=False):
    with open(filename) as file:
        urls = file.read().splitlines()
    asyncio.run(crawl(urls=urls, chunk=chunk, recursive=recursive))


def get(urls, chunk=10, recursive=False):
    if type(urls) is not list:
        urls = list(map(str.strip, urls.split(",")))
    asyncio.run(crawl(urls=urls, chunk=chunk, recursive=recursive))


def cli():
    args = get_args()
    if args.urls:
        if args.chunk and args.recursive:
            get(urls=args.urls, chunk=args.chunk, recursive=args.recursive)
        elif args.chunk:
            get(urls=args.urls, chunk=args.chunk)
        elif args.recursive:
            get(urls=args.urls, recursive=args.recursive)
        else:
            get(urls=args.urls)
    elif args.file:
        if args.chunk and args.recursive:
            file(filename=args.file, chunk=args.chunk, recursive=args.recursive)
        elif args.chunk:
            file(filename=args.file, chunk=args.chunk)
        elif args.recursive:
            file(filename=args.file, recursive=args.recursive)
        else:
            file(filename=args.file)
    else:
        print("Please supply a list of URLs (-u) or filename (-f)")


if __name__ == "__main__":
    cli()
