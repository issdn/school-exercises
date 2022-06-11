const XLSX = require("xlsx");
const graph = require("./graph");

class XLSXParser {
  /**
   * @param {Array} currencyTableTuple - Kolejka 5 walut z tabeli. Trzyba maksymalnie 5 elementow.
   */
  constructor(filepath) {
    this.filepath = filepath;
    this.file = this.parseExcel(this.filepath)[0].data;
    this.tableBody = document.getElementById("exchange-rates-tbody");
    this.currencyTableTuple = [];
  }

  /**
   *
   * @param {String} filename - Absolutna sciezka pliku.
   * @returns {any}
   */
  parseExcel = (filename) => {
    const excelData = XLSX.readFile(filename, { cellDates: true });

    return Object.keys(excelData.Sheets).map((name) => ({
      name,
      data: XLSX.utils.sheet_to_json(excelData.Sheets[name]),
    }));
  };

  /**
   * Zmienia wszystkie pelne daty excel na skrocone. Eg. Tue May 25 2022 00:00:00 (East Pacific) -> May-25-2022
   * @param {Object} sheet - Plik zwrocony przez funkcje parseExcel.
   * @returns {Object}
   */
  clearDates = (sheet) => {
    sheet.forEach((row, index) => {
      const date = Object.values(row)[0];
      const dateArr = date.toString().split(" ");
      let finalDate;
      if (dateArr.length > 4) {
        const newDateArr = dateArr.slice(1, 4);
        finalDate = newDateArr.join("-");
      } else {
        finalDate = dateArr.join(" ");
      }
      sheet[index]["data"] = finalDate;
    });
    return sheet;
  };

  /**
   * Ze slownika robi liste. Tzn. ze zwroconego przez parseExcel objektu {data: May-25-2022, nazwa waluty : wartosc} robi liste [May-25-2022, wartosc, wartosc]
   * @param {Object} sheet - Objekt zwrocony przez funkcje parseExcel lub clearDates.
   * @returns {Array}
   */
  currenciesObjectToArray = (sheet) => {
    let sheetArr = [];
    sheet.forEach((obj) => {
      sheetArr.unshift(Object.values(obj));
    });
    return sheetArr;
  };

  /**
   *
   * @param {String} name - Skrocona nazwa waluty.
   * @returns {Array} - Zwraca liste wszystkich wartosci walut.
   */
  getCurrencyFluctuation = (name) => {
    let fluctuation = {};
    const data = this.getCurrencies(false);
    data.forEach((row) => {
      fluctuation[row["data"]] = row[name];
    });
    return fluctuation;
  };

  /**
   * Rysuje graf historii wartosci waluty.
   * @param {Object} e - DOM Event.
   * @param {String} name - Skrocona nazwa waluty.
   */
  graphCurrency = (e, name) => {
    // Tutaj dodaje nazwe waluty do kolejki tak zeby po 5 kliknietych walutach,
    //automatycznie usuwala sie z grafu pierwsza kliknieta waluta.
    this.currencyTableTuple.push(name);

    // Bierze liste historii wartosci waluty i wywoluje funkcje, ktora rysuje wykres.
    const fluctuation = this.getCurrencyFluctuation(name);
    addData(name, fluctuation);

    // tr-activated nie tylko jest do zmiany tla poszczegolnych funkcji
    // ale tez do decydowania o tym czy ten element powinien byc zdjety czy narysowany na wykresie.
    e.target.classList.toggle("tr-activated");

    // Po 5 walutan na grafie, usuwa pierwszy element z listy "datasets" grafu.
    if (this.currencyTableTuple.length > 5) {
      Array.from(document.getElementsByClassName("tr-activated")).forEach(
        (tr) => {
          if (tr.attributes.currency.value === this.currencyTableTuple[0]) {
            tr.classList.toggle("tr-activated");
            removeData(tr.attributes.currency.value);
            chart.update();
          }
        }
      );
      // Po 5 walutan na grafie, usuwa pierwszy element z kolejki.
      this.currencyTableTuple.shift();
    }
  };

  /**
   * Usuwa walute z wykresu.
   * @param {Object} e - DOM Event.
   * @param {String} name - Skrocona nazwa waluty.
   */
  removeCurrencyFromGraph = (e, name) => {
    e.target.classList.toggle("tr-activated");

    // Usuwa element z kolejki poczym z wykresu funkcja *removeData* w calosci.
    const eIndex = this.currencyTableTuple.indexOf(name);
    if (eIndex > -1) this.currencyTableTuple.splice(eIndex, 1);

    removeData(name);
  };

  /**
   *  Jezeli kliknieta w tabeli waluta nie ma klasy *tr-activated* to ta funkcja dodaje ja do wykresu.
   *  Jezeli natomiast ma, to usuwa ja.
   * @param {Object} e - DOM Event.
   */
  handleTableCurrencyClick = (e) => {
    let graphed = e.target.classList.contains("tr-activated");
    const name = e.target.attributes.currency.value;

    graphed === false
      ? this.graphCurrency(e, name)
      : this.removeCurrencyFromGraph(e, name);
  };

