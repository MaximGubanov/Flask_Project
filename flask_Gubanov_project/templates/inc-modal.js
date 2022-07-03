const modalWindow = document.getElementById("deleteModal")
const btnCloseModal = document.getElementById("btnCloseModal")
const btnDelete = document.getElementById("btnDelete")

btnDelete.addEventListener('click', () => {
    modalWindow.classList.add('hidden')
})

btnCloseModal.addEventListener('click', () => {
    modalWindow.classList.remove('hidden')
})

