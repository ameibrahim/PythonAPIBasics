let box = document.querySelector(".box");

let vehicleClass = 2
let engineSize = 5
let cylinders = 6
let transmission = 1
let CO2Rating = 6
let D = 0
let E = 0
let X = 1
let Z = 0

let url = `http://127.0.0.1:5000/get-results/?vehicleClass=${vehicleClass}&engineSize=${engineSize}&cylinders=${cylinders}&transmission=${transmission}&CO2Rating=${CO2Rating}&D=${D}&E=${E}&X=${X}&Z=${Z}`
async function getResults() {
    let result = await fetch(url, { 
        method: 'GET'
    });
    let JSONResult = await result.json();

    let fuel = JSONResult.fuel_result
    let co2 = JSONResult.CO2_result

    box.textContent = `Fuel: ${fuel}, CO2: ${co2}`;
}

getResults();
