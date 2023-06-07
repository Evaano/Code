/* const str = "well this is awkward"
const num = 12
const numbers = [3, 7, 2, 9, 1, 1];

console.log(findLargest(numbers));

console.log(isPalindrome(str));

console.log(reverseString(str));

console.log(factorial(num));

console.log(sortAscending(numbers));

console.log(removeDuplicates(numbers));

function reverseString(str) {
	return str.split("").reverse().join("");
}

function isPalindrome(str) {
	let reversedString = str.split("").reverse().join("");
	return str === reversedString
}

function factorial(num) {
	if (num === 1) {
		return 1;
	}
	return (num * factorial(num - 1));
}

function findLargest(arr) {
	return Math.max(...arr)
}

function sortAscending(arr) {
	return arr.sort((a, b) => a - b);
}

function removeDuplicates(arr) {
	return [...new Set(arr)];
}

//hoisting
function foo() {
	console.log(x); // undefined
	var x = 1;
	console.log(x); // 1
}
foo();

bar();

function bar() {
	var x = 1;
	console.log(x); // 1
}


//class and object difference
class Car {
	constructor(make, model, color) {
		this.make = make;
		this.model = model;
		this.color = color;
		this.engineStatus = "off";
	}

	startEngine() {
		if (this.engineStatus == "off") {
			this.engineStatus = "on";
			console.log("Engine has started");
		}
		else {
			if (this.engineStatus == "on") {
				console.log("Engine has already been started")
			}
		}
	}

	drive() {
		if (this.engineStatus == "on") {
			console.log(`${this.color} ${this.make} ${this.model} is driving`)
		}
		else {
			console.log("Can't drive without turning the engine on")
		}
	}
}

let car1 = new Car("Mazda", "RX-7", "Pink");
let car2 = new Car("Mazda", "RX-8", "Red");
let car3 = new Car("Nissan", "GTR", "Black");

car1.startEngine();
car1.drive();
car2.drive();
car3.startEngine();
car3.startEngine();



// Normal and Arrow function
class Person {
	constructor(name) {
		this.name = name;
	}

	// Arrow function
	sayHello() {
		setTimeout(() => {
			console.log(`Hello my name is ${this.name}`)
		}, 1000)
	}


	// Normal function
	sayHello() {
		setTimeout(function () {
			console.log(`Hello my name is ${this.name}`)
		}.bind(this), 1000)
	}
}

let person1 = new Person("Bob");
person1.sayHello();

Promise
const fetchData = new Promise((resolve, reject) => {
	fetch('https://jsonplaceholder.typicode.com/todos/1')
		.then(response => response.json())
		.then(json => console.log(json))
		.catch(error => reject(error))
});



const fetchData = (callback) => {
	fetch('https://jsonplaceholder.typicode.com/todos/1')
		.then(response => response.json())
		.then(json => callback(null, json))
		.catch(error => callback(error, null));
};

// Example usage
fetchData((error, data) => {
	if (error) {
		console.error(error);
	} else {
		console.log(data);
	}
});





 */