import asyncio
import random
from typing import Final, Optional

JUST_JOINED_MOOD: Final[str] = "just_joined"
LEAVING_OFF_MOOD: Final[str] = "leaving_off"

MOODS: Final[tuple[str, ...]] = (
    "happy",
    "sad",
    "angry",
    "anxious",
    "joking",
    "having_fun",
    "frightened",
    "surprised",
    "panic",
    "envy",
    "gloomy",
    "agitated",
    "affectionate",
    "shy",
    "worry",
    "enthusiastic",
    "confused",
    "satisfied",
    "curious",
    "delight",
    "disappointed",
)


class MoodManager:
    """
    Some dummy state that all friend nodes could exchange on caching up
    """

    def __init__(self) -> None:
        self._mood = JUST_JOINED_MOOD
        self._mood_changer: Optional[asyncio.Task] = None

    @property
    def current_mood(self) -> str:
        return self._mood

    async def start(self) -> None:
        self._mood_changer = asyncio.create_task(self._change_mood_periodically())

    async def stop(self) -> None:
        if self._mood_changer:
            self._mood_changer.cancel()
            await self._mood_changer

    async def _change_mood_periodically(self) -> None:
        await asyncio.sleep(5)

        while True:
            try:
                self._mood = random.choice(MOODS)
                await asyncio.sleep(3)
            except asyncio.CancelledError:
                self._mood = LEAVING_OFF_MOOD
                return
