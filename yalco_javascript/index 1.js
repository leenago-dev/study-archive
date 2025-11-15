// 1. 콘솔 활용하기
console.log("Hello, World");
console.log(43);
console.log(false);

/* 터미널에서 실행하려면 > node+파일명 < 을 입력하면 됨, 일반 모드로 돌아갈 경우 ctrl+c 두 번 누르기
    > control+option+n <을 누르면 'code runner' extension이 실행되고, 여기에서 바로 확인 가능 (변경 할 때마다 저장 후 단축키 입력)
    console은 개발자가 코드에서 사용하는 요소를 확인하기 위해 사용하는 것! (**개발자를 위한 것**)
*/

// 2. 흔히 활용되는 console 기능
console.log("Hello, World!");
console.info("Hello, World!"); // console.log와 동일한 기능이나, firefox 브라우저에서는 아이콘이 추가됨
console.warn("Hello, World!"); // 경고 메세지 출력
console.error("Hello, World!"); // 에러 메세지 출력

/*
자바스크립트 런타임 환경 runtime environment 이란?
자바스크립트 코드를 실행할 수 있는 소프트웨어

컴퓨터가 회사라면, 자바스크립트란 언어를 구사하는 직원
대표적으로 브라우저와 Node.js 등이 있음
콘솔 등은 자바스크립트 런타임 환경의 기능
*/

// 3. 주석 (command+/)과 세미콜론
// 어떤 코드를 일시적으로 비활성화 하거나, 현재 사용하지는 않지만 지우고 싶지는 않을 때 사용
// 세미콜론이 없어도 동작하지만, 팀의 convention에 맞춰 사용하는 것이 좋음!

// console.log("Hello") console.log("World") ➡️ SyntaxError: Unexpected identifier 'console' 발생
console.log("Hello"); console.log("World"); console.log("Testing semicolon");

// 4. 변수와 상수
// i.e. 1
const SALUTATION = "Hello";
let person = "John"; // 'person'이라는 변수를 선언하고, 거기에 'John'이라는 값을 할당
person = "Jane"; // 이미 person 이라는 변수가 생성됐기 때문에, let을 사용하지 않고 바로 person에 값을 변경

console.log(person);

// i.e. 2
let x = 1;
let y = x;
console.log('변경 전', x, y); // 여러 변수가 같은 값을 가지고 있다면, 해당 값은 데이터 영역의 한 곳에만 저장됨.

x = "Hello";
console.log('변경 후', x, y); // 변수 x의 값을 변경하면, 기존 위치에 새 값을 넣는 것이 아니라 다른 곳에 데이터를 재할당

// 이미 만들어진 주머니를 재선언 할 수 없음
let z = 1;
//let z = 2; ❌ SyntaxError: Identifier 'z' has already been declared

// 상수는 대문자로 작성하는 것이 관례; 값이 변경하지 않을 것이라는 의도를 명확히 표현하기 위함!
const PI = 3.14;
console.log(PI); // 상수는 값을 변경할 수 없음 ➡️ 재할당 불가능
// PI = 3.141592; ❌ TypeError: Assignment to constant variable.

// 여러 변수와 상수 동시 선언 (but 실제로는 많이 사용되지 않음!)
let a = 1, b = 2, c = 3;
const X = 1, Y = 5, Z = 10;
