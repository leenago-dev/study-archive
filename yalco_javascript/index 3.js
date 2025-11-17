// 1. 블록문과 스코프
/*
블록문: 0개 이상의 구문 (statement)을 묶을 때 사용
*/

// 스코프 안에서 선언된 변수는 스코프 밖에서는 사용 불가
{
  const x = 'Hello';
  let y = 'world!';
  console.log(x, y);
}

// console.log(x); // ReferenceError: x is not defined
// console.log(y); // ReferenceError: y is not defined

// 단, 스코프 밖에서 선언된 변수는 스코프 안에서도 사용 가능

let x = 1;

{
  let y = 2;
  console.log(x, y);
}
console.log(x);
//console.log(y); // Uncaught ReferenceError: y is not defined


//
const xx = 0;
let yy = 'Hello!';
console.log(xx, yy);

{
  const xx = 1; // 💡 블록 안에서는 바깥의 const 재선언 가능
  let yy = '안녕하세요~'; // ⚠️ 여기에서 const, let을 빼먹으면 재선언이 아니라 바깥것의 값(여기서는 yy)을 바꿈!

  console.log(xx, yy);

}

console.log(xx, yy);


// 스코프 체인
/*
나중에 온 것이 먼저 나감 (LIFO, Last In First Out)
- 블럭 안에 해당 변수/상수가 없으면 바깥쪽으로 찾아 나감

- 전역 변수 사용은 코드 어느 곳에서 접근 가능하기 때문에, 변수나 상수는 가능한 블록 내에서 선언해서 메모리 효율을 챙기기!
*/

let a = 0;
let b = 1;
let c = 2;
console.log('시점 1:', a, b, c); // 0 1 2

{
  let a = 'A';
  let b = 'B'
  console.log('시점 2:', a, b, c); // A B 2

  {
    let a = '가'
    console.log('시점 3:', a, b, c); // 가 B 2
  }

  console.log('시점 4:', a, b, c); // A B 2
}

console.log('시점 5:', a, b, c); // 0 1 2


// 2. if/else

const open = true;

if (open) { console.log('영업 중입니다!') }
else { console.log("영업 종료했어요!") };

// 다른 예시 (헷갈림 주의!)
const x1 = 24;

if (x1 % 2) {
  console.log("홀수입니다.") // 24 % 2 = 0 이므로 falsy라 실행되지 않음
}
else if (x1 % 4) {
  console.log("짝수입니다.") // 24 % 4 = 0 이므로 falsy라 실행되지 않음
}
else {
  console.log("4의 배수입니다.") // 최종적으로 실행
};

// 실전에서 사용하는 예시
// else의 경우 가독성이 좋지 않기 때문에, 삼항 연산자나 아래와 같이 return문을 사용하는 것이 좋음!

function evalNum() {
  const x2 = 21;

  if (x2 % 2) {
    console.log('홀수입니다.');
    return; // 만약 위 값이 truthy라면, 이 부분이 실행되고, return에서 끝나버림
  }

  if (x2 % 4) {
    console.log('짝수입니다.');
    return;
  }

  console.log('4의 배수입니다.');
}

evalNum();
console.log('블록문 바깥');


// 3. switch문
/*
주어진 값에 따라 다양한 옵션을 실행할 때 사용
 */

const fingersOut = 2;

switch (fingersOut) {
  // 순서 상관없음
  case 2: // 주어진 평가에 일치하는 case로 실행위치 이동
    console.log('가위');
    break; // 해당 case를 실행하고 나서 바로 switch문을 빠져나가라는 의미 (없으면 아래 case도 실행됨)
  case 0:
    console.log('바위');
    break;
  case 5:
    console.log('보');
    break;
  default: // case에 해당하는 값이 없을 때 사용, 항상 맨 마지막에 작성해준다. (여기에는 break가 없어도 됨)
    console.log('무효');
}

// 다른 예시
const direction = 'north';
let directionKor;

switch (direction) {
  case 'north':
    directionKor = "북";
    break;

  case 'south':
    directionKor = "남";
    break;

  case 'east':
    directionKor = "동";
    break;

  case 'west':
    directionKor = "서";
    break;

  default:
    directionKor = "없음";
}

console.log(directionKor);

// 다른 예시 ➡️ 객체를 사용한 방법

const directionObj = "south";

const directionKorObj = {
  "north": "북",
  "south": "남",
  "east": "동",
  "west": "서",
}[directionObj] ?? "없음";

