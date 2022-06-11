const Chart = require("chart.js");

let chart;
/**
 * Usuwa prosta wartosci waluty z wykresu za pomoca jej nazwy.
 * @param {String} name - Nazwa waluty.
 */
const removeData = (name) => {
  const datasets = chart.data.datasets;
  // Szuka w ktorej liscie etykieta ma taka sama nazwe jak parametr name i usuwa te liste z listy datasets.
  datasets.forEach((dataset, index) => {
    if (dataset.label == name) {
      datasets.splice(index, 1);
    }
  });
  chart.update();
};

/**
 *
 * @param {String} name - Nazwa waluty.
 * @param {Object} data - Objekt data.dataset.data porzebny dla wykresu z biblioteki chart.js. Tzn. {data : wartosc waluty}
 */
const addData = (name, data) => {
  // Wybiera losowy kolor dla prostej na wykresie.
  const a = Math.round(Math.random() * 255);
  const b = Math.round(Math.random() * 255);
  const c = Math.round(Math.random() * 255);
  const finalData = {
    label: name,
    data: data,
    fill: false,
    backgroundColor: [`rgba(${a},${b},${c},0.8)`],
    borderColor: [`rgba(${a},${b},${c},0.8)`],
    tension: 0.1,
    borderWidth: 2,
  };
  chart.data.datasets.push(finalData);
  chart.update();
};

/**
 * Tworzy pusty graf.
 */
const graphData = () => {
  const ctx = document.getElementById("chart").getContext("2d");
  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      maintainAspectRatio: false,
    },
  });
};
