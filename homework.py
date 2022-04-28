
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: int
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def get_duration_in_minutes(self) -> float:
        """Получить время в минутах"""
        return self.duration * self.MIN_IN_HOUR

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER = 18
    SPEED_SUBTRAHEND = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""

        return (
            (
                self.SPEED_MULTIPLIER * self.get_mean_speed()
                - self.SPEED_SUBTRAHEND
            )
            * self.weight / self.M_IN_KM * self.get_duration_in_minutes()
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        return (
            (
                self.WEIGHT_MULTIPLIER_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WEIGHT_MULTIPLIER_2 * self.weight
            )
            * self.get_duration_in_minutes()
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    length_pool: float
    count_pool: int
    SPEED_ADDEND = 1.1
    WEIGHT_MULTIPLIER = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в бассейне."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        return (
            (
                self.get_mean_speed() + self.SPEED_ADDEND
            )
            * self.WEIGHT_MULTIPLIER * self.weight
        )


DATA = {
    'SWM': (Swimming, 5),
    'RUN': (Running, 3),
    'WLK': (SportsWalking, 4)
}

TRAINING_TYPE = 'Датчик передал неверный вид тренировки "{}".'
NUM_VALUES = (
    'Датчик передал неверное количество показателей '
    'тренировки "{}" - "{}" вместо "{}".'
)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in DATA:
        raise ValueError(TRAINING_TYPE.format(workout_type))
    training, values = DATA[workout_type]
    if values != len(data):
        raise ValueError(NUM_VALUES.format(workout_type, len(data), values))
    return training(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        main(read_package(workout_type, data))
