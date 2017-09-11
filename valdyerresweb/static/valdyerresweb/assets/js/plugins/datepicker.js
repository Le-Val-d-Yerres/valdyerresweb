var Datepicker = function () {

    return {

        //Datepickers
        initDatepicker: function () {
            // Regular datepicker
            $('#date').datepicker({
                dateFormat: 'dd.mm.yy',
                prevText: '<i class="fa fa-angle-left"></i>',
                nextText: '<i class="fa fa-angle-right"></i>'
            });

            // Date range
            $('#start').datepicker({
                dateFormat: 'dd.mm.yy',
                prevText: '<i class="fa fa-angle-left"></i>',
                nextText: '<i class="fa fa-angle-right"></i>',
                onSelect: function (selectedDate) {
                    $('#finish').datepicker('option', 'minDate', selectedDate);
                }
            });
            $('#finish').datepicker({
                dateFormat: 'dd.mm.yy',
                prevText: '<i class="fa fa-angle-left"></i>',
                nextText: '<i class="fa fa-angle-right"></i>',
                onSelect: function (selectedDate) {
                    $('#start').datepicker('option', 'maxDate', selectedDate);
                }
            });

            // Inline datepicker
            $('#inline').datepicker({
                dateFormat: 'dd.mm.yy',
                prevText: '<i class="fa fa-angle-left"></i>',
                nextText: '<i class="fa fa-angle-right"></i>'
            });

            // Inline date range
            $('#inline-start').datepicker({
                dateFormat: 'dd.mm.yy',
                prevText: '<i class="fa fa-angle-left"></i>',
                nextText: '<i class="fa fa-angle-right"></i>',
                onSelect: function (selectedDate) {
                    $('#inline-finish').datepicker('option', 'minDate', selectedDate);
                }
            });
            $('#inline-finish').datepicker({
                dateFormat: 'dd.mm.yy',
                prevText: '<i class="fa fa-angle-left"></i>',
                nextText: '<i class="fa fa-angle-right"></i>',
                onSelect: function (selectedDate) {
                    $('#inline-start').datepicker('option', 'maxDate', selectedDate);
                }
            });

            /* French initialisation for the jQuery UI date picker plugin. */
            /* Written by Keith Wood (kbwood{at}iinet.com.au),
                          Stéphane Nahmani (sholby@sholby.net),
                          Stéphane Raimbault <stephane.raimbault@gmail.com> */
            ( function (factory) {
                if (typeof define === "function" && define.amd) {

                    // AMD. Register as an anonymous module.
                    define(["../widgets/datepicker"], factory);
                } else {

                    // Browser globals
                    factory(jQuery.datepicker);
                }
            }(function (datepicker) {

                datepicker.regional.fr = {
                    closeText: "Fermer",
                    prevText: "Précédent",
                    nextText: "Suivant",
                    currentText: "Aujourd'hui",
                    monthNames: ["janvier", "février", "mars", "avril", "mai", "juin",
                        "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
                    monthNamesShort: ["janv.", "févr.", "mars", "avr.", "mai", "juin",
                        "juil.", "août", "sept.", "oct.", "nov.", "déc."],
                    dayNames: ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"],
                    dayNamesShort: ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."],
                    dayNamesMin: ["D", "L", "M", "M", "J", "V", "S"],
                    weekHeader: "Sem.",
                    dateFormat: "dd/mm/yy",
                    firstDay: 1,
                    isRTL: false,
                    showMonthAfterYear: false,
                    yearSuffix: ""
                };
                datepicker.setDefaults(datepicker.regional.fr);

                return datepicker.regional.fr;

            }) );
        }

    };
}();