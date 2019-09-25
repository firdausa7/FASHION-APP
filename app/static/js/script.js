function touch() {
    var chg = document.getElementById("navbox");

    if (chg.style.width == "300px") {
        chg.style.width = "0px";
        // navs.style.display = "none";
        navs.style.opacity = "0";
        btn.style.top = "10px";
        d1.classList.remove("d1");
        d2.classList.remove("d2");
        d3.classList.remove("d3");
    } else {
        chg.style.width = "300px";
        //  navs.style.display = "block";
        navs.style.opacity = "1";
        btn.style.top = "18px";
        d1.classList.add("d1");
        d2.classList.add("d2");
        d3.classList.add("d3");
    }

}

function buzz() {
    navigator.vibrate(20);
}