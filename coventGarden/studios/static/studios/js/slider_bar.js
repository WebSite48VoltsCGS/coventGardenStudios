var swiper = new Swiper(".mySwiper", {
    effect: "coverflow",
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: "auto",
    coverflowEffect: {
    rotate: 30,
    stretch: 0,
    depth: 40,
    modifier: 1,
    slideShadows: false,
    },
    pagination: {
    el: ".swiper-pagination",
    },
    initialSlide: 2, // Affiche la 3e image (index 2) par défaut
    });
    