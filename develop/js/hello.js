// hello.js
let greeting = "Hello from Node.js!";
console.log(greeting);

let num1 = 5;
let num2 = 10;
console.log(`The sum is: ${num1 + num2}`);

let daysBack = 1;

    async function fetchData(sensorId, daysBack) {
      const since = daysBack * 24 * 60 * 60; // days → seconds
      //- viewer/api is a read only location defined in nginx that redirects to /api to avoid auth
      const url = `https://data.hetsa.nu/viewer/api/strudeviken?measurement=${sensorId}&since=${since}`;
      const response = await fetch(url);
      const data = await response.json();
      return data.result;
    }

    const sensors = new Map();
    sensors.set('Gr&aring;', '28:3E:B5:8F:35:20:01:4A');
    sensors.set('R&ouml;da', '28:FF:64:1F:5B:A7:57:86');

    const dataSets = [];
    for (const [name, address] of sensors) {
        const data = await fetchData(address, daysBack);
        dataSets.push({ name, data });
    }

    //console.log(dataSets[0]);

    const dataset = dataSets[0].data;

    const times = dataset.map(d => new Date(d.time * 1000));
    const values = dataset.map(d => d.value);

    console.log(times);
    console.log(values);
/*
    for (const [name, address] of sensors) {
        console.log(`Sensor Name: ${name}, Address: ${address}`);
    }
*/
