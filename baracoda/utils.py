import os
import sys
from logging import Filter, Handler
from typing import Iterable

from slack import WebClient
from slack.errors import SlackApiError

client = WebClient(token=os.getenv("SLACK_API_TOKEN", ""))


class SlackHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        self.send_message(log_entry)

    def send_message(self, sent_str):
        try:
            client.chat_postMessage(
                channel=os.getenv("SLACK_CHANNEL_ID", ""),
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": sent_str,
                        },
                    },
                ],
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")


class PackagePathFilter(Filter):
    """Subclass of logging Filter class which provides two log record helpers, namely:

    - relativepath: the relative path to the python module, this allows you to click on the path and line number from
    a terminal and open the source at the exact line in an IDE.
    - relative_path_and_lineno: a concatenation of `relativepath` and `lineno` to easily format the record helper to a
    certain length.

    Based heavily on https://stackoverflow.com/a/52582536/15200392
    """

    def filter(self, record):
        pathname = record.pathname

        record.relativepath = None
        record.relative_path_and_lineno = None

        abs_sys_paths: Iterable[str] = map(os.path.abspath, sys.path)

        for path in sorted(abs_sys_paths, key=len, reverse=True):  # longer paths first
            if not path.endswith(os.sep):
                path += os.sep
            if pathname.startswith(path):
                record.relativepath = os.path.relpath(pathname, path)
                record.relative_path_and_lineno = f"{record.relativepath}:{record.lineno}"

                break

        return True
