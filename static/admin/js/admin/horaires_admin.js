var $ = django.jQuery;

$(document).ready(function() {
	var days = ['lundi', 'mardi']

	for (var i = 0; i < days.length; i++) {

		$('#id_' + days[i] + '_journee_continue').bind('click', function() {

			day = $(this).attr('id').split('_')[1];

			if ($('#id_' + day + '_matin_fin').is(':disabled')) {
				$('#id_' + day + '_matin_fin').attr('disabled', false);
				$('#id_' + day + '_matin_fin').next().attr('disabled', false);
			} else {
				$('#id_' + day + '_matin_fin').attr('disabled', true);
				$('#id_' + day + '_matin_fin').next().attr('disabled', true);
			}

			if (! $('#id_' + day + '_matin_fin').is(':disabled')) {
				$('#id_' + day + '_am_debut').attr('disabled', false);
				$('#id_' + day + '_am_debut').next().attr('disabled', false);
			} else {
				$('#id_' + day + '_am_debut').attr('disabled', true);
				$('#id_' + day + '_am_debut').next().attr('disabled', true);
			}

		});

	};

}); 