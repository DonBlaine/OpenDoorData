function showNavBar(){
	var nb = document.getElementById("navbar");
	var pt = document.getElementById("page_name");
	var nbstyle = window.getComputedStyle(nb).getPropertyValue('width');
	var bt = document.getElementById("navbar_symbol");
	var nt = document.getElementById("product_name");

	if (nbstyle == "0px"){
		pt.style.opacity = "0";
		nt.style.transition = "opacity 1s"
		nt.style.display = "inline-block";
		bt.style.marginLeft = "230px";
		nb.style.width = "220px";
		nt.style.opacity = "1";

	}
	else{
		pt.style.opacity = "1";
		nt.style.transition = "opacity 0s";
		bt.style.marginLeft = "10px";
		nb.style.width = 0;
		nt.style.opacity = "0";
	}
}
