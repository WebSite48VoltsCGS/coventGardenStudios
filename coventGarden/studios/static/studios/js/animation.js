/* Animation fiche technique */ 

function showImage(element) {
	var modal = document.getElementById("imageModal");
	var modalImage = document.getElementById("modalImage");
  
	// Récupérer l'URL de l'image à afficher
	var imageUrl = element.getAttribute("src");
  
	// Affecter l'URL de l'image au modalImage
	modalImage.setAttribute("src", imageUrl);
  
	// Afficher le modal
	modal.style.display = "block";
  }
  
  function hideImage() {
	var modal = document.getElementById("imageModal");
  
	// Masquer le modal
	modal.style.display = "none";
  }
  