  /**
   * Tworzy tabele z walutami.
   * @param {Array} row - Lista walut z jednego dnia.
   */
  exchangeRatesTable = (row) => {
    // Usuwa wykres poniewaz po usunieciu walut z tabeli, usuwaja sie takze ich potrzebne dla wykresu klasy.
    if (chart) chart.destroy();
    graphData("Wybierz walute.", []);
    // Usuwa pozostale waluty z tabeli.
    this.tableBody.innerHTML = "";
    // Usuwa niepotrzebne rzedy.
    delete row["nr tabeli"];
    delete row["pełny numer tabeli"];
    // Bierze dwie listy nazw walut i ich wartosci.
    const currencies = Object.keys(row);
    const values = Object.values(row);
    // Tworzy rzedy w tabeli, kazdy rzad to element html <tr>,
    // a w nim <th> w ktorej jest nazwa waluty i <td> w ktorej jest jej wartosc.
    currencies.forEach((currency, index) => {
      const row = document.createElement("tr");
      const currencyElem = document.createElement("th");
      const value = document.createElement("td");
      // W kazdej liscie powinna byc data na pierwszy miejscu,
      // wiec tu pomijane jest dodawanie do niej specjalnych argumentow.
      if (index === 0) {
        row.setAttribute("id", "date");
      } else {
        row.setAttribute("class", "currency");
        row.setAttribute("currency", currency);
        row.setAttribute("graphed", false);
        row.addEventListener("click", this.handleTableCurrencyClick);
      }
      currencyElem.appendChild(document.createTextNode(currency));
      value.appendChild(document.createTextNode(values[index]));
      row.appendChild(currencyElem);
      row.appendChild(value);
      tableBody.appendChild(row);
    });
  };

  /**
   * Tworzy menu z datami, po ktorych wyborze, zmienia sie tabela na te, z odpowiednim dniem.
   */
  datesToDropdown = () => {
    const sheet = this.getSheet();
    const clearedSheet = sheet.slice(3, sheet.length - 1);
    const currencies = document.getElementById("currencies");
    clearedSheet.forEach((row) => {
      const data = Object.values(row)[0];
      const option = document.createElement("option");
      option.value = data;
      option.appendChild(document.createTextNode(data));
      currencies.appendChild(option);
    });
  };

  /**
   *
   * @returns {Object} - Object z listami walut.
   */
  getSheet = () => {
    const clearedData = this.clearDates(this.file);
    return this.currenciesObjectToArray(clearedData);
  };

  /**
   * Usuwa niepotrzebne elementy z listy.
   * @param {boolean} reversed - Zapytanie czy lista powinna byc obrocona.
   * @returns {Array}
   */
  getCurrencies = (reversed = true) => {
    const clearedData = this.clearDates(this.file);
    if (reversed !== true) return clearedData.slice(1, clearedData.length - 3);
    return clearedData.slice(1, clearedData.length - 3).reverse();
  };
  /**
   * Na nowo tworzy tabele z walutami z odpowiedniego dnia.
   * @param {String} day - Dzien z tabeli.
   */
  updateExchangeRatesTable = (day) => {
    const currencies = this.getCurrencies();
    // Szuka listy z odpowiednim dniem i tworzy z niej tabele.
    currencies.forEach((row) => {
      if (day === row["data"]) {
        this.exchangeRatesTable(row);
      }
    });
  };

  /**
   * Tworzy pierwsza tabele z ostatniego dnia i dropdown menu.
   */
  updateDOMWithExcelData = () => {
    this.exchangeRatesTable(this.getCurrencies()[0]);

    const currencies = document.getElementById("currencies");
    currencies.innerHTML = "";
    this.datesToDropdown();
  };
}

let xlsxParser = undefined;
const tableBody = document.getElementById("exchange-rates-tbody");
const ratesForm = document.getElementById("exchange-rates-form");
const fileInput = document.getElementById("excel-file-input");

fileInput.addEventListener("input", (e) => {
  const invalid = document.getElementById("invalid-file");
  invalid.style.display = "none";
  invalid.innerHTML = "";
  const valid = document.getElementById("added-file");
  valid.style.display = "none";
  valid.innerHTML = "";
  const fileFormat = e.target.files[0].name.split(".").pop();

  if (fileFormat === "xlsx" || fileFormat === "xls") {
    document.getElementById("add-file-button").disabled = false;
    valid.style.display = "block";
    valid.appendChild(
      document.createTextNode("Dodano: " + e.target.files[0].name)
    );
  } else {
    invalid.style.display = "block";
    invalid.appendChild(
      document.createTextNode("Niepoprawny plik: " + e.target.files[0].name)
    );
    document.getElementById("add-file-button").disabled = true;
  }
});

// Po wybraniu daty z dropdown menu wywoluje funkcje updateExchangeRatesTable ktora tworzy tabele z wybranej daty.
ratesForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const exchangeRates = document.getElementById("currencies");
  const day = exchangeRates.value;
  xlsxParser.updateExchangeRatesTable(day);
});

// Po zaladowaniu pliku tworzy instancje klasy xlsxParser i wywoluje jej funkcje pdateDOMWithExcelData.
const fileInputForm = document.getElementById("file-input-form");
fileInputForm.addEventListener("submit", (e) => {
  e.preventDefault();
  e.stopPropagation();
  const fileInput = document.getElementById("excel-file-input");
  filepath = fileInput.files[0].path;
  xlsxParser = new XLSXParser(filepath);
  xlsxParser.updateDOMWithExcelData();
});

window.onload = graphData("Wybierz walute.", []);
