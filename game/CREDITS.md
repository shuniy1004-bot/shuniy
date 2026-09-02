# game/ 출처

## 구슬 레이스 코스 · 물리
[lazygyu/roulette](https://github.com/lazygyu/roulette) 에서 가져왔습니다.
MIT License, Copyright (c) 2023 LazyGyu — 전문은 `LICENSE-marble-roulette.txt`.

- `maps.js` — 코스 데이터. 원본 그대로
- `engine.js` — 물리 · 사다리 로직. 원본을 이 사이트에 맞게 옮긴 것

## 사다리타기
모요 사이트에서 쓰던 방식 그대로입니다 — 가로줄은 그리지 않고,
내려가는 선이 지나갈 때만 드러납니다.
줄 수는 `2 * 인원^2` 로, 2~10명 구간에서 자리별 승률 카이제곱 검정을 통과합니다.

## 룰렛
이 사이트에서 새로 만들었습니다 (`wheel.js`).
당첨을 가중치 추첨으로 먼저 정하고 원판을 그 칸에 맞춰 돌리므로,
결과가 프레임 속도나 누른 시간에 좌우되지 않습니다.
