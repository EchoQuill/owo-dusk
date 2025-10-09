/*
This file is part of owo-dusk.

Copyright (c) 2024-present EchoQuill

Portions of this file are based on code by EchoQuill, licensed under the
GNU General Public License v3.0 (GPL-3.0).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
*/


var password = localStorage.getItem("password") || prompt("Enter Password");

if (password) {
  localStorage.setItem("password", password);
} else {
  alert("Password is required.");
  location.reload();
}


document.addEventListener("DOMContentLoaded", async () => {
  await handle_charts(); // Initial chart load
  await update_stat_cards(); // Initial stat card load
  setInterval(async () => {
    const data = await fetch_data("/api/console", false);
    console.log(data);
    logMessage(data);
    await update_stat_cards(); // Update stat cards every 3 seconds
    // If you want to re-render charts for real-time updates (more resource-intensive)
    // You would call handle_charts() here or specific chart update functions.
    // For now, we are focusing on the numerical stats.
  }, 3000);
});

function logMessage(data) {
  const consoleElement = document.getElementById("messages");

  consoleElement.innerHTML = data;
  consoleElement.scrollTop = consoleElement.scrollHeight;
}

async function handle_gamble_earnings_chart() {
  const data = await fetch_data("/api/fetch_gamble_data");
  console.log(data)

  var ctx = document.getElementById('gamble_earnings').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        '12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM',
        '7 AM', '8 AM', '9 AM', '10 AM', '11 AM',
        '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM',
        '7 PM', '8 PM', '9 PM', '10 PM', '11 PM'
      ],
      datasets: [
        {
          label: 'Winnings',
          data: data.win_data,
          fill: false,
          borderColor: 'rgb(0, 200, 0)',
          backgroundColor: 'rgb(0, 200, 0)',
          tension: 0.2
        },
        {
          label: 'Losses',
          data: data.lose_data,
          borderColor: 'rgb(220, 53, 69)',
          backgroundColor: 'rgb(220, 53, 69)',
          tension: 0.2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      devicePixelRatio: 4,
      plugins: {
        legend: {
          position: 'top',
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Win/Loss count'
          },
          grid: {
            display: true,
            color: 'rgba(102, 64, 199, 0.3)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Time of Day'
          },
          grid: {
            display: true,
            color: 'rgba(102, 64, 199, 0.3)'
          }
        }
      }
    }
  });
}

async function handle_weekly_runtimes_chart() {
  const data = await fetch_data("/api/fetch_weekly_runtime");
  console.log(data)


  var ctx = document.getElementById('weekly_runtimes');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      datasets: [{
        label: 'Minutes Ran',
        data: data.runtime_data,
        backgroundColor: [
          'rgb(190, 128, 248)',
          'rgb(170, 88, 247)',
          'rgb(130, 45, 209)',
          'rgb(121, 28, 209)',
          'rgb(102, 10, 189)',
          'rgb(78, 4, 146)',
          'rgb(53, 3, 100)'
        ],
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      devicePixelRatio: 4,
      plugins: {
        legend: {
          position: 'top',
        }
      },
      scales: {
        x: {
          grid: {
            display: true,
            color: 'rgba(102, 64, 199, 0.3)'
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            display: true,
            color: 'rgba(102, 64, 199, 0.3)'
          }
        }
      }
    }
  });

  // Removed direct update here, moved to update_stat_cards() for real-time updates
  // var ctx = document.getElementById('total_uptime_card');
  // ctx.innerText = uptime_calc(data.current_uptime);
}

