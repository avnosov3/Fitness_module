class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        return (self.duration * 60)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        COEF_CALORIE_RUNNING_1 = 18
        COEF_CALORIE_RUNNING_2 = 20
        return ((COEF_CALORIE_RUNNING_1 * self.get_mean_speed()
                - COEF_CALORIE_RUNNING_2)
                * self.weight / self.M_IN_KM * self.get_duration_in_minutes())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        COEF_CALORIE_WALKING_1 = 0.035
        COEF_CALORIE_WALKING_2 = 0.029
        return ((COEF_CALORIE_WALKING_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * COEF_CALORIE_WALKING_2 * self.weight)
                * self.get_duration_in_minutes())


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в бассейне."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        COEF_CALORIE_SWIMMING_1 = 1.1
        COEF_CALORIE_SWIMMING_2 = 2
        return ((self.get_mean_speed() + COEF_CALORIE_SWIMMING_1)
                * COEF_CALORIE_SWIMMING_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        data_ditc_swm = {'workout_type': workout_type,
                         'num_of_strokes': data[0],
                         'time_in_hour': data[1],
                         'user_weight': data[2],
                         'length_pool': data[3],
                         'count_pool': data[4]
                         }
        return Swimming(data_ditc_swm['num_of_strokes'],
                        data_ditc_swm['time_in_hour'],
                        data_ditc_swm['user_weight'],
                        data_ditc_swm['length_pool'],
                        data_ditc_swm['count_pool'])
    elif workout_type == 'RUN':
        data_dict_run = {'workout_type': workout_type,
                         'num_of_steps': data[0],
                         'time_in_hour': data[1],
                         'user_weight': data[2]
                         }
        return Running(data_dict_run['num_of_steps'],
                       data_dict_run['time_in_hour'],
                       data_dict_run['user_weight'])
    elif workout_type == 'WLK':
        data_dict_wlk = {'workout_type': workout_type,
                         'num_of_steps': data[0],
                         'time_in_hour': data[1],
                         'user_weight': data[2],
                         'user_height': data[3]
                         }
        return SportsWalking(data_dict_wlk['num_of_steps'],
                             data_dict_wlk['time_in_hour'],
                             data_dict_wlk['user_weight'],
                             data_dict_wlk['user_height'])
    else:
        return 'я сломался'


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
