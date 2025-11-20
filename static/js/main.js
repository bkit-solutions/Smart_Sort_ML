// main.js - small UI helpers
(function(){
  // navbar shadow toggle
  const nav = document.querySelector(".navbar");
  if(nav){
    window.addEventListener("scroll", () => {
      if(window.scrollY > 30) nav.classList.add("shadow-sm");
      else nav.classList.remove("shadow-sm");
    });
  }

  // optional: make carousel autoplay faster
  try{
    const carousel = document.querySelector('#heroSlides');
    if(carousel) {
      const bsCarousel = bootstrap.Carousel.getOrCreateInstance(carousel, { interval: 6000 });
    }
  }catch(e){console.warn(e)}
})();
