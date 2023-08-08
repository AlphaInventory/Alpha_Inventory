const inputIcono = document.querySelector('.mostrar')
const inputPassword = document.querySelector('.input_password')

inputIcono.addEventListener('click', () => {
    inputIcono.classList.toggle('fa-eye-slash')
    inputIcono.classList.toggle('fa-eye')
    inputPassword.type = inputPassword.type === 'password' ? 'text' : 'password'
})

const inputIcono_ = document.querySelector('.mostrar-')
const inputPassword_ = document.querySelector('.input_password-')

inputIcono_.addEventListener('click', () => {
    inputIcono_.classList.toggle('fa-eye-slash')
    inputIcono_.classList.toggle('fa-eye')
    inputPassword_.type = inputPassword_.type === 'password' ? 'text' : 'password'
})

const inputIcono__ = document.querySelector('.mostrar--')
const inputPassword__ = document.querySelector('.input_password--')

inputIcono__.addEventListener('click', () => {
    inputIcono__.classList.toggle('fa-eye-slash')
    inputIcono__.classList.toggle('fa-eye')
    inputPassword__.type = inputPassword__.type === 'password' ? 'text' : 'password'
})