import dataclasses
import datetime
from enum import StrEnum
from typing import Any

from mashumaro.mixins.json import DataClassJSONMixin


class SnooLevels(StrEnum):
    baseline = "BASELINE"
    level1 = "LEVEL1"
    level2 = "LEVEL2"
    level3 = "LEVEL3"
    level4 = "LEVEL4"
    stop = "ONLINE"


class SnooStates(StrEnum):
    baseline = "BASELINE"
    level1 = "LEVEL1"
    level2 = "LEVEL2"
    level3 = "LEVEL3"
    level4 = "LEVEL4"
    stop = "ONLINE"
    pretimeout = "PRETIMEOUT"
    timeout = "TIMEOUT"
    suspended = "SUSPENDED"
    weaning_baseline = "WEANING_BASELINE"
    global_settings = "GLOBAL_SETTINGS"
    unrecoverable_suspended = "UNRECOVERABLE_SUSPENDED"
    unrecoverable_error = "UNRECOVERABLE_ERROR"
    none = "NONE"
    manual = "MANUAL"


class SnooEvents(StrEnum):
    TIMER = "timer"
    CRY = "cry"
    COMMAND = "command"
    SAFETY_CLIP = "safety_clip"
    LONG_ACTIVITY_PRESS = "long_activity_press"
    ACTIVITY = "activity"
    POWER = "power"
    STATUS_REQUESTED = "status_requested"
    STICKY_WHITE_NOISE_UPDATED = "sticky_white_noise_updated"
    CONFIG_CHANGE = "config_change"
    RESTART = "restart"


@dataclasses.dataclass
class AuthorizationInfo:
    snoo: str
    aws_access: str
    aws_id: str
    aws_refresh: str


@dataclasses.dataclass
class SnooDevice(DataClassJSONMixin):
    serialNumber: str
    firmwareVersion: str
    babyIds: list[str]
    name: str
    deviceType: int | None = None
    presence: dict | None = None
    presenceIoT: dict | None = None
    awsIoT: dict | None = None
    lastSSID: dict | None = None
    provisionedAt: str | None = None


@dataclasses.dataclass
class SnooStateMachine(DataClassJSONMixin):
    up_transition: str
    since_session_start_ms: int
    sticky_white_noise: str
    weaning: str
    time_left: int
    session_id: str
    state: SnooStates
    is_active_session: bool
    down_transition: str
    hold: str
    audio: str
    time_left_timestamp: datetime.datetime | None = None
    level: SnooLevels | None = None

    def __post_init__(self):
        if self.time_left != -1:
            self.time_left_timestamp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                seconds=self.time_left
            )
        else:
            self.time_left_timestamp = None
        if self.up_transition == "NONE" and self.down_transition == "NONE":
            self.level = SnooLevels.stop
        elif self.up_transition == SnooLevels.level1:
            self.level = SnooLevels.baseline
        elif self.up_transition == SnooLevels.level2:
            self.level = SnooLevels.level1
        elif self.up_transition == SnooLevels.level3:
            self.level = SnooLevels.level2
        elif self.up_transition == SnooLevels.level4:
            self.level = SnooLevels.level3
        elif self.down_transition == SnooLevels.level3:
            self.level = SnooLevels.level4


@dataclasses.dataclass
class SnooData(DataClassJSONMixin):
    left_safety_clip: int
    rx_signal: dict
    right_safety_clip: int
    sw_version: str
    event_time_ms: int
    state_machine: SnooStateMachine
    system_state: str
    event: SnooEvents


@dataclasses.dataclass
class BabySettings(DataClassJSONMixin):
    carRideMode: bool
    daytimeStart: int
    minimalLevel: str
    minimalLevelVolume: str
    motionLimiter: bool
    responsivenessLevel: str
    soothingLevelVolume: str
    weaning: bool


@dataclasses.dataclass
class BabyData(DataClassJSONMixin):
    _id: str
    babyName: str
    birthDate: str
    breathSettingHistory: list
    createdAt: str
    disabledLimiter: bool
    expectedBirthDate: str
    pictures: list
    settings: BabySettings
    sex: str
    preemie: Any | None = None  # Not sure what datatype this is yet & may not be supplied - boolean?
    startedUsingSnooAt: str | None = None
    updatedAt: str | None = None
