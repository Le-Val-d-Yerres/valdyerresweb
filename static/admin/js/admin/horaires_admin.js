var $ = django.jQuery;

function toggleJourneeContinue(day) {
	if ($('#id_' + day + '_journee_continue').attr('checked')) {
		if($('#id_' + day + '_matin_ferme').attr('checked'))
		{
			$('#id_' + day + '_matin_ferme').attr('checked',false);
			$('#id_' + day + '_matin_fin').attr('disabled', false);
			$('#id_' + day + '_matin_fin').next().attr('disabled', false);
			$('#id_' + day + '_matin_debut').attr('disabled', false);
			$('#id_' + day + '_matin_debut').next().attr('disabled', false);
			$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1691px');
			$('#id_' + day + '_matin_debut').next().css('background-position', ' 0 -1691px');
		}
		
		if($('#id_' + day + '_am_ferme').attr('checked'))
		{
			$('#id_' + day + '_am_ferme').attr('checked',false);
			$('#id_' + day + '_am_fin').attr('disabled', false);
			$('#id_' + day + '_am_fin').next().attr('disabled', false);
			$('#id_' + day + '_am_debut').attr('disabled', false);
			$('#id_' + day + '_am_debut').next().attr('disabled', false);
			$('#id_' + day + '_am_fin').next().css('background-position', ' 0 -1691px');
			$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1691px');
			
		}
		$('#id_' + day + '_matin_fin').attr('disabled', true);
		$('#id_' + day + '_matin_fin').next().attr('disabled', true);
		$('#id_' + day + '_am_debut').attr('disabled', true);
		$('#id_' + day + '_am_debut').next().attr('disabled', true);
		$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1734px');
		$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1734px');
		$('#id_' + day + '_matin_fin').val('');
		$('#id_' + day + '_am_debut').val('');
		$('#id_' + day + '_matin_ferme').attr('disabled',true);
		$('#id_' + day + '_am_ferme').attr('disabled',true);
		
	} else {
		$('#id_' + day + '_matin_fin').attr('disabled', false);
		$('#id_' + day + '_matin_fin').next().attr('disabled', false);
		$('#id_' + day + '_am_debut').attr('disabled', false);
		$('#id_' + day + '_am_debut').next().attr('disabled', false);
		$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1691px');
		$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1691px');
		$('#id_' + day + '_matin_ferme').attr('disabled',false);
		$('#id_' + day + '_am_ferme').attr('disabled',false);

	}

}

function toggleFermetureMatin(day) {
	if ($('#id_' + day + '_matin_ferme').attr('checked')) {
		$('#id_' + day + '_matin_fin').attr('disabled', true);
		$('#id_' + day + '_matin_fin').next().attr('disabled', true);
		$('#id_' + day + '_matin_debut').attr('disabled', true);
		$('#id_' + day + '_matin_debut').next().attr('disabled', true);
		$('#id_' + day + '_matin_debut').next().attr('disabled', true);
		$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1734px');
		$('#id_' + day + '_matin_debut').next().css('background-position', ' 0 -1734px');
		$('#id_' + day + '_matin_fin').val('');
		$('#id_' + day + '_matin_debut').val('');
		$('#id_' + day + '_journee_continue').attr('disabled', true)
	} else {
		$('#id_' + day + '_matin_fin').attr('disabled', false);
		$('#id_' + day + '_matin_fin').next().attr('disabled', false);
		$('#id_' + day + '_matin_debut').attr('disabled', false);
		$('#id_' + day + '_matin_debut').next().attr('disabled', false);
		$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1691px');
		$('#id_' + day + '_matin_debut').next().css('background-position', ' 0 -1691px');
		$('#id_' + day + '_journee_continue').attr('disabled', false)

	}

}


function toggleFermetureAM(day) {
	if ($('#id_' + day + '_am_ferme').attr('checked')) {
		$('#id_' + day + '_am_fin').attr('disabled', true);
		$('#id_' + day + '_am_fin').next().attr('disabled', true);
		$('#id_' + day + '_am_debut').attr('disabled', true);
		$('#id_' + day + '_am_debut').next().attr('disabled', true);
		$('#id_' + day + '_am_debut').next().attr('disabled', true);
		$('#id_' + day + '_am_fin').next().css('background-position', ' 0 -1734px');
		$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1734px');
		$('#id_' + day + '_am_fin').val('');
		$('#id_' + day + '_am_debut').val('');
		$('#id_' + day + '_journee_continue').attr('disabled', true)

	} else {
		$('#id_' + day + '_am_fin').attr('disabled', false);
		$('#id_' + day + '_am_fin').next().attr('disabled', false);
		$('#id_' + day + '_am_debut').attr('disabled', false);
		$('#id_' + day + '_am_debut').next().attr('disabled', false);
		$('#id_' + day + '_am_fin').next().css('background-position', ' 0 -1691px');
		$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1691px');
		$('#id_' + day + '_journee_continue').attr('disabled', false)
	}

}

$(document).ready(function() {
	var days = ['lundi', 'mardi','mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

	for (var i = 0; i < days.length; i++) {

		$('#id_' + days[i] + '_journee_continue').bind('click', function() {

			day = $(this).attr('id').split('_')[1];
			
			toggleJourneeContinue(day);
			

		});

		$('#id_' + days[i] + '_matin_ferme').bind('click', function() {

			day = $(this).attr('id').split('_')[1];

			toggleFermetureMatin(day);

		});
		$('#id_' + days[i] + '_am_ferme').bind('click', function() {

			day = $(this).attr('id').split('_')[1];

			toggleFermetureAM(day);

		});
		
	};

});
