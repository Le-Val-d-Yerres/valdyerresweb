var Masking = function () {

    return {
        
        //Masking
        initMasking: function () {
	        $(".date1").mask('99/99/9999', {placeholder:'_'});
	        $("#phone").mask('99 99 99 99 99', {placeholder:'_'});
	        $("#postal").mask('99999', {placeholder:'_'});
	        $("#card").mask('9999-9999-9999-9999', {placeholder:'X'});
	        $("#serial").mask('***-***-***-***-***-***', {placeholder:'_'});
	        $("#tax").mask('99-9999999', {placeholder:'X'});
        }

    };
    
}();