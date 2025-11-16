// 1. 자료형
// primitive data types
const a = true, b = 123.45, c = "Hello";
console.log(a, typeof a);
console.log(b, typeof b)
console.log(c, typeof c); //typeof 연산자를 사용하면 자료형 반환 (Python의 'type()' 함수와 동일)

let description = `미국의 프로그래머로
자바스크립트 언어를 만들었으며
모질라의 CEO와 CTO를 역임했다.`;

console.log(description, typeof description);

let d;
console.log(d, typeof d); //undefined: 값이 부여되지 않은 변수
// 다른 언어들과 달리, undefined도 값이 있음! (초기화 때 많이 사용한다)

let e = null;
console.log(e, typeof e); //null: JavaScript에서는 null이 object 타입이지만, 이는 언어 자체의 오류임!

// null 여부는 아래와 같이 확인할 것
console.log(e === null);

// 2. 문자열
let word1 = "Hello, this's a string";
console.log(word1)

let word2 = '작은 따옴표 안에 \'작은 따옴표\'는 이스케이프 표현을 써서 표현할 수 있다!';
console.log(word2);

let word3 = "안녕하세요! \n 반갑습니다! \t 줄을 바꿔서 탭을 사용해볼게요 \\";
console.log(word3);

// 너무 긴 문장은 \로 코드 상에서만 줄바꿈을 하되, 실제 출력에는 영향을 주지 않음

let longName = '김수한무 거북이와 두루미 \
삼천갑자 동방삭 치치카포 사리사리센타 \
워리워리 세브리깡 무두셀라 구름이 \
허리케인에 담벼락 담벼락에 서생원 \
서생원에 고양이 고양이엔 바둑이 \
바둑이는 돌돌이';

console.log(longName);

// 템플릿 리터럴 - Backtick 문자열은 이스케이프 문자열을 사용하지 않더라도 탭과 엔터를 인식함!

const NAME = '홍길동';
let age = 20;
let married = false;

console.log(
`제 이름은 ${NAME}, 나이는 ${age}세구요, \
${married ? '기혼' : '미혼'}입니다.`); // f-string 표기법과 비슷!


// 3. 문자열에 사용되는 연산자

/*
x === y : x와 y의 값이 자료형까지 같은지 확인
x !== y : x와 y의 값이 자료형까지 같지 않은지 확인
x < y : (문자열에서는) x가 y보다 사전순으로 먼저 온다
x > y : (문자열에서는) x가 y보다 사전순으로 나중에 온다

❗️ JavaScript에서는 자료형 구분을 하지 않고 암묵적으로 타입을 변환하기 때문에, 자료형 구분이 필요한 것!
*/

console.log(
  '1' === '1',
  '1' === 1,
  '1' === 2
); // true, false, false

console.log(
  '1' !== '1',
  '1' !== 1,
  '1' !== 2
); // false, true, true

// ⚠️ 숫자 문자열 관련 주의!
console.log(
  100 > 12, // 숫자는 그 자체로 비교
  '100' > '12', // 문자는 사전순으로 비교
  '100' > 12, // 문자와 숫자를 비교하면 문자를 숫자로 변환
); // true, false, true

// 연결
/* 부수효과가 일어나지 않도록 프로그래밍하는 것이 좋음!
부수효과?: 어디에 들어가있는 값을 변경하는 것 (예상치 못한 문제를 일으킬 수 있음)

 - x+y : x와 y를 연결하는 연산자 (부수효과 없음)
 - x+=y : 값을 변경해서 연결하는 연산자 (부수효과 있음)
*/

let str1 = '헬로';
str1 += ' 월드';

// 부수효과
console.log(str1);

// 값 반환
let str2 = str1 += '~~~';

console.log(str2);

// 부수효과
console.log(str1);

// ⚠️ 오류. 왼쪽 값은 부수효과의 대상(변수)이어야 함
const STR = '안녕~';
// STR += ' 반가워요!'; // ❌ TypeError: Assignment to constant variable.
console.log(STR);

