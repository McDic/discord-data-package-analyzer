import bisect
import json

from collections.abc import Iterator
from csv import DictReader
from dataclasses import dataclass
from datetime import datetime
from glob import glob
from pathlib import Path
from typing import Any, Final
from multiprocessing.pool import Pool
from zoneinfo import ZoneInfo


UTC: Final[ZoneInfo] = ZoneInfo("UTC")


@dataclass
class Message:
    """
    Represent a message.
    """

    id: str
    timestamp: datetime
    content: str

    @classmethod
    def yield_messages(cls, path: Path) -> Iterator["Message"]:
        """
        Yield messages from given `path`.
        """
        with open(path, "r") as messages_csv:
            reader = DictReader(messages_csv)
            for row in reader:
                yield cls(
                    id=row["ID"],
                    timestamp=datetime.fromisoformat(row["Timestamp"]),
                    content=row["Contents"],
                )

    def __lt__(self, other) -> bool:
        if not isinstance(other, Message):
            raise TypeError
        return self.timestamp < other.timestamp


@dataclass(eq=True, frozen=True)
class MessageChannel:
    """
    Represent a channel to send messages.
    """

    id: str
    type: int
    name: str | None


@dataclass(frozen=True)
class MessageCondition:
    """
    Represent a message condition to filter messages.
    """

    channel: str | None = None
    content: str | None = None
    min_timestamp: datetime = datetime.min.replace(tzinfo=UTC)
    max_timestamp: datetime = datetime.max.replace(tzinfo=UTC)


class DiscordPackage:
    """
    Represent a discord package.
    """

    def __init__(self, path: Path | str) -> None:
        self._path = Path(path)
        self.messages_index: dict[str, str | None] = {}
        self.messages: dict[MessageChannel, list[Message]] = {}
        self._analyze()

    @staticmethod
    def raise_if_not_directory(path: Path):
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"{path} is not an existing directory")

    @staticmethod
    def raise_if_not_file(path: Path):
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"{path} is not an existing file")

    def _analyze(self):
        """
        Analyze the whole discord package.
        """
        self.raise_if_not_directory(self._path)

        messages_path = self._path / "messages"
        if messages_path.exists() and messages_path.is_dir():
            self._analyze_messages(messages_path)

    def _analyze_messages(self, path: Path):
        """
        Analyze the whole discord messages in a package.
        """
        self.raise_if_not_directory(path)
        self.raise_if_not_file(path / "index.json")
        # Skip `index.json` because it is redundant

        with Pool() as pool:
            result = pool.map(
                self._analyze_single_message_folder,
                (path / dirname for dirname in glob("c*", root_dir=path)),
            )
            for message_channel, messages in result:
                self.messages[message_channel] = messages

    @classmethod
    def _analyze_single_message_folder(
        cls, path: Path
    ) -> tuple[MessageChannel, list[Message]]:
        """
        Analyze a single message folder.
        """
        cls.raise_if_not_file(path / "channel.json")
        cls.raise_if_not_file(path / "messages.csv")

        with open(path / "channel.json") as channeljson_file:
            channeljson_raw: dict[str, Any] = json.load(channeljson_file)
            channel = MessageChannel(
                id=channeljson_raw["id"],
                type=channeljson_raw["type"],
                name=channeljson_raw.get("name"),
            )

        messages = sorted(Message.yield_messages(path / "messages.csv"))
        return channel, messages

    def export_ids(self, path: Path, condition: MessageCondition | None = None):
        """
        Export ids to given `path`, in format Discord Privacy Team required.
        """
        with open(path, "w") as outfile:
            for channel, messages in self.search_messages(condition=condition):
                outfile.write(f"{channel.id}:\n")
                outfile.write(", ".join(message.id for message in messages))
                outfile.write("\n\n")

    def search_messages(
        self, condition: MessageCondition | None = None
    ) -> Iterator[tuple[MessageChannel, Iterator[Message]]]:
        """
        Search messages by given information.
        The order of messages in each group is subject to be changed.
        """
        condition = condition or MessageCondition()
        if condition.min_timestamp > condition.max_timestamp:
            raise ValueError("Min timestamp is bigger than max timestamp")

        for message_channel, messages in self.messages.items():
            if condition.channel and not (
                condition.channel == message_channel.id
                or condition.channel in (message_channel.name or "")
            ):
                continue

            start_index = bisect.bisect_left(
                messages, Message("", condition.min_timestamp, "")
            )
            end_index = bisect.bisect_right(
                messages, Message("", condition.max_timestamp, "")
            )
            yield (
                message_channel,
                (
                    message
                    for message in messages[start_index:end_index]
                    if not condition.content or condition.content in message.content
                ),
            )
