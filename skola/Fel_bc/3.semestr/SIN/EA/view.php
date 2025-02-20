<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="cs" xml:lang="cs">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="http://ocw.cvut.cz/moodle/theme/standard/styles.php" />
<link rel="stylesheet" type="text/css" href="http://ocw.cvut.cz/moodle/theme/standardwhite/styles.php" />

<!--[if IE 7]>
    <link rel="stylesheet" type="text/css" href="http://ocw.cvut.cz/moodle/theme/standard/styles_ie7.css" />
<![endif]-->
<!--[if IE 6]>
    <link rel="stylesheet" type="text/css" href="http://ocw.cvut.cz/moodle/theme/standard/styles_ie6.css" />
<![endif]-->


    <meta name="keywords" content="moodle, Y36SIN - ZS 09/10: Šablona pro EA " />
    <title>Y36SIN - ZS 09/10: Šablona pro EA</title>
    <link rel="shortcut icon" href="http://ocw.cvut.cz/moodle/theme/standardwhite/favicon.ico" />
    <!--<style type="text/css">/*<![CDATA[*/ body{behavior:url(http://ocw.cvut.cz/moodle/lib/csshover.htc);} /*]]>*/</style>-->

<script type="text/javascript" src="http://ocw.cvut.cz/moodle/lib/javascript-static.js"></script>
<script type="text/javascript" src="http://ocw.cvut.cz/moodle/lib/javascript-mod.php"></script>
<script type="text/javascript" src="http://ocw.cvut.cz/moodle/lib/overlib/overlib.js"></script>
<script type="text/javascript" src="http://ocw.cvut.cz/moodle/lib/overlib/overlib_cssstyle.js"></script>
<script type="text/javascript" src="http://ocw.cvut.cz/moodle/lib/cookies.js"></script>
<script type="text/javascript" src="http://ocw.cvut.cz/moodle/lib/ufo.js"></script>
<script type="text/javascript" src="http://ocw.cvut.cz/moodle/lib/dropdown.js"></script>  

<script type="text/javascript" defer="defer">
//<![CDATA[
setTimeout('fix_column_widths()', 20);
//]]>
</script>
<script type="text/javascript">
//<![CDATA[
function openpopup(url,name,options,fullscreen) {
  fullurl = "http://ocw.cvut.cz/moodle" + url;
  windowobj = window.open(fullurl,name,options);
  if (fullscreen) {
     windowobj.moveTo(0,0);
     windowobj.resizeTo(screen.availWidth,screen.availHeight);
  }
  windowobj.focus();
  return false;
}

function uncheckall() {
  void(d=document);
  void(el=d.getElementsByTagName('INPUT'));
  for(i=0;i<el.length;i++) {
    void(el[i].checked=0);
  }
}

function checkall() {
  void(d=document);
  void(el=d.getElementsByTagName('INPUT'));
  for(i=0;i<el.length;i++) {
    void(el[i].checked=1);
  }
}

function inserttext(text) {
  text = ' ' + text + ' ';
  if ( opener.document.forms['theform'].message.createTextRange && opener.document.forms['theform'].message.caretPos) {
    var caretPos = opener.document.forms['theform'].message.caretPos;
    caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? text + ' ' : text;
  } else {
    opener.document.forms['theform'].message.value  += text;
  }
  opener.document.forms['theform'].message.focus();
}

function getElementsByClassName(oElm, strTagName, oClassNames){
	var arrElements = (strTagName == "*" && oElm.all)? oElm.all : oElm.getElementsByTagName(strTagName);
	var arrReturnElements = new Array();
	var arrRegExpClassNames = new Array();
	if(typeof oClassNames == "object"){
		for(var i=0; i<oClassNames.length; i++){
			arrRegExpClassNames.push(new RegExp("(^|\\s)" + oClassNames[i].replace(/\-/g, "\\-") + "(\\s|$)"));
		}
	}
	else{
		arrRegExpClassNames.push(new RegExp("(^|\\s)" + oClassNames.replace(/\-/g, "\\-") + "(\\s|$)"));
	}
	var oElement;
	var bMatchesAll;
	for(var j=0; j<arrElements.length; j++){
		oElement = arrElements[j];
		bMatchesAll = true;
		for(var k=0; k<arrRegExpClassNames.length; k++){
			if(!arrRegExpClassNames[k].test(oElement.className)){
				bMatchesAll = false;
				break;
			}
		}
		if(bMatchesAll){
			arrReturnElements.push(oElement);
		}
	}
	return (arrReturnElements)
}
//]]>
</script>
</head>

<body  class="mod-resource course-165 dir-ltr lang-cs_utf8" id="mod-resource-view">

<div id="page">

    <div id="header" class=" clearfix">        <h1 class="headermain">Y36SIN - Úvod do softwarového inženýrství</h1>
        <div class="headermenu"><div class="navigation">
<ul><li><form action="http://ocw.cvut.cz/moodle/mod/resource/view.php" onclick="this.target='_top';"><fieldset class="invisiblefieldset"><input type="hidden" name="id" value="5285" /><button type="submit" title="Předchozí činnost"><span class="arrow ">&#x25C4;</span><span class="accesshide " >&nbsp;Předchozí činnost</span></button></fieldset></form></li><li><form action="http://ocw.cvut.cz/moodle/course/jumpto.php" method="get"  id="navmenupopup" class="popupform"><div><select id="navmenupopup_jump" name="jump" onchange="self.location=document.getElementById('navmenupopup').jump.options[document.getElementById('navmenupopup').jump.selectedIndex].value;">
   <option value="http://ocw.cvut.cz/moodle/mod/forum/view.php?id=5280" style="background-image: url(http://ocw.cvut.cz/moodle/mod/forum/icon.gif);">Novinky</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5281" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Studijní materiály</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5313" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Přednášky</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5283" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Přednášky Arlow</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5284" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Studentské referáry (ORM, CMS, SVN, Bugtracking,Ja...</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5361" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Case nástroj Enterprise Architect - souhlas s lice...</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5285" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Návod pro nastavení EA</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5286" selected="selected" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Přejít na...</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5287" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Vaše projekty</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5288" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Podmínky odevzdávání dokumentace projektů</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5289" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Cvičení - Co a kdy se odevzdává?</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5290" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Šablona na přerozdělování bodů</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5312" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Šablona výkazu práce (=projektový deník)</option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5331" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Ukázkový projekt</option>
   <option value="http://ocw.cvut.cz/moodle/mod/forum/view.php?id=5292" style="background-image: url(http://ocw.cvut.cz/moodle/mod/forum/icon.gif);">Fórum -  Přesuny studentů mezi cvičeními</option>
   <option value="http://ocw.cvut.cz/moodle/mod/forum/view.php?id=5293" style="background-image: url(http://ocw.cvut.cz/moodle/mod/forum/icon.gif);">Fórum - Dotazy studentů studentům</option>
   <option value="http://ocw.cvut.cz/moodle/mod/forum/view.php?id=5294" style="background-image: url(http://ocw.cvut.cz/moodle/mod/forum/icon.gif);">Fórum - Dotazy studentů vyučujícím</option>
   <option value="http://ocw.cvut.cz/moodle/mod/forum/view.php?id=5298" style="background-image: url(http://ocw.cvut.cz/moodle/mod/forum/icon.gif);">Zakládání projektu </option>
   <option value="http://ocw.cvut.cz/moodle/mod/resource/view.php?id=5297" style="background-image: url(http://ocw.cvut.cz/moodle/mod/resource/icon.gif);">Podmínky a hodnocení předmětu</option>
</select><input type="hidden" name="sesskey" value="e4jxdc1fSw" /><div id="noscriptnavmenupopup" style="display: inline;"><input type="submit" value="Proveď" /></div><script type="text/javascript">
//<![CDATA[
document.getElementById("noscriptnavmenupopup").style.display = "none";
//]]>
</script></div></form></li><li><form action="http://ocw.cvut.cz/moodle/mod/resource/view.php"  onclick="this.target='_top';"><fieldset class="invisiblefieldset"><input type="hidden" name="id" value="5287" /><button type="submit" title="Další činnost"><span class="accesshide " >Další činnost&nbsp;</span><span class="arrow ">&#x25BA;</span></button></fieldset></form></li></ul>
</div></div>
    </div>    <div class="navbar clearfix">
        <div class="breadcrumb"><h2 class="accesshide " >Nacházíte se zde</h2> <ul>
<li class="first"><a onclick="this.target='_top'" href="http://ocw.cvut.cz/moodle/">moodle</a></li><li class="first"> <span class="accesshide " >/&nbsp;</span><span class="arrow sep">&#x25BA;</span> <a onclick="this.target='_top'" href="http://ocw.cvut.cz/moodle/course/view.php?id=165">Y36SIN - ZS 09/10</a></li><li class="first"> <span class="accesshide " >/&nbsp;</span><span class="arrow sep">&#x25BA;</span> <a onclick="this.target='_top'" href="http://ocw.cvut.cz/moodle/mod/resource/index.php?id=165">Studijní materiály</a></li><li class="first"> <span class="accesshide " >/&nbsp;</span><span class="arrow sep">&#x25BA;</span> Šablona pro EA</li></ul></div>
        <div class="navbutton">&nbsp;</div>
    </div>
    <!-- END OF HEADER -->
    <div id="content" class=" clearfix">
<script type="text/javascript">
<!--
openpopup('/mod/resource/view.php?inpopup=true&id=5286','resource3369','resizable=1,scrollbars=1,directories=1,location=1,menubar=1,toolbar=1,status=1,width=620,height=450');

-->
</script><div class="box generalbox generalboxcontent boxaligncenter"><p>Šablona obsahující doporučenou strukturu balíčků pro program Eneterprise Archotect.</p></div><div class="popupnotice">Tento studijní materiál by se měl zobrazovat v novém okně<br />Pokud se tak nestalo, klikněte zde: <a href="http://ocw.cvut.cz/moodle/mod/resource/view.php?inpopup=true&amp;id=5286" onclick="this.target='resource3369'; return openpopup('/mod/resource/view.php?inpopup=true&amp;id=5286', 'resource3369','resizable=1,scrollbars=1,directories=1,location=1,menubar=1,toolbar=1,status=1,width=620,height=450');">Šablona pro EA</a></div></div><div id="footer"><hr /><p class="helplink"></p><div class="logininfo">Momentálně na stránky přistupujete s právy hosta. (<a  href="https://ocw.cvut.cz/moodle/login/index.php">Přihlásit se</a>)</div><div class="homelink"><a  href="http://ocw.cvut.cz/moodle/course/view.php?id=165">Y36SIN - ZS 09/10</a></div></div>
</div>
</body>
</html>
