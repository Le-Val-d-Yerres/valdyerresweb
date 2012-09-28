django.jQuery(document).ready(function($) {

	var myForm = document.getElementById("horaires_form");

	myForm.lundi_journee_continue.onclick = function(argument) {
		if (myForm.id_lundi_matin_fin.disabled == true) {
			myForm.id_lundi_matin_fin.disabled = false;
			myForm.id_lundi_matin_fin.nextSibling.disabled = false;
		} else {
			myForm.id_lundi_matin_fin.disabled = true;
			myForm.id_lundi_matin_fin.nextSibling.disabled = true;
			/**$('#id_lundi_matin_fin').hide();**/
			myForm.id_lundi_matin_fin.value = '';
		}

		if (myForm.id_lundi_am_debut.disabled == true) {
			myForm.id_lundi_am_debut.disabled = false;
			myForm.id_lundi_am_debut.nextSibling.disabled = false;
		} else {
			myForm.id_lundi_am_debut.disabled = true;
			myForm.id_lundi_am_debut.nextSibling.disabled = true;
			myForm.id_lundi_am_debut.value = '';
		}

	}










}); 