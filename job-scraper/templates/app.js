var data = "";
const controls = {
    inputs: {
        jobTitle: d3.select("#jobTitle"),
        language: d3.select("#languages").node(), //Node is used to select the actual HTML element rather than a D3 object
        location: d3.select("#location")
    },
    submitButton: d3.select("#button"),
    tableBody: d3.select("tbody")
}

function init() {
    populatePageControls();//On page load, populates the controls (dropdowns, etc)
    
    controls.submitButton.on("click", populateSearchResults);
}

async function loadData() { //Async method to load in the data
    var initialDataFromFile = await d3.csv("aswift_prog.csv");
    data = filterNulls(initialDataFromFile);
}

async function populatePageControls() {
    await loadData(); //Waits for the data to be loaded before attempting to populate the controls as they need the data
    populateLanguagesDropdown();
}

async function populateLanguagesDropdown() {
    var languages = [];

    for (var i = 0; i < data.length; i++) {
        var singleItemLanguages = formatLanguageData(data[i]["Language"], "Array"); //Fetches the array for each job's languages
        languages = languages.concat(singleItemLanguages); //Adds the languages from this job to the main languages array
    }

    languages = Array.from(new Set(languages)); //Removes duplicates by converting to a set which can only contain unique values then converting back to array

    var dropdownAll = document.createElement("option");
    dropdownAll.innerHTML = "Default";
    dropdownAll.value = 0;
    controls.inputs.language.options.add(dropdownAll);

    languages.forEach((item, index) => { //For each language in the languages array, creates a new option in the dropdown
        var dropdownItem = document.createElement("option");
        dropdownItem.innerHTML = item;
        dropdownItem.value = item;
        controls.inputs.language.options.add(dropdownItem);
    });
}

function populateSearchResults(event) {
    event.preventDefault();

    var selectedJobTitle = controls.inputs.jobTitle.property("value").toLowerCase().trim();
    var selectedLanguage = controls.inputs.language.value;
    var selectedLocation = controls.inputs.location.property("value").toLowerCase().trim();

    var searchResults = data.filter(job => job.JobTitle.toLowerCase().includes(selectedJobTitle));
    searchResults = searchResults.filter(job => job.Location.toLowerCase().includes(selectedLocation));
    searchResults = searchResults.filter(job => job.Language.toLowerCase().includes(selectedLanguage) || selectedLanguage == 0);
    

    outputDataTable(searchResults);
}

function outputDataTable(data) {
    controls.tableBody.html("");
    for (var i = 0; i < data.length; i++) {
        var HTMLContentString = "<td>" + [i+1] + "</td>";
        
        for(var key in data[i]) {
            var formattedDataItem = data[i][key];
            
            if (key === "Language") { //IF it's the language column, calls the formatter to make it display in a neater way
                formattedDataItem = formatLanguageData(data[i][key], "String");
            }
            
            HTMLContentString += "<td>" + formattedDataItem + "</td>"
        }

        controls.tableBody.insert("tr").html(HTMLContentString);
    }
}

function formatLanguageData(initialLanguageData, formatType) {
    var strippedLanguageData = initialLanguageData.replace(/[\[\]'\s]+/g,''); //Removes all the brackets and ' from the string
    var languageDataArray = strippedLanguageData.split(","); //Converts the string into an array by splitting the items at each comma
    
    if (formatType === "Array") { //Returns the data array for use in populating the dropdown which needs an array
        return languageDataArray;
    }
    else if (formatType === "String") { //Returns a neat looking string for displaying on the page
        return languageDataArray.join(", "); //Joins the array into a formatted string using commas
    }
}

function filterNulls(data) {
    return data.filter(item => Object.values(item).every(value => {
        if (value === null || value === undefined || value === '') {
            return false;
        }
        return true;
    }));
}

init();