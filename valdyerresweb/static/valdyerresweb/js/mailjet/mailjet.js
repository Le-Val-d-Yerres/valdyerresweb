function getXMLHttpRequest() 
{
        var xhr = null;
        
        if (window.XMLHttpRequest || window.ActiveXObject) 
        {
                if (window.ActiveXObject) 
                {
                        try 
                        {
                                xhr = new ActiveXObject("Msxml2.XMLHTTP");
                        } 
                        catch(e) 
                        {
                                xhr = new ActiveXObject("Microsoft.XMLHTTP");
                        }
                } 
                else 
                {
                        xhr = new XMLHttpRequest();
                }
        } 
        else 
        {
                return null;
        }
        
        return xhr;
}

var ajaxReponse;

function affichageReponse()
{
	form = document.getElementById('mailAjax');
	
	
	
	if (ajaxReponse == "0")
	{
		document.getElementById('lettreErreur').innerHTML = "Merci d'utiliser un courriel valide.";
		document.getElementById('lettreErreur').className = "alert mailMsg";
	}
	else if (ajaxReponse == "1")
	{
		mailBox = document.getElementById('mailBox');
		form.parentNode.removeChild(form);
		
		divAlert = document.createElement("div");
		
		divAlert.className = "alert mailMsg alert-success";
		divAlert.innerHTML = "Votre adresse a été ajoutée. Un courriel vous a été envoyé, vous avez 24h pour confirmer votre adresse.";
		
		mailBox.appendChild(divAlert);
	}
	else if (ajaxReponse == "2")
	{
		document.getElementById('lettreErreur').innerHTML = "Une erreur est survenue lors de l'ajout de votre courriel, merci de réessayer plus tard.";
		document.getElementById('lettreErreur').className = "alert mailMsg alert-danger";
	}
	else if (ajaxReponse == "3")
	{
		document.getElementById('lettreErreur').innerHTML = "Vous êtes déjà abonné à la lettre d'informations du Val d'Yerres.";
		document.getElementById('lettreErreur').className = "alert mailMsg alert-info";
	}
	else if (ajaxReponse == "4")
	{
		document.getElementById('lettreErreur').innerHTML = "Vous devez accepter les cookies pour utiliser ce formulaire.";
		document.getElementById('lettreErreur').className = "alert mailMsg";
	}
	else if (ajaxReponse == "-1")
	{
		setTimeout(affichageReponse, 500);
	}
	else
	{
		document.getElementById('lettreErreur').innerHTML = "Une erreur est survenue lors de l'ajout de votre courriel, merci de réessayer plus tard.";
		document.getElementById('lettreErreur').className = "alert mailMsg alert-danger";
	}
}

function mailjet()
{
	var mail = encodeURIComponent(document.getElementById('mail').value);
	var token = document.getElementById('csrftoken').value;
	
    var xhr = getXMLHttpRequest();
    
    if (xhr && xhr.readyState != 0) 
    {
            xhr.abort();
            delete xhr;
    }
    
    document.getElementById('lettreErreur').className = "mailMsg";
    document.getElementById('lettreErreur').innerHTML = '<img src="/static/valdyerresweb/img/loader.gif" />';
	setTimeout(affichageReponse, 500);
	ajaxReponse = "-1";
    
    xhr.onreadystatechange = function() {
            if (xhr.readyState == 4)
            {
            	if (xhr.status == 200)
            	{
            		ajaxReponse = xhr.responseText;
            	}
            	else
            	{
            		ajaxReponse = "2";
            	}
                    
            }
    }
    
    xhr.open("POST", "/mail/mailjet-ajax.html", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("email="+mail+"&csrftoken="+token);
}

function setCSRFToken()
{
	var xhr = getXMLHttpRequest();
	
	if (xhr && xhr.readyState != 0) 
	{
	        xhr.abort();
	        delete xhr;
	}
	
	xhr.onreadystatechange = function() 
	{
        if (xhr.readyState == 4)
        {
        	if (xhr.status == 200)
        	{
     			document.getElementById('csrftoken').value = xhr.responseText;
        	} 
        }
	}
	
	xhr.open("GET", "/mail/get-token.html", true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.send();
}
