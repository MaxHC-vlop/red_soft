from datetime import time


def check_arrival_time(plan_arrival: time, fact_arrival: time) -> str:
    plan_arrival = (plan_arrival.hour * 60) + plan_arrival.minute
    fact_arrival_minutes = (fact_arrival.hour * 60) + fact_arrival.minute
    difference_minutes = fact_arrival_minutes - plan_arrival

    if difference_minutes > 0:
        return f"Самолет опаздывает на {difference_minutes} минут"

    elif difference_minutes < 0:
        return f"Самолет прилетел раньше на {-difference_minutes} минут"

    else:
        return "Самолет прилетел вовремя"


def main():
    plan_time = time(13)
    fact_time = time(12, 40)
    result_string = "Самолет прилетел раньше на 20 минут"
    assert check_arrival_time(plan_time, fact_time) == result_string

    plan_time = time(12, 20)
    fact_time = time(12, 40)
    result_string = "Самолет опаздывает на 20 минут"
    assert check_arrival_time(plan_time, fact_time) == result_string

    plan_time = time(12, 20)
    fact_time = time(12, 20)
    result_string = "Самолет прилетел вовремя"
    assert check_arrival_time(plan_time, fact_time) == result_string


if __name__ == '__main__':
    main()
