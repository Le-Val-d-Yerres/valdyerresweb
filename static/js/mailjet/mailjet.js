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
	
	
	
	if (texte == "0")
	{
		document.getElementById('lettreErreur').innerHTML = "Merci d'utiliser un courriel valide.";
		document.getElementById('lettreErreur').className = "alert mailMsg";
	}
	else if (texte == "1")
	{
		mailBox = document.getElementById('mailBox');
		form.parentNode.removeChild(form);
		
		document.getElementById('lettreErreur').innerHTML = "";
		document.getElementById('lettreErreur').className = "";
		
		divAlert = document.createElement("div");
		
		divAlert.className = "alert mailMsg alert-success";
		divAlert.innerHTML = "Votre adresse a été ajoutée. Un courriel vous a été envoyé, vous avez 24h pour confirmer votre adresse.";
		
		mailBox.appendChild(divAlert);
	}
	else if (texte == "2")
	{
		document.getElementById('lettreErreur').innerHTML = "Une erreur est survenue lors de l'ajout de votre courriel, merci de réessayer plus tard.";
		document.getElementById('lettreErreur').className = "alert mailMsg alert-danger";
	}
	else if (texte == "3")
	{
		document.getElementById('lettreErreur').innerHTML = "Vous êtes déjà abonné à la lettre d'informations du Val d'Yerres.";
		document.getElementById('lettreErreur').className = "alert mailMsg alert-info";
	}
	else if (texte == "4")
	{
		document.getElementById('lettreErreur').innerHTML = "Vous devez accepter les cookies pour utiliser ce formulaire.";
		document.getElementById('lettreErreur').className = "alert mailMsg";
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