// 다른 자료형과 연결하면 모두 문자열로 반환이 된다.
let result = '안녕' + 1 + true;

console.log(result);
console.log(typeof result); // string


// 4. 숫자에 사용되는 연산자
let x4 = 1 / 0;
console.log(x4, typeof x4); // Infinity, number

// 무한대에는 양음이 있음
console.log(-x4, typeof -x4); // -Infinity, number

// Infinity도 예약어!
let z4 = Infinity;
console.log(z4, typeof z4);

// 'Not a Number' 라는 숫자형 자료형이 있음!
let x5 = 1 / 'abc';
let y5 = 2 * '가나다';
let z5 = NaN;

console.log(x5, typeof x5);
console.log(y5, typeof y5);
console.log(z5, typeof z5);

// NaN은 양음이 없음
console.log(-NaN);

let x6 = 1 / 'abc';

//
console.log(
  x6,
  x6 == NaN, //  ⚠️ false - == 으로는 NaN 값 확인이 불가하다!
  x6 === NaN, //  ⚠️ false - === 으로는 NaN 값 확인이 불가하다!
  typeof x6, //  ⚠️ number로 출력이 되어 NaN 값 확인이 불가하다!
  isNaN(x6), // 숫자가 아닐 시 true
  Number.isNaN(x6) // 숫자 자료형인 주제에 숫자가 아니어야만 true
);

// 산술 연산자
// 1) 이항 산술 연산자 - 부수효과가 없음!
// 널리 사용되는 홀수와 짝수의 판별법
console.log(
  '홀수 ',
  123 % 2,
  55 % 2,
  999 % 2
);
console.log(
  '짝수 ',
  2 % 2,
  100 % 2,
  8 % 2
);

// 2) 단항 산술 연산자 - 부수효과 있음!

let check = 10;

// 값을 반환부터 하고 증가
console.log('1.', check++, check); // 10, 11

// 값을 증가부터 하고 반환
console.log('2.', ++check, check); // 12, 12


// 숫자로 변환될 수 없는 문자열
// 첫 번째 값 주의 - 증가 이전에도 변환
let text = 'abc';
console.log(text++, text); // NaN, NaN


//5. 부동소수점과 실수계산 오차
/*
JavaScript의 number 자료형은 64비트 부동소수점 수를 사용하며, 이는 이진법과 십진법의 차이로 인해 실수 계산 오차가 발생할 수 있다.

정확한 계산이 필요할 경우, 라이브러리를 활용할 수 있다.
*/

console.log(0.1 + 0.2); // 0.30000000000000004
console.log(0.1 + 0.2 === 0.3); // false

// ⭐️ 6. 불리언과 관련 연산자 ⭐️
console.log(true, typeof true); // true, boolean
console.log(false, typeof false); // false, boolean

let aa = 1 === 2;
let bb = 'abc' !== 'def'
let cc = aa !== bb;
let dd = typeof aa === typeof bb === true; // typeof a와 typeof b를 먼저 계산한 후에, 값이 true가 반환되면 true와 true를 비교하게 된다.

console.log(aa, typeof aa);
console.log(bb, typeof bb);
console.log(cc, typeof cc);
console.log(dd, typeof dd);

// 1) 부정 연산자
console.log(
  true, !true, false, !false
); // true, false, true, false

console.log(
  true, !true, !!true, !!!true
); // true, false, true, false

console.log(
  false, !false, !!false, !!!false
); // false, true, false, true

// 2) and or 연산자


// (1) and 연산자 - 양쪽 모두 true일 때만 true 반환
console.log(
  true && true,
  true && false,
  false && true,
  false && false,
); // true, false, false, false

// (2) or 연산자 - 한쪽이라도 true이면 true 반환
console.log(
  true || true,
  true || false,
  false || true,
  false || false,
); // true, true, true, false

// (3)단축평가 short circuit
// && : 앞의 것이 false면 뒤의 것을 평가할 필요 없음
// || : 앞의 것이 true면 뒤의 것을 평가할 필요 없음
// 평가는 곧 실행 - 이 점을 이용해서 연산 부하가 적은 코드를 앞에 두고, 뒤의 코드는 평가하지 않고 실행하지 않도록 하기!