async function handle_cowoncy_earnings_chart() {
  const data = await fetch_data("/api/fetch_cowoncy_data");
  console.log(data);

  var ctx = document.getElementById('cowoncy_earnings');
  new Chart(ctx, {
    type: 'line',
    data: data.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      devicePixelRatio: 4,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            boxWidth: 10,
          }
        }
      },
      scales: {
        x: {
          type: 'category',
          ticks: {
            maxRotation: 45,
            minRotation: 30,
          },
          grid: {
            display: true,
            color: 'rgba(102, 64, 199, 0.3)'
          }
        },
        y: {
          beginAtZero: true,
          stacked: true,
          ticks: {
            stepSize: 200,
          },
          grid: {
            display: true,
            color: 'rgba(102, 64, 199, 0.3)'
          }
        }
      }
    }
  });

  // Removed direct updates here, moved to update_stat_cards() for real-time updates
  // var ctx = document.getElementById('total_cash_card');
  // ctx.innerText = data.total_cash;
  // var ctx = document.getElementById('total_captchas_card');
  // ctx.innerText = data.total_captchas;

}

async function handle_total_commands_chart() {
  var ctx = document.getElementById('total_commands');
  const data = await fetch_data("/api/fetch_cmd_data");
  console.log(data);

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.command_names,
      datasets: [{
        label: 'Times send',
        data: data.count,
        backgroundColor: generateRandomRGB(data.count),
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      devicePixelRatio: 4,
      plugins: {
        legend: {
          position: 'left',
        }
      }
    }
  });

  // Removed direct update here, moved to update_stat_cards() for real-time updates
  // let temp = 0;
  // for (let i = 0; i < data.count.length; i++) {
  //   temp += data.count[i];
  // }
  // var ctx = document.getElementById('total_commands_card');
  // ctx.innerText = temp;
}


async function fetch_data(api_addr, is_json=true) {
  try {
    const response = await fetch(api_addr, {
      method: 'GET',
      headers: {
        'password': password // Replace with your actual password
      }
    });

    if (!response.ok) {
      throw new Error("Failed to fetch command data");
    }

    let data;
    if (is_json) {
      data = await response.json();
    } else {
      data = await response.text();
      console.log("success in fetching data!");
      return data; // Return early if not JSON
    }


    if (data.status !== "success") {
      throw new Error("API returned an error");
    } else {
      console.log("success in fetching data!")
      return data
    }
 } catch (error) {
    console.error("Error when fetching data:", error);
  }
}

function generateRandomRGB(arr) {
  return arr.map(() => {
    const r = Math.floor(Math.random() * 156);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`;
  });
}
async function handle_charts() {
  await handle_total_commands_chart();
  await handle_cowoncy_earnings_chart();
  await handle_weekly_runtimes_chart();
  await handle_gamble_earnings_chart();
}

// New/Modified function to update stat cards, now including Uptime and Commands
async function update_stat_cards() {
  // Update Total Cash and Captchas
  const cowoncyData = await fetch_data("/api/fetch_cowoncy_data");
  if (cowoncyData) {
    document.getElementById('total_cash_card').innerText = cowoncyData.total_cash;
    document.getElementById('total_captchas_card').innerText = cowoncyData.total_captchas;
  }

  // Update Daily Uptime
  const runtimeData = await fetch_data("/api/fetch_weekly_runtime");
  if (runtimeData && runtimeData.current_uptime) {
    document.getElementById('total_uptime_card').innerText = uptime_calc(runtimeData.current_uptime);
  }

  // Update Commands
  const cmdData = await fetch_data("/api/fetch_cmd_data");
  if (cmdData && cmdData.count) {
    let totalCommands = 0;
    for (let i = 0; i < cmdData.count.length; i++) {
      totalCommands += cmdData.count[i];
    }
    document.getElementById('total_commands_card').innerText = totalCommands;
  }
}

function uptime_calc(arr) {
  let sec = arr[1] - arr[0];

  const hours = Math.floor(sec / 3600);
  const minutes = Math.floor((sec % 3600) / 60);
  let seconds = Math.round(sec % 60);

  // Handle rounding overflow (e.g., 59.6 → 60)
  if (seconds === 60) {
    seconds = 0;
    if (minutes === 59) {
      minutes = 0;
      hours += 1;
    } else {
      minutes += 1;
    }
  }

  const h = String(hours).padStart(2, '0');
  const m = String(minutes).padStart(2, '0');
  const s = String(seconds).padStart(2, '0');

  return `${h}:${m}:${s}`;
}