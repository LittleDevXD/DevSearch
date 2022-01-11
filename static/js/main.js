
// multiple pages work while searching with keywords

// Get search form
let searchForm = document.getElementById("searchForm")

// Page Links
let pageLinks = document.getElementsByClassName("page-link")
for (let i=0; i < pageLinks.length; i++) {
    // Everytime a page link is clicked, trigger this func
    pageLinks[i].addEventListener("click", function (e) {
        // Prevent Default Behaviours
        e.preventDefault()
        console.log(pageLinks[i])
        // Get page no. sent by data_page attribute
        let page = this.dataset.page
        console.log(page)
        // Add a hidden input to Form 
        searchForm.innerHTML += `<input value=${page} name="page" hidden>`

        // Submit Search Form
        searchForm.submit()
    })
}