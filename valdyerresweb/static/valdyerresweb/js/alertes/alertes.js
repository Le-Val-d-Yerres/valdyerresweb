function compteur()
{
        var content = document.getElementById("alerteMessage").value;
        
        var longueur = content.length;
        
        if (longueur < 450)
        {
                document.getElementById("alerteCompteur").innerHTML = longueur+"/500";
        }
        else
        {
                document.getElementById("alerteCompteur").innerHTML = "<span style=\"color: red\">"+longueur+"/500</span>";
        }
        
        if (longueur > 0)
        {
        	document.getElementById('msgErreur').className = "control-group";
        }
}

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
     			document.getElementById('tokenCsrf').value = xhr.responseText;
        	} 
        }
	}
	
	xhr.open("GET", "/equipements/alertes/get-token.html", true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.send();
}

var ajaxReponse;

function affichage()
{
	if (ajaxReponse == "0")
	{
		document.getElementById('alerteErreur').innerHTML = '<div style="margin-right: 10px;" class="alert">Merci d\'utiliser une adresse courriel valide.</div>';
	}
	else if (ajaxReponse == "1")
	{
		var form = document.getElementById("form1");
		while (form.firstChild) {
			form.removeChild(form.firstChild);
		}
		
		var form = document.getElementById("form2");
		while (form.firstChild) {
			form.removeChild(form.firstChild);
		}
		
		document.getElementById('alerteErreur').innerHTML = '';
		
		document.getElementById('form1').innerHTML = '<div style="margin-top: 10px;margin-right: 10px;text-align: left;" class="alert alert-success">Votre message a bien été envoyé, nous vous répondrons dans les plus brefs délais.</div>';
	}
	else if (ajaxReponse == "2")
	{
		document.getElementById('alerteErreur').innerHTML = '<div style="margin-right: 10px;" class="alert alert-danger">Une erreur s\'est produite lors de l\'envoi de votre message, merci de réessayer plus tard.</div>';
	}
	else if (ajaxReponse == "3")
	{
		document.getElementById('alerteErreur').innerHTML = '<div style="margin-right: 10px;" class="alert">Merci d\'utiliser un numéro de téléphone valide.</div>';
	}
	else if (ajaxReponse == "4")
	{
		document.getElementById('alerteErreur').innerHTML = '<div style="margin-right: 10px;" class="alert">Merci d\'attendre une minute entre deux signalements.</div>';
	}
	else if (ajaxReponse == "5")
	{
		document.getElementById('alerteErreur').innerHTML = '<div style="margin-right: 10px;" class="alert">Vous devez accepter les cookies pour utiliser ce formulaire.</div>';
	}
	else if (ajaxReponse == "6")
	{
		document.getElementById('alerteErreur').innerHTML = '<div class="alert">Merci de remplir tous les champs.</div>'
	}
	else if (ajaxReponse == "-1")
	{
		setTimeout(affichage, 500);
	}
	else
	{
		document.getElementById('alerteErreur').innerHTML = '<div style="margin-right: 10px;" class="alert alert-danger">Une erreur s\'est produite lors de l\'envoi de votre message, merci de réessayer plus tard.</div>';
	}
}

function envoiAlerte()
{
	var valide = true;
	var nom = encodeURIComponent(document.getElementById('alerteNom').value);
	if (nom == "")
	{
		valide = false;
		document.getElementById('nomErreur').className = "control-group error";
	}
	else
	{
		document.getElementById('nomErreur').className = "control-group";
	}
	
	var prenom = encodeURIComponent(document.getElementById('alertePrenom').value);
	if (prenom == "")
	{
		valide = false;
		document.getElementById('prenomErreur').className = "control-group error";
	}
	else
	{
		document.getElementById('prenomErreur').className = "control-group";
	}
	
	var rue = encodeURIComponent(document.getElementById('alerteRue').value);
	if (rue == "")
	{
		valide = false;
		document.getElementById('rueErreur').className = "control-group error";
	}
	else
	{
		document.getElementById('rueErreur').className = "control-group";
	}
	
	var codePostal = encodeURIComponent(document.getElementById('alerteCodePostal').value);
	if (codePostal == "")
	{
		valide = false;
		document.getElementById('codepostalErreur').className = "control-group error";
	}
	else
	{
		document.getElementById('codepostalErreur').className = "control-group";
	}
	
	var ville = encodeURIComponent(document.getElementById('alerteVille').value);
	if (ville == "")
	{
		valide = false;
		document.getElementById('villeErreur').className = "control-group error";
	}
	else
	{
		document.getElementById('villeErreur').className = "control-group";
	}
	
	var tel = encodeURIComponent(document.getElementById('alerteTel').value);
	if (tel == "")
	{
		valide = false;
		document.getElementById('telErreur').className = "control-group error";
	}
	else
	{
		document.getElementById('telErreur').className = "control-group";
	}
	
	var mail = encodeURIComponent(document.getElementById('alerteMail').value);
	if (mail == "")
	{
		valide = false;
		document.getElementById('mailErreur').className = "control-group error";
	}
	else
	{
		document.getElementById('mailErreur').className = "control-group";
	}
	
	var msg = encodeURIComponent(document.getElementById('alerteMessage').value);
	if (msg == "")
	{
		valide = false;
		document.getElementById('msgErreur').className = "control-group error";
	}
	else
	{
		document.getElementById('msgErreur').className = "control-group";
	}
	
	var alerteId = encodeURIComponent(document.getElementById('alerteId').value);
	var equipement = encodeURIComponent(document.getElementById('equipementId').value);
	
	var token = encodeURIComponent(document.getElementById('tokenCsrf').value);
	
	document.getElementById('alerteErreur').innerHTML = '<img style="margin-left: 50px;" src="/static/valdyerresweb/img/loader.gif" />';
	setTimeout(affichage, 500);
	ajaxReponse = "-1";

	if (valide)
	{
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
	            		ajaxReponse = xhr.responseText;
	            	}    
	            }
	    }
	    
	    xhr.open("POST", "/equipements/alertes/alertes-ajax.html", true);
	    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	    xhr.send("equipementId="+equipement+"&alerteId="+alerteId+"&nom="+nom+"&prenom="+prenom+"&rue="+rue+"&codePostal="+codePostal+"&ville="+ville+"&tel="+tel+"&mail="+mail+"&msg="+msg+"&csrftoken="+token);	
	}
	else
	{	
		ajaxReponse = "6";
	}
}