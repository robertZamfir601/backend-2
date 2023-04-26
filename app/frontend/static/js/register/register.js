const baseURL = "http://localhost:8000/"

async function  logMeIn() {
   let r;
   let link = baseURL + "register"
   var data = new FormData(regForm);
   try {
      let response = await fetch(link, {
         method: "POST",
         body: data,
         headers: {
         },
         mode: 'no-cors'
      })
      return response
   } catch (error) {
      console.log("error " + error)
   }
}

const regForm = document.getElementById("regForm")
const username = document.getElementById("username")
const password = document.getElementById("password")
const re_password = document.getElementById("floatingPassword_verif")
const errorElement = document.getElementById('error')
regForm.addEventListener("submit", regSubmit)


async function regSubmit(event) { 
   event.preventDefault()
   let messages = [];

   if (username.value === '' || username.value == null ) {
      messages.push('Email is not valid');
   }

   if (password.value !== re_password.value) {
      messages.push('Passwoards do not match')
   }

   if (messages.length > 0) {
      errorElement.innerText = messages.join('\n')
   } else {
      let res = await logMeIn();

      if (res.status === 401) {
         messages.push('Email already taken')
         errorElement.innerText = messages.join('\n')
      } else if (res.status === 200) {
         let d = await res.json()
         token = d.token;
         const expires = new Date(Date.now() + 3600 * 1000 * 24); // 24 hours from now
         document.cookie = `token=${token}; expires=${expires.toUTCString()}; path=/`;

         window.location.href = "/profile"
      }
   }
}