let error = true;
// error = false;

error && console.log('error'); // 앞의 코드가 true일 때만 뒤의 코드 실행 (false일 경우에는 실행할 필요가 없음)
error || console.log('no error'); // 앞의 코드가 false일 때만 뒤의 코드 실행


// 3) 삼항 연산자
let check_if = true;
// check_if = false;

let result_if = check_if ? '참입니다.' : '거짓입니다.'; // check_if가 true일 때는 '참입니다.'를, false일 때는 '거짓입니다.'를 반환
console.log(result_if);


// 4) Truthy vs Falsy
// (1) Truthy - true로 평가되는 값
console.log(
  1.23 ? true : false,
  -999 ? true : false,
  '0' ? true : false,
  ' ' ? true : false, // 띄어쓰기도 true로 평가됨
  Infinity ? true : false,
  -Infinity ? true : false,
  {} ? true : false,
  [] ? true : false,
  "회사원" ? true : false,
);

// (2) Falsy - false로 평가되는 값
console.log(
  0 ? true : false,
  null ? true : false,
  undefined ? true : false,
  NaN ? true : false,
  '' ? true : false,
);

// 💡 어떤 값들은 false로 타입변환됨
console.log(
  0 == false,
  0 === false,
  '' == false, // 빈 문자열은 false로 평가됨
  '' === false
); // true, false, true, false

console.log(
  null == false,
  undefined == false,
  NaN == false,
); // false, false, false


// 7. 연산자 마무리
// 1) 쉼표 연산자

let x1 = 1, y1 = 2, z1 = 3;
console.log(x1, y1, z1);

// 괄호를 하나 더 해주면, 마지막으로 실행한 것을 반환
console.log(
  (++x1, y1 += x1, z1 *= y1)
); // 1이 2로 증가 ➡️ 2와 2가 더해서 4 ➡️ 4와 3이 곱해서 12

// 2) null 병합 연산자
// ⚠️ null 병합 연산자는 왼쪽 값이 null 또는 undefined일 때만 오른쪽 값을 반환

let x2;
x2 ?? console.warn(x2, 'x에 값이 할당되지 않아 값이 없습니다.');

x2 = 0;
x2 ?? console.warn(x2, 'x는 0이라 값이 있습니다.');

x2 = null;
x2 ?? console.warn(x2, 'x는 null이라 값이 없습니다.');

// 다른 예)
let baby1 = '홍길동';
let baby2; // 아직 이름을 짓지 못함

const nameTag1 = baby1 ?? '1번 아기';
const nameTag2 = baby2 ?? '2번 아기';

console.log(nameTag1, nameTag2); // '홍길동', '2번 아기'

// 3) 병합 할당 연산자
let x3 = 0;
let y3 = '';
let z3 = null;

x3 ||= 100; // x3이 0이라 false로 평가되므로, 100이 나오고, 거기에 병합 할당 연산자를 사용하면 100이 할당된다.
y3 &&= '있어야 바뀜'; // y3이 빈 문자열이라 false로 평가되고 and 연산자라 뒤의 값을 평가하지 않고 넘어가기 때문에, 똑같이 공백이 할당된다.
z3 ??= '기본값'; // z3이 null이라 false로 평가되므로, '기본값'이 나오고, 거기에 병합 할당 연산자를 사용하면 '기본값'이 할당된다.

console.log(x3, y3, z3); // 100, '', '기본값'


// 8. 객체와 배열 미리보기
// 1) 객체 (object)
/* JavaScript에서 원시 타입이 아닌 모든 데이터는 근본적으로 '객체' 이다.
객체는 복합적인 정보를 프로퍼티 (key-value pair)들로 직접 저장하는 자료형이다.

const objName = {
  key1: value1,
  key2: value2,
  ...
};
// ⚠️ 블록이 아님!
*/

const person1 = {
  name: '김철수',
  age: 25,
  married: false
}; // const인데 안에 있는 값은 변경할 수 있음