console.log(directionKorObj);

// 다른 예시 ➡️ case를 여러 개 사용하는 방법
const startMonth = 1;
let holidays = '분기 내 휴일:';

switch (startMonth) {
  case 1:
    holidays += ' 설날';
  case 2:
  case 3:
    holidays += ' 3•1절';
    break;

  case 4:
  case 5:
    holidays += ' 어린이날';
  case 6:
    holidays += ' 현충일';
    break;

  case 7:
  case 8:
    holidays += ' 광복절';
  case 9:
    holidays += ' 추석';
    break;

  case 10:
    holidays += ' 한글날';
  case 11:
  case 12:
    holidays += ' 크리스마스';
    break;

  default:
    holidays = '잘못된 월입니다.';
}

console.log(holidays);


// 4. for문
/*
반복문: 코드를 여러 번 실행하고 싶을 때 사용
- 조건을 적지 않는 경우 true로 판단이 되어 무한루프에 빠질 수 있으니 주의!
 */

for (let i = 0; i < 10; i++) {
  console.log(i); // 한 턴을 실행하고 그 다음 i를 ++로 하나씩 증가
}

for (let i = 0; i < 10;) {
  console.log(i++);
}

for (let x = 0, y = 10; x <= y; x++, y--) {
  console.log(x, y);
}

// 객체와 배열의 for loop
// 객체에서는 for in 문을 사용해서 key를 순회하며 값을 출력한다!
const lunch = {
  name: "떡볶이",
  taste: "매운맛",
  price: 8000,
  cold: false
};

for (const key in lunch) { // 객체의 경우 key를 순회하며 값을 출력! (변할 것이 아니기 때문에 const로 선언 / key 대신 다른 변수명 사용 가능)
  console.log(key, ':', lunch[key]);
}

// for of 문 ➡️ value를 순회 / '이터러블' 객체에서만 사용
// for in 문 ➡️ key를 순회

const list = [1, '가나다', false, null];

for (const item of list) {
  console.log(item);
} // 1, 가나다, false, null

const list2 = [1, '가나다', false, null];

for (const item in list2) {
  console.log(item); // 0, 1, 2, 3
}

// for of문의 장점

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// ⚠️ 변수(i)를 사용하므로 위험요소 존재
for (let i = 0; i < numbers.length; i++) {
  // 이곳에 i를 변경하는 코드가 들어간다면...
  console.log(numbers[i]);
}

// ⭐️ 변수를 사용하지 않음으로 보다 안전
for (const num of numbers) {
  console.log(num);
}


// 5. continue와 break
// 1) continue: 해당되는 턴을 건너뛰고 다음 턴으로 이동
for (let i = 1; i <= 10; i++) {
  if (i % 3 === 0) continue; // (!i % 3) 으로 표현할 수도 있음
  console.log(i);
}
// 1, 2, 4, 5, 7, 8, 10

// 2) break: 해당되는 턴을 마주치면 바로 for문을 종료
for (let i = 1; i <= 10; i++) {
  if (i === 5) break;
  console.log(i);
}

console.log('for 루프 종료'); // 1, 2, 3, 4, "for 루프 종료"


// 6. while문과 do while문
// 1) while문

let x4 = 0;

while (x4 < 10) {
  console.log(x4++); // while문 안에다가 x4를 증가시키는 코드를 넣어줘야 무한반복을 하지 않음!
}

// 방법 1: x5를 먼저 증가시키고 홀수일 때 출력
let x5 = 0;

while (x5 < 10) {
  x5++;
  if (x5 % 2 !== 0) {
    console.log(x5);
  }
}

// 방법 2: 더 짧고 직관성을 유지한 코드
let x6 = 0;

while (x6 < 10) {
  const xNow = x6++;

  if (xNow % 2 === 0) continue;
  if (xNow > 7) break;

  console.log(xNow);
}

// 2) do while문: 일단 수행을 한 다음, 조건을 평가

// (1) while 조건에 맞지 않는 경우
let x7 = 12;

do {
  console.log(x7++);
} while (x7 < 10); // 12 -> while 조건에는 맞지 않더라도, console.log는 한 번 실행

// (2) while 조건에 맞는 경우
let x8 = 12;

do {
  console.log(x8++)
} while (x8 < 20); // 12, 13, 14, 15, 16, 17, 18, 19 -> while 조건에 맞아서 console.log가 19까지 실행됨
