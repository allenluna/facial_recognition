let logo = document.querySelector("#logo")
let navbar = document.querySelector("#navbar")

logo.onclick = () => {
    navbar.classList.toggle("show")

    let navbarItem = document.querySelectorAll(".link span");

    navbarItem.forEach(item => {
        item.classList.toggle("active")
    })

    document.querySelector(".logo-link-burger").classList.toggle("active")
    document.querySelector(".logo-link").classList.toggle("active")
}