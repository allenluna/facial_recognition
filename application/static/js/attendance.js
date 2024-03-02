document.querySelector("#openAttendance").addEventListener("click", () => {
    fetch("/add/open-attendance", {
        method : "POST",
        headers : {"Content-type": "application/json"},
        body : JSON.stringify({"open_attendance" : document.querySelector("#openAttendance").id})
    })
})

document.querySelector("#home").addEventListener("click", () => {
    fetch("/add/open-attendance", {
        method : "POST",
        headers : {"Content-type": "application/json"},
        body : JSON.stringify({"open_attendance" : document.querySelector("#home").id})
    })
})

document.querySelector("#addStudent").addEventListener("click", () => {
    fetch("/add/open-attendance", {
        method : "POST",
        headers : {"Content-type": "application/json"},
        body : JSON.stringify({"open_attendance" : document.querySelector("#addStudent").id})
    })
})