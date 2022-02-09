
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

// Remove tags with one click while updating project
let tags = document.getElementsByClassName('project-tag');

for (let i=0; i<tags.length; i++) {
    tags[i].addEventListener('click', (e) => {
        let tagID = e.target.dataset.tag;
        let projectID = e.target.dataset.project;

        // Delete relationship in Backend with api
        fetch("http://127.0.0.1:8000/api/remove-tag/", {
            method: 'DELETE',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify({'project':projectID, 'tag':tagID})
        })
        .then(response => response.json())
        .then(data => {})

        // Remove frontend tag
        e.target.remove()
    })
}