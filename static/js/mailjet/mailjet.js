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

function affichageReponse(texte)
{
	form = document.getElementById('mailJetForm');
	form.parentNode.removeChild(form);
	
	mailBox = document.getElementById('mailBox');
	
	divAlert = document.createElement("div");
	
	if (texte == "0")
	{
		divAlert.className = "alert mailMsg";
		divAlert.innerHTML = "Merci d'utiliser un courriel valide.";
	}
	else if (texte == "1")
	{
		divAlert.className = "alert mailMsg alert-success";
		divAlert.innerHTML = "Votre adresse a été ajoutée. Un courriel vous a été envoyé, vous avez 24h pour confirmer votre adresse.";
	}
	else if (texte == "2")
	{
		divAlert.className = "alert mailMsg alert-danger";
		divAlert.innerHTML = "Une erreur est survenue lors de l'ajout de votre courriel, merci de réessayer plus tard.";
	}
	else if (texte == "3")
	{
		divAlert.className = "alert mailMsg alert-info";
		divAlert.innerHTML = "Vous êtes déjà abonné à la lettre d'informations du Val d'Yerres.";
	}
	else if (texte == "4")
	{
		divAlert.className = "alert mailMsg";
		divAlert.innerHTML = "Vous devez accepter les cookies pour utiliser ce formulaire.";
	}
	else
	{
		divAlert.className = "alert mailMsg alert-danger";
		divAlert.innerHTML = "Une erreur est survenue lors de l'ajout de votre courriel, merci de réessayer plus tard.";
	}
	
	mailBox.appendChild(divAlert);
}

function mailjet()
{
	var mail = encodeURIComponent(document.getElementById('mail').value);
	
	DOMptr = document.getElementById('mailJetForm');
	var token = DOMptr.firstChild.value;
	
    var xhr = getXMLHttpRequest();
    
    if (xhr && xhr.readyState != 0) 
    {
            xhr.abort();
            delete xhr;
    }
    
    xhr.onreadystatechange = function() {
            if (xhr.readyState == 4)
            {
            	if (xhr.status == 200)
            	{
            		affichageReponse(xhr.responseText);
            	}
            	else
            	{
            		affichageReponse("2");
            	}
                    
            }
    }
    
    xhr.open("POST", "/mail/mailjet-ajax.html", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("email="+mail+"&csrftoken="+token);
}
