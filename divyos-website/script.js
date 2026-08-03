// Smooth Scroll

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e) {

        e.preventDefault();

        document.querySelector(this.getAttribute("href")).scrollIntoView({

            behavior: "smooth"

        });

    });

});


// Header Shadow on Scroll

const header = document.querySelector("header");

window.addEventListener("scroll", () => {

    if (window.scrollY > 50) {

        header.style.background = "rgba(0,0,0,0.85)";
        header.style.boxShadow = "0 5px 20px rgba(0,0,0,0.4)";

    }

    else {

        header.style.background = "rgba(0,0,0,0.5)";
        header.style.boxShadow = "none";

    }

});


// Reveal Animation

const cards = document.querySelectorAll(".card");

const observer = new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.style.opacity="1";
            entry.target.style.transform="translateY(0px)";

        }

    });

});

cards.forEach(card=>{

    card.style.opacity="0";
    card.style.transform="translateY(40px)";
    card.style.transition=".8s";

    observer.observe(card);

});


// Download Message

const downloadButtons = document.querySelectorAll(".btn");

downloadButtons.forEach(button=>{

    button.addEventListener("click",()=>{

        alert("Thanks for downloading DivyOS 🚀");

    });

});


// Current Year

const footer = document.querySelector("footer p");

footer.innerHTML =
`© ${new Date().getFullYear()} DivyOS • Developed by Divyansh Singh`;