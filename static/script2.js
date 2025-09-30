document.addEventListener('DOMContentLoaded', function () {
    // Gérer la soumission du formulaire de création de voyage
    const voyageForm = document.getElementById('voyageForm');
    if (voyageForm) {
        voyageForm.addEventListener('submit', function(e) {
            e.preventDefault();  // Empêche la soumission par défaut

            // Récupérer les données du formulaire
            const destination = document.getElementById('destination').value;
            const start_date = document.getElementById('start_date').value;
            const end_date = document.getElementById('end_date').value;
            const type = document.getElementById('type').value;
            const budget = document.getElementById('budget').value;
            const transport = document.querySelector('input[name="transport"]').checked ? 'Oui' : 'Non';
            const eco = document.querySelector('input[name="eco"]').checked ? 'Oui' : 'Non';

            // Vérification des champs obligatoires
            if (!destination || !start_date || !end_date || !type || !budget) {
                alert('Veuillez remplir tous les champs obligatoires.');
                return;
            }

            // Stocker les données dans le localStorage
            localStorage.setItem('voyageData', JSON.stringify({
                destination: destination,
                start_date: start_date,
                end_date: end_date,
                type: type,
                budget: budget,
                transport: transport,
                eco: eco
            }));

            // Rediriger vers la page de confirmation
            window.location.href = 'voyage_confirme.html';
        });
    }

    // Gérer l'inscription
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;

            // Vérification des mots de passe et des champs obligatoires
            if (!name || !email || !password || !confirmPassword) {
                alert('Veuillez remplir tous les champs.');
                return;
            }

            if (password !== confirmPassword) {
                document.getElementById('errorMessage').style.display = 'block';
                return;
            }

            // Enregistrement de l'utilisateur dans le localStorage
            localStorage.setItem('user', JSON.stringify({
                name: name,
                email: email,
                password: password
            }));

            // Afficher le message de succès
            document.getElementById('errorMessage').style.display = 'none';
            document.getElementById('successMessage').style.display = 'block';

            // Redirection vers la page de connexion après inscription
            setTimeout(() => {
                window.location.href = 'se_connecter.html';
            }, 2000);
        });
    }

    // Gérer la connexion
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.getElementById('login_email').value;
            const password = document.getElementById('login_password').value;

            // Vérification des champs
            if (!email || !password) {
                alert('Veuillez entrer votre email et votre mot de passe.');
                return;
            }

            // Récupérer l'utilisateur enregistré
            const user = JSON.parse(localStorage.getItem('user'));

            // Vérifier les informations de connexion
            if (user && user.email === email && user.password === password) {
                // Connexion réussie
                alert('Connexion réussie, bienvenue ' + user.name);
                // Redirection vers la page client
                window.location.href = 'client.html'; // Redirection vers la page client
            } else {
                // Afficher un message d'erreur
                document.getElementById('loginErrorMessage').style.display = 'block';
            }
        });
    }

    // Toggle visibility of additional options
    const showMoreToggle = document.getElementById('show-more-toggle');
    const additionalOptions = document.getElementById('additionalOptions');
    
    if (showMoreToggle && additionalOptions) {
        showMoreToggle.addEventListener('click', function() {
            console.log("Toggle button clicked"); // Debugging: Check if button click is registered

            if (additionalOptions.style.display === 'none' || additionalOptions.style.display === '') {
                additionalOptions.style.display = 'block';
                this.textContent = 'Moins de critères';
                console.log("Additional options displayed"); // Debugging: Confirm visibility change
            } else {
                additionalOptions.style.display = 'none';
                this.textContent = 'Plus de critères';
                console.log("Additional options hidden"); // Debugging: Confirm visibility change
            }
        });
    } else {
        console.error("show-more-toggle or additionalOptions element not found");
    }
});
// À la fin de script.js
document.addEventListener('DOMContentLoaded', ()=>{
  const prefill = localStorage.getItem('assistant_prefill');
  if(prefill && document.getElementById('msg')){
    document.getElementById('msg').value = `Itinéraire pour ${prefill}`;
    localStorage.removeItem('assistant_prefill');
  }
});


// Effets d'apparition sur la home
document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('.reveal').forEach(el=>{
    const io = new IntersectionObserver((entries)=>entries.forEach(e=>e.isIntersecting && el.classList.add('visible')), {threshold:.12});
    io.observe(el);
  });
});
