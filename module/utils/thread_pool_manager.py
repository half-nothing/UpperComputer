from concurrent.futures import ThreadPoolExecutor

thread_pool = ThreadPoolExecutor(thread_name_prefix="CommonThreadPool", max_workers=16)

