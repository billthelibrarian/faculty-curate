
// react to search button click

        // validate input box terms



// react to reset button click

        // clear input box

function clearMainSearchBox() {
        document.getElementById("main-search-box").value == "";

}






// display table in div id=results-table




function makeDataTable() {
        console.log("TEST");

        let btn = document.getElementById("search-button");
        btn.addEventListener("click", function handleClick() {
                let searchTerms = document.getElementById("main-search-box").value;
                console.log(searchTerms); 
        });
    
    }






