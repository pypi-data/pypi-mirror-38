# 동식물 모니터링 시스템의 Python용 Datalib.

## 목적

  UTC로 기록된 데이터를 국가별 시간대에 맞게 가져오려면 범위에 대한 적절한 변환이 필요하다.  변환 과정은 생각하므로 데이터 분석의 장애물이 될 수 있다. 이러한 장애물을 해소하고 데이터 분석 과정을 돕기 위해 본 라이브러리를 개발하였다.



## 개요

  현재 MongoDB에 저장된 데이터는 UTC를 기준으로 저장된다. UTC로 저장하는 이유는 시간대나 위치 등에 구애받지 않고, 데이터를 공통적으로 저장하고 이용하기 위해서이다. 

  그러나 국가별 시차가 존재한다. 시차로 인해 데이터를 가져올 때 범위의 변환이 필요하다. 예를 들어 한국 시간 기준  15일의 데이터를 가져오려면 UTC 기준 14일 오후 3시부터 15일 오후 3시까지의 데이터를 가져와야 한다. 

본 라이브러리는 이러한 변환 기능과 더불어 손쉽게 데이터를 가져올 수 있는 다양한 API를 제공한다.

## API 명세

본 라이브러리의 패치키명은 apmondatalib이다.



### create_raw_data_fetcher 메소드

  create_raw_data_fetcher는 apmondatalib의 인스턴스를 생성하는 함수이다. 본 라이브러리를 사용하기 위한 첫 번째 진입 함수이다.

| 역할     |                        |                                     |
| -------- | ---------------------- | ----------------------------------- |
| 파라메터 | host                   | MongoDB의 접속 주소                 |
|          | port                   | MongoDB의 포트 (기본값: 27017)      |
|          | database               | 데이터베이스 이름 (기본값: apmonv1) |
|          | sensor_id              | 센서의 식별자                       |
|          | time_offset            | 시간대 (한국의 기본값: 9)           |
| 반환값   | DataFetcher의 인스턴스 |                                     |



### SensorRawDataFetcher 클래스

#### 생성자

| 분류     | 이름                   | 설명                                |
| -------- | ---------------------- | ----------------------------------- |
| 파라메터 | host                   | MongoDB의 접속 주소                 |
|          | port                   | MongoDB의 포트 (기본값: 27017)      |
|          | database               | 데이터베이스 이름 (기본값: apmonv1) |
|          | sensor_id              | 센서의 식별자                       |
|          | time_offset            | 시간대 (한국의 기본값: 9)           |
| 반환값   | DataFetcher의 인스턴스 |                                     |



#### read

데이터베이스에 저장된 센서값을 가져오는 함수이다.

| 파라메터 | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | sensor_type             | SensorType Enum 중 하나     |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
|          | page_number             | 페이지 번호                 |
| 반환값   | RawData 클래스의 리스트 |                             |



#### read_humidity

| 분류     | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | page_size               | 한번에 가져올 데이터의 갯수 |
|          | page_number             | 페이지 번호                 |
| 반환값   | RawData 클래스의 리스트 | 센서값의 목록               |



#### read_temperature

| 분류     | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | page_size               | 한번에 가져올 데이터의 갯수 |
|          | page_number             | 페이지 번호                 |
| 반환값   | RawData 클래스의 리스트 | 센서값의 목록               |



#### read_light

| 분류     | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | page_size               | 한번에 가져올 데이터의 갯수 |
|          | page_number             | 페이지 번호                 |
| 반환값   | RawData 클래스의 리스트 | 센서값의 목록               |



#### read_motion

| 분류     | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | page_size               | 한번에 가져올 데이터의 갯수 |
|          | page_number             | 페이지 번호                 |
| 반환값   | RawData 클래스의 리스트 | 센서값의 목록               |



#### SensorType (Enum)

시스템이 지원하는 센서의 타입이며, 다음과 같은 항목을 사용할 수 있다.

| 이름        | 설명             |
| ----------- | ---------------- |
| Humidity    | 습도 센서        |
| Temperature | 온도 센서        |
| Light       | 조도 센서        |
| Motion      | 움직임 감지 센서 |



#### RawData 클래스

센서값을 표현하는 클래스이며, 현재 네 가지 항목을 가지고 있다. 추후에 시간 정보가 추가될 예정이다.

| 이름      | 설명                         |
| --------- | ---------------------------- |
| id        | MongoDB에 저장된 데이터의 ID |
| sensor_id | 센서 보드의 식별자           |
| type      | SensorType Enum 중 하나      |
| value     | 측정값                       |



## 설치방법

```bash
pip install apmondatalib
```

위의 명령어를 입력하여 설치한다.



## 예제

  다음의 예제는 각 타입의 데이터를 가져오는 기본적인 예제이다.

```python

from apmondatalib import DataFetcher


def main():
    d = DataFetcher.create_raw_data_fetcher("49.247.210.243", 27017, "apmonv1", "SEN03", 9)
    for x in d.read(DataFetcher.SensorType.Humidity, 50, 5):
        print x

    for x in d.read(DataFetcher.SensorType.Temperature, 50, 5):
        print x

    for x in d.read(DataFetcher.SensorType.Light, 50, 5):
        print x

    for x in d.read(DataFetcher.SensorType.Motion, 50, 5):
        print x


if __name__ == "__main__":
    main()
```

   

