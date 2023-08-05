"""Define request cmdlr used."""

import sys
from functools import reduce

import aiohttp

from ..log import logger
from ..merge import merge_dict


def build_request(
        analyzer, analyzer_system, session, global_semaphore, host_pool):
    """Get the request class."""
    max_try = analyzer_system['max_try']
    per_host_connections = analyzer_system['per_host_connections']
    delay = analyzer_system['delay']

    class request:
        """session.request contextmanager."""

        def __init__(self, url, **req_kwargs):
            """init."""
            self.req_kwargs = req_kwargs
            self.url = url

            self.resp = None
            self.host_semaphore_acquired = False
            self.global_semaphore_acquired = False

            host_pool.register_host(url, per_host_connections, delay)

        async def __acquire(self):
            self.host_semaphore_acquired = True
            await host_pool.acquire(self.url)

            self.global_semaphore_acquired = True
            await global_semaphore.acquire()

        def __release(self):
            if self.global_semaphore_acquired:
                self.global_semaphore_acquired = False
                global_semaphore.release()

            if self.host_semaphore_acquired:
                self.host_semaphore_acquired = False
                host_pool.release(self.url)

        async def __get_response(self):
            await self.__acquire()

            await host_pool.wait_for_delay(self.url)

            real_req_kwargs = reduce(
                merge_dict,
                [
                    analyzer.default_request_kwargs,
                    self.req_kwargs,
                    {'url': self.url},
                ]
            )

            self.resp = await session.request(**real_req_kwargs)
            self.resp.raise_for_status()

            return self.resp

        async def __aenter__(self):
            """Async with enter."""
            for try_idx in range(max_try):
                try:
                    return await self.__get_response()

                except aiohttp.ClientError as e:
                    current_try = try_idx + 1

                    logger.error(
                        'Request Failed ({}/{}): {} => {}: {}'
                        .format(
                            current_try, max_try,
                            self.url,
                            type(e).__name__, e,
                        )
                    )

                    await self.__aexit__(*sys.exc_info())

                    if current_try == max_try:
                        raise e from None

                except Exception as e:
                    await self.__aexit__(*sys.exc_info())

                    raise e from None

        async def __aexit__(self, exc_type, exc, tb):
            """Async with exit."""
            if self.resp:
                await self.resp.release()

            self.__release()

    return request
