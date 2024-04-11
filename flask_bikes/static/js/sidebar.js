function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    var content = sidebar.querySelector('.sidebar-content');
    var map = document.getElementById("map");

    if (sidebar.style.width === "0px" || sidebar.style.width === "") {
        sidebar.style.width = "250px"; 
        map.style.marginLeft = "250px"; 
        content.style.opacity = "1";
        content.style.pointerEvents = "auto";
    } else {
        sidebar.style.width = "0";
        map.style.marginLeft = "0";
        content.style.opacity = "0";
        content.style.pointerEvents = "none";
    }
}
