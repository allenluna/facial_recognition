// for open camera
let openCamera = document.querySelector("#openCamera")
let closeCamera = document.querySelector("#closeCamera")
let cameraStream = document.querySelector("#photoStream")
let cameraBackgroundWrapper = document.querySelector(".img-wrapper-data")
let imageTitleSection = document.querySelector("#photoTitle")
let inputSection = document.querySelector(".inputsection")
let trainModalData = document.querySelector("#trainStudent")
openCamera.addEventListener("click", () => {
    fetch("/add/start-cam", {
        method : "POST",
        headers : {"Content-Type" : "application/json"},
        body : JSON.stringify({"start" : openCamera.id, "close" : "close"}),
    }).then(res => res.json()).then(() => {
        openCamera.style.display = "none"
        closeCamera.style.display = "block"
        cameraStream.src = "/add/open-cam"
        cameraBackgroundWrapper.classList.remove("img-wrapper")
        cameraBackgroundWrapper.classList.add("img-wrapper-change")
        inputSection.style.display = "block"
        imageTitleSection.innerHTML = "Smile! 😊"
    })
})

const pageAccessedByReload = (
    (window.performance && window.performance.type === 1) ||
      window.performance
        .getEntriesByType('navigation')
        .map((nav) => nav.type)
        .includes('reload')
  );

if(pageAccessedByReload == true){
    fetch("/add/start-cam", {
        method : "POST",
        headers : {"Content-Type" : "application/json"},
        body : JSON.stringify({"start" : "start", "close" : closeCamera.id}),
    })
}

// close camera
closeCamera.addEventListener("click", () => {
    fetch("/add/start-cam", {
        method : "POST",
        headers : {"Content-Type" : "application/json"},
        body : JSON.stringify({"start" : "start", "close" : closeCamera.id}),
    }).then(res => res.json()).then((res) => {
        console.log(res["message"])
        openCamera.style.display = "block"
        closeCamera.style.display = "none"
        cameraStream.src = "static/assets/hero.png"
        cameraBackgroundWrapper.classList.add("img-wrapper")
        cameraBackgroundWrapper.classList.remove("img-wrapper-change")
        inputSection.style.display = "none"
        imageTitleSection.innerHTML = "Hello. Take your photo"
    })
})

// input field design
let inputItems = document.querySelectorAll(".inputField")
inputItems.forEach(item => {
    item.addEventListener("input", (e) => {
        if(e.target.value != ""){
            e.target.classList.add("is-valid")
        }else{
            e.target.classList.remove("is-valid")
        }
    })
})

// add student form data to the database
let studId;
document.querySelector("#saveDatabase").addEventListener("click", e => {
    e.preventDefault()
    let studentData = studentForm()
    let firstname = document.querySelector("#firstname");
    let lastname = document.querySelector("#lastname")
    let address = document.querySelector("#address")
    let number = document.querySelector("#number")
    fetch("/add/add-student-data", {
        method : "POST",
        body : studentData
    }).then(res => res.json())
    .then(res => {

        let message = res["message"]
        // for training modal data
        studentToTrain(message)
        studId = message.id
        if(firstname.value == ""){
            firstname.classList.remove("is-valid")
            firstname.classList.add("is-invalid")
        }else if(lastname.value == ""){
            lastname.classList.remove("is-valid")
            lastname.classList.add("is-invalid")
        }else if(address.value == ""){
            address.classList.remove("is-valid")
            address.classList.add("is-invalid")
        }else if(number.value == ""){
            number.classList.remove("is-valid")
            number.classList.add("is-invalid")
        }
    firstname.classList.remove("is-valid")
    lastname.classList.remove("is-valid")
    address.classList.remove("is-valid")
    number.classList.remove("is-valid")
    document.querySelector("#studForm").reset()

    })
})


document.querySelector("#trainStudentImage").addEventListener("click", () => {
    
    fetch(`/add/train-student-data?student=${studId}`).then(res => res.json()).then(res => {
            console.log(res["message"])
        })
    trainModalData.innerHTML = ""
})


const studentToTrain = (data) => {
    let studentImage = document.createElement("div")
    studentImage.className = "studentToTrainData"
    studentImage.innerHTML = `
    <p>Train this image for face attendance facial recognition. required</p>
    <h1>${data.firstname} ${data.lastname}</h1>
    `

    trainModalData.appendChild(studentImage)
}


// student form data function
const studentForm = () => {
    let firstname = document.querySelector("#firstname");
    let lastname = document.querySelector("#lastname")
    let address = document.querySelector("#address")
    let number = document.querySelector("#number")

    let newForm = new FormData()
    newForm.append("firstname", firstname.value)
    newForm.append("lastname", lastname.value)
    newForm.append("address", address.value)
    newForm.append("number", number.value)

    return newForm
}
