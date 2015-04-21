var $ = django.jQuery;

function toggleJourneeContinue(day) {
	if ($('#id_' + day + '_journee_continue').prop('checked')) {
		if($('#id_' + day + '_matin_ferme').prop('checked'))
		{
			$('#id_' + day + '_matin_ferme').attr('checked',false);
			$('#id_' + day + '_matin_fin').attr('disabled', false);
			$('#id_' + day + '_matin_fin').next().attr('disabled', false);
			$('#id_' + day + '_matin_debut').attr('disabled', false);
			$('#id_' + day + '_matin_debut').next().attr('disabled', false);
			$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1908px');
			$('#id_' + day + '_matin_debut').next().css('background-position', ' 0 -1908px');
            $('#id_' + day + '_matin_fin').next().css('background-color', '#EEE');
			$('#id_' + day + '_matin_debut').next().css('background-color', '#EEE');
		}
		
		if($('#id_' + day + '_am_ferme').prop('checked'))
		{
			$('#id_' + day + '_am_ferme').attr('checked',false);
			$('#id_' + day + '_am_fin').attr('disabled', false);
			$('#id_' + day + '_am_fin').next().attr('disabled', false);
			$('#id_' + day + '_am_debut').attr('disabled', false);
			$('#id_' + day + '_am_debut').next().attr('disabled', false);
			$('#id_' + day + '_am_fin').next().css('background-position', ' 0 -1908px');
			$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1908px');
            $('#id_' + day + '_am_fin').next().css('background-color', '#EEE');
			$('#id_' + day + '_am_debut').next().css('background-position', '#EEE');
			
		}
		$('#id_' + day + '_matin_fin').attr('disabled', true);
		$('#id_' + day + '_matin_fin').next().attr('disabled', true);
		$('#id_' + day + '_am_debut').attr('disabled', true);
		$('#id_' + day + '_am_debut').next().attr('disabled', true);
		$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1908px');
		$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1908px');
        $('#id_' + day + '_matin_fin').next().css('background-color', '#EEE');
		$('#id_' + day + '_am_debut').next().css('background-color', '#EEE');
		$('#id_' + day + '_matin_fin').val('');
		$('#id_' + day + '_am_debut').val('');
		$('#id_' + day + '_matin_ferme').attr('disabled',true);
		$('#id_' + day + '_am_ferme').attr('disabled',true);
		
	} else {
		$('#id_' + day + '_matin_fin').attr('disabled', false);
		$('#id_' + day + '_matin_fin').next().attr('disabled', false);
		$('#id_' + day + '_am_debut').attr('disabled', false);
		$('#id_' + day + '_am_debut').next().attr('disabled', false);
		$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1865px');
		$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1865px');
        $('#id_' + day + '_matin_fin').next().css('background-color', '#EEE');
		$('#id_' + day + '_am_debut').next().css('background-color', '#EEE');
		$('#id_' + day + '_matin_ferme').attr('disabled',false);
		$('#id_' + day + '_am_ferme').attr('disabled',false);

	}

}

function toggleFermetureMatin(day) {
	if ($('#id_' + day + '_matin_ferme').prop('checked')) {
		$('#id_' + day + '_matin_fin').attr('disabled', true);
		$('#id_' + day + '_matin_fin').next().attr('disabled', true);
		$('#id_' + day + '_matin_debut').attr('disabled', true);
		$('#id_' + day + '_matin_debut').next().attr('disabled', true);
		$('#id_' + day + '_matin_debut').next().attr('disabled', true);
		$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1908px');
		$('#id_' + day + '_matin_debut').next().css('background-position', ' 0 -1908px');
        $('#id_' + day + '_matin_fin').next().css('background-color', '#EEE');
		$('#id_' + day + '_matin_debut').next().css('background-color', '#EEE');
		$('#id_' + day + '_matin_fin').val('');
		$('#id_' + day + '_matin_debut').val('');
		$('#id_' + day + '_journee_continue').attr('disabled', true)
	} else {
		$('#id_' + day + '_matin_fin').attr('disabled', false);
		$('#id_' + day + '_matin_fin').next().attr('disabled', false);
		$('#id_' + day + '_matin_debut').attr('disabled', false);
		$('#id_' + day + '_matin_debut').next().attr('disabled', false);
		$('#id_' + day + '_matin_fin').next().css('background-position', ' 0 -1865px');
		$('#id_' + day + '_matin_debut').next().css('background-position', ' 0 -1865px');
        $('#id_' + day + '_matin_fin').next().css('background-color', '#E1F0F5');
		$('#id_' + day + '_matin_debut').next().css('background-color', '#E1F0F5');
		$('#id_' + day + '_journee_continue').attr('disabled', false)

	}

}


function toggleFermetureAM(day) {
	if ($('#id_' + day + '_am_ferme').prop('checked')) {
		$('#id_' + day + '_am_fin').attr('disabled', true);
		$('#id_' + day + '_am_fin').next().attr('disabled', true);
		$('#id_' + day + '_am_debut').attr('disabled', true);
		$('#id_' + day + '_am_debut').next().attr('disabled', true);
		$('#id_' + day + '_am_debut').next().attr('disabled', true);
		$('#id_' + day + '_am_fin').next().css('background-position', ' 0 -1908px');
		$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1908px');
        $('#id_' + day + '_am_fin').next().css('background-color', '#EEE');
		$('#id_' + day + '_am_debut').next().css('background-color', '#EEE');
		$('#id_' + day + '_am_fin').val('');
		$('#id_' + day + '_am_debut').val('');
		$('#id_' + day + '_journee_continue').attr('disabled', true)

	} else {
		$('#id_' + day + '_am_fin').attr('disabled', false);
		$('#id_' + day + '_am_fin').next().attr('disabled', false);
		$('#id_' + day + '_am_debut').attr('disabled', false);
		$('#id_' + day + '_am_debut').next().attr('disabled', false);
		$('#id_' + day + '_am_fin').next().css('background-position', ' 0 -1865px');
		$('#id_' + day + '_am_debut').next().css('background-position', ' 0 -1865px');
        $('#id_' + day + '_am_fin').next().css('background-color', '#E1F0F5');
		$('#id_' + day + '_am_debut').next().css('background-color', '#E1F0F5');
		$('#id_' + day + '_journee_continue').attr('disabled', false)
	}

}

$(document).ready(function() {
	var days = ['lundi', 'mardi','mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    var i = 0;
	for (i = 0; i < days.length; i++) {

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

        toggleJourneeContinue(days[i]);
        toggleFermetureMatin(days[i]);
        toggleFermetureAM(days[i]);
		
	};

});