console.log(typeof person1); // object
console.log(person1);

// 객체의 프로퍼티 접근 방법 2가지
// 1) 점 표기법
console.log(person1.name, person1.age, person1.married);

// 2) 대괄호 표기법
console.log(person1['name']);
console.log(person1['age']);
console.log(person1['married']);

// 존재하지 않는 프로퍼티에 접근하려면 'undefined'를 반환한다.
// 존재하는 프로퍼티인지 확인하려면 'in'을 사용한다.
console.log('name' in person1); // true
console.log('gender' in person1); // false

// 새 프로퍼티 추가
person1.gender = 'male';
console.log('gender' in person1); //true

// 프로퍼티 내용 수정
person1.age = 26
console.log(person1.age);


// 2) 배열 (array)
const winners = [12, 592, 7, 48];
const weekdays = ['월', '화', '수', '목', '금', '토', '일'];

// 한 배열에 여러 자료형을 한 번에 넣을 수 있음
const randoms = ['홍길동', -24, true, null, undefined];

console.log(typeof winners);
console.log(winners, weekdays, randoms);

// 특정 순서의 값에 접근하는 법 (0부터 시작)
console.log(winners[0], weekdays[6], randoms[3]);

// 배열의 길이(요소의 갯수)를 얻는 법
console.log(winners.length, weekdays.length, randoms.length); // .len()과 비슷

// 마지막 요소 얻기
console.log(winners[winners.length - 1]);

const numbers = [1, 2, 3];

// 특정 위치의 값 수정
numbers[2] = 5;

console.log(numbers); // [1, 2, 5]

// 맨 끝에 값 추가 (push)
numbers.push(10);

console.log(numbers); // [1, 2, 5, 10]

// 배열의 범주를 넘어가게 되면, undefined를 반환한다.
const winners2 = [12, 592, 7, 48]; // 0, 1, 2, 3으로 인덱싱 되어있음 (length는 4)
console.log(winners2[winners2.length]); // undefined

// 객체 안에 객체, 배열 등등을 다 넣을 수 있음
const person2 = {
  name: '김달순',
  age: 23,
  languages: ['Korean', 'English', 'French'],
  education: {
    school: '한국대',
    major: ['컴퓨터공학', '전자공학'],
    graduated: true,
  }
};

console.log(person2.languages[2]); // French
console.log(person2.education.graduated); // true
console.log(person2.education.major[1]); // 전자공학



// ⭐️ 9. 원시타입 vs 참조타입 ⭐️
/* 원시타입: 원시 자료형은 복사할 땐 같은 값을 바라보고 있다가, 한 쪽에 다른 값을 할당하면 각자 새로운 값을 바라보게 됨.
*/

let number3 = 1;
let string3 = 'ABC';
let bool3 = true;

let number4 = number3;
let string4 = string3;
let bool4 = bool3;

number4 = 2;
string4 = '가나다';
bool4 = false;

console.log('~3:', number3, string3, bool3);
console.log('~4:', number4, string4, bool4);

let number1 = 1;
number2 = number1;
number2 = 2;

console.log(number1, number2); // 1, 2

/* 참조타입: 주소를 갖는 주머니에 들어있고, 복사할 때 주소의 주머니를 동일하게 복사함
같은 주소값을 참조하고 있는 상태라서 원본도 함께 변경되는 것!
*/
const obj1 = {
  num: 1, str: 'ABC', bool: true
};
const obj2 = obj1;

console.log('obj1:', obj1); // { num: 1, str: 'ABC', bool: true }
console.log('obj2:', obj2); // { num: 1, str: 'ABC', bool: true }

// ⭐️ const임에도 내부 값은 변경 가능! 힙(heap) 영역에 있는 값을 변경하는 것이기 때문에 변경 가능
obj2.num = 2;
obj2.str = '가나다';
obj2.bool = false;

console.log('obj1:', obj1); // { num: 2, str: 'ABC', bool: true } ❗️ 원본도 변경됨
console.log('obj2:', obj2); // { num: 2, str: '가나다', bool: false }
